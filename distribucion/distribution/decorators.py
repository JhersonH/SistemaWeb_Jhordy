from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(allowed_roles):
    """
    Decorador para vistas FBV y CBV.
    - allowed_roles: lista de roles permitidos (['ops_manager', 'dispatcher'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user_role = getattr(getattr(request.user, "profile", None).role, "role_type", None)

            if request.user.is_superuser or user_role in allowed_roles:
                return view_func(request, *args, **kwargs)

            raise PermissionDenied("No tienes permisos suficientes.")
        return _wrapped_view
    return decorator
