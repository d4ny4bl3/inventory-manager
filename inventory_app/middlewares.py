from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin


class LoginRequiredMiddleware(MiddlewareMixin):
    """Middleware, který přesměruje uživatele na přihlašovací stránku, s výjímkou stránky /login/ a /admin/"""

    @staticmethod
    def process_request(request):
        # Získání cesty aktuální URL
        current_url = request.path_info

        # Pokud je uživatel nepřihlášený a stránka není login nebo sign-up
        if not request.user.is_authenticated and current_url != '/login/' and not current_url.startswith('/admin/'):
            return redirect(settings.LOGIN_URL)
