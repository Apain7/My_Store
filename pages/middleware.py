from django.shortcuts import redirect
from django.urls import resolve

PUBLIC_URL_NAMES = [
    'login',
    'logout_user',
    'register',
    'register_api',
    'token_obtain_pair',
    'token_refresh',
]

class AdminAccessControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            if not request.user.is_authenticated:
                return redirect('login')
            if not request.user.is_superuser:
                return redirect('home')
        return self.get_response(request)

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            current_url_name = resolve(request.path_info).url_name
        except:
            current_url_name = None

        print(f"URL Name: {current_url_name}, Authenticated: {request.user.is_authenticated}")

        if not request.user.is_authenticated and current_url_name not in PUBLIC_URL_NAMES:
            print(f"Redirecting to login from {current_url_name}")
            return redirect('login')

        return self.get_response(request)

