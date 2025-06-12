# api/middleware.py

class SiteSettingsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Do something with request
        response = self.get_response(request)
        # Do something with response
        return response
