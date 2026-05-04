class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            print("Logged user role:", request.user.role)
        response = self.get_response(request)
        return response