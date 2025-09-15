def dark_mode_context(request):
    if request.user.is_authenticated and hasattr(request.user, 'preferences'):
        return {'dark_mode': request.user.preferences.dark_mode}
    return {'dark_mode': False}

def user_preferences(request):
    if request.user.is_authenticated:
        from preferences.models import UserPreference
        try:
            dark_mode = UserPreference.objects.get(user=request.user).dark_mode
        except UserPreference.DoesNotExist:
            dark_mode = False
    else:
        dark_mode = False

    return {'dark_mode': dark_mode}
