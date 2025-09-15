from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from dashboard.views import CustomLoginView
from dashboard.views import custom_permission_denied_view

handler403 = custom_permission_denied_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('dashboard/', include('dashboard.urls')),
    path("users/", include("users.urls", namespace="users")),
    path('transport/', include('transport.urls')),
    path("accounts/login/", CustomLoginView.as_view(), name="login"),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^favicon\\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)