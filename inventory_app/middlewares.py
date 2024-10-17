from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin


# class LoginRequiredMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         current_url = resolve(request.path_info).url_name
#         print(f"Current URL: {request.path_info}, Authenticated: {request.user.is_authenticated}")
#
#         if not request.user.is_authenticated and current_url not in ['login/', '/admin/', '/admin/login/', '/admin/logout/']:
#             return redirect(settings.LOGIN_URL)
#
#         return self.get_response(request)


class LoginRequiredMiddleware(MiddlewareMixin):
    """Middleware, který přesměruje uživatele na přihlašovací stránku, s výjímkou stránky /login/ a /admin/"""

    @staticmethod
    def process_request(request):
        # Získání cesty aktuální URL
        current_url = request.path_info

        # Pokud je uživatel nepřihlášený a stránka není login nebo sign-up
        if not request.user.is_authenticated and current_url != '/login/' and not current_url.startswith('/admin/'):
            return redirect(settings.LOGIN_URL)
