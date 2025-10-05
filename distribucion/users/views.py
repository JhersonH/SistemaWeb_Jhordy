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

import json
import os
from django.conf import settings

# Solo usuarios con rol de administrador (superuser o staff) pueden acceder
def _staff_or_super(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

# Decorador reutilizable para las vistas protegidas
staff_required = user_passes_test(_staff_or_super, login_url='login')

@login_required
@staff_required
def user_list(request):
    users = User.objects.select_related("profile__role").all()
    roles = Role.objects.all()
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

            # ✅ Guardar todos los campos del ProfileForm
            profile.role = pform.cleaned_data.get("role")
            profile.doc_id = pform.cleaned_data.get("doc_id")
            profile.phone = pform.cleaned_data.get("phone")
            profile.avatar = pform.cleaned_data.get("avatar")
            profile.birth_date = pform.cleaned_data.get("birth_date")
            profile.address = pform.cleaned_data.get("address")
            profile.hire_date = pform.cleaned_data.get("hire_date")
            profile.position = pform.cleaned_data.get("position")

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
    # Excluye superusuarios y staff
    employees = (
        Profile.objects
        .select_related("user", "role")
        .exclude(user__is_superuser=True)
        .exclude(user__is_staff=True)
        .order_by("user__username")
    )

    roles = Role.objects.all()

    return render(request, "users/employee_list.html", {
        "employees": employees,
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

@login_required
def load_user_data_by_dni(request):
    """
    Vista que devuelve datos del usuario por DNI/RUC.
    Útil para autocompletado basado en DNI.
    """
    json_path = os.path.join(settings.BASE_DIR, 'users', 'user_api.json')

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return JsonResponse({"error": "Archivo user_api.json no encontrado."}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Error al leer el archivo JSON."}, status=500)

    dni = request.GET.get("dni", "").strip()
    if dni:
        user_data = data.get(dni)
        if user_data:
            return JsonResponse(user_data)
        else:
            return JsonResponse({"error": "DNI no encontrado en la base de datos."}, status=404)

    return JsonResponse(data)

@login_required
def save_profile_data_by_dni(request):
    """
    Vista que recibe DNI y datos de Profile, y los guarda en la base de datos.
    """
    if request.method != 'POST':
        return JsonResponse({"error": "Método no permitido."}, status=405)

    dni = request.POST.get("dni", "").strip()
    first_name = request.POST.get("first_name", "").strip()
    last_name = request.POST.get("last_name", "").strip()
    email = request.POST.get("email", "").strip()
    username = request.POST.get("username", "").strip()
    phone = request.POST.get("phone", "").strip()
    birth_date = request.POST.get("birth_date", "").strip()
    address = request.POST.get("address", "").strip()
    hire_date = request.POST.get("hire_date", "").strip()
    position = request.POST.get("position", "").strip()

    if not dni:
        return JsonResponse({"error": "DNI es requerido."}, status=400)

    # Buscar el usuario por DNI (asumiendo que `doc_id` es el DNI en Profile)
    try:
        profile = Profile.objects.get(doc_id=dni)
        user = profile.user
    except Profile.DoesNotExist:
        # Opcional: crear usuario si no existe
        # user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email)
        # profile = Profile.objects.create(user=user, doc_id=dni)
        return JsonResponse({"error": "Usuario no encontrado con ese DNI."}, status=404)

    # Actualizar datos de User
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.username = username
    user.save()

    # Actualizar datos de Profile
    profile.phone = phone
    if birth_date:
        from datetime import datetime
        profile.birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
    profile.address = address
    if hire_date:
        profile.hire_date = datetime.strptime(hire_date, "%Y-%m-%d").date()
    profile.position = position
    profile.save()

    return JsonResponse({"success": True, "message": "Datos actualizados correctamente."})