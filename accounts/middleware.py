from django.shortcuts import redirect
from django.urls import resolve


class LoginRequireMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Skip static files
        if request.path.startswith('/static'):
            return self.get_response(request)

        resolver_match = resolve(request.path)
        view_name = resolver_match.url_name

        open_views = ['login', 'register', ' index']

        if not request.user.is_authenticated and view_name not in open_views:
            print("VIEW NAME:", view_name)
            return redirect('login')
        return self.get_response(request)
