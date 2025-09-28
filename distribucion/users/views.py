from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import UserProfileUpdateForm
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import update_session_auth_hash
from .forms import UserCreateForm, UserUpdateForm, ProfileForm, AdminSetPasswordForm
from .models import Profile
from roles.models import Role

# Solo usuarios con rol de administrador (superuser o staff) pueden acceder
def _staff_or_super(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

# Decorador reutilizable para las vistas protegidas
staff_required = user_passes_test(_staff_or_super, login_url='login')

@login_required
@staff_required
def user_list(request):
    q = request.GET.get("q", "").strip()
    role_id = request.GET.get("role", "").strip()

    users = User.objects.all().select_related("profile__role")
    roles = Role.objects.all()

    if q:
        users = users.filter(username__icontains=q)
    if role_id:
        users = users.filter(profile__role_id=role_id)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string("users/_user_table.html", {"users": users}, request=request)
        return JsonResponse({"html": html})

    return render(request, "users/list.html", {"users": users, "roles": roles})

@login_required
@staff_required
@transaction.atomic
def user_create(request):
    if request.method == "POST":
        uform = UserCreateForm(request.POST)
        pform = ProfileForm(request.POST, request.FILES)
        if uform.is_valid() and pform.is_valid():
            user = uform.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            for f in ("role", "doc_id", "phone", "avatar"):
                setattr(profile, f, pform.cleaned_data.get(f))
            profile.save()
            messages.success(request, "Usuario creado correctamente.")
            return redirect("users:list")
    else:
        uform = UserCreateForm()
        pform = ProfileForm()
    return render(request, "users/form.html", {
        "title": "Nuevo usuario",
        "user_form": uform,
        "profile_form": pform,
        "is_create": True,
    })

@login_required
@staff_required
@transaction.atomic
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)

    # Seguridad: el admin no debe poder editar su propia cuenta desde aquí
    if request.user == user:
        return HttpResponseForbidden("No puedes editar tu propia cuenta desde esta vista.")

    profile, _ = Profile.objects.get_or_create(user=user)
    if request.method == "POST":
        uform = UserUpdateForm(request.POST, instance=user)
        pform = ProfileForm(request.POST, request.FILES, instance=profile)
        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, "Usuario actualizado.")
            return redirect("users:list")
    else:
        uform = UserUpdateForm(instance=user)
        pform = ProfileForm(instance=profile)
    return render(request, "users/form.html", {
        "title": f"Editar: {user.username}",
        "user_form": uform,
        "profile_form": pform,
        "is_create": False,
        "instance": user,
    })

@login_required
@staff_required
@require_POST
def user_toggle_active(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.user == user:
        return HttpResponseForbidden("No puedes desactivar tu propia cuenta.")

    user.is_active = not user.is_active
    user.save(update_fields=["is_active"])
    messages.info(request, f"Usuario {'activado' if user.is_active else 'desactivado'}.")
    return redirect("users:list")

@login_required
@staff_required
def user_reset_password(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.user == user:
        return HttpResponseForbidden("No puedes resetear tu propia contraseña desde esta vista.")

    if request.method == "POST":
        form = AdminSetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Contraseña cambiada correctamente.")
            return redirect("users:list")
    else:
        form = AdminSetPasswordForm(user)
    return render(request, "users/reset_password.html", {"form": form, "user_obj": user})

@login_required
@staff_required
def employee_list(request):
    q = request.GET.get("q", "").strip()
    role_id = request.GET.get("role", "").strip()

    # Excluye usuarios superusuarios o staff
    employees = Profile.objects.select_related("user", "role") \
        .exclude(user__is_superuser=True) \
        .exclude(user__is_staff=True)

    roles = Role.objects.all()

    if q:
        employees = employees.filter(user__first_name__icontains=q)
    if role_id:
        employees = employees.filter(role_id=role_id)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string(
            "users/_employee_table.html",
            {"employees": employees},  # 👈 MISMO NOMBRE
            request=request
        )
        return JsonResponse({"html": html})

    return render(request, "users/employee_list.html", {
        "employees": employees,  # 👈 MISMO NOMBRE
        "roles": roles,
    })

@login_required
@staff_required
@transaction.atomic
def employee_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        pform = ProfileForm(request.POST, request.FILES, instance=profile)
        if pform.is_valid():
            pform.save()
            messages.success(request, "Empleado actualizado correctamente.")
            return redirect("users:employee_list")
    else:
        pform = ProfileForm(instance=profile)

    return render(request, "users/employee_form.html", {
        "profile_form": pform,
        "user": user,
        "title": "Editar Empleado"
    })

@login_required
@transaction.atomic
def profile_update(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        user_form = UserProfileUpdateForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_obj = user_form.save(commit=False)
            new_password = user_form.cleaned_data.get("new_password")

            print("Contraseña nueva recibida:", new_password)  # DEBUG

            if new_password and new_password.strip():
                user_obj.set_password(new_password)
                user_obj.save()
                update_session_auth_hash(request, user_obj)  # No cerrar sesión
            else:
                user_obj.save()

            profile_form.save()

            messages.success(request, "Tu perfil ha sido actualizado correctamente.")
            return redirect("users:profile_update")
    else:
        user_form = UserProfileUpdateForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, "users/profile_form.html", {
        "user_form": user_form,
        "profile_form": profile_form,
        "title": "Mi perfil"
    })
