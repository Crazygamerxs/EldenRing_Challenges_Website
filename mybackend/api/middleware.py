from django.http import HttpResponse
from .models import SiteSettings

class SiteSettingsMiddleware:
    """
    Middleware to apply site settings across the application
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            settings = SiteSettings.get_settings()

            # Define allowed paths during maintenance
            allowed_paths = [
                '/api/login/',
                '/admin/login/',
                '/api/csrf-token/',
                '/api/admin/',
                '/admin/',
            ]

            # Maintenance mode check
            if settings.maintenance_mode:
                if not any(request.path.startswith(p) for p in allowed_paths):
                    is_admin = hasattr(request, 'user') and request.user.is_authenticated and request.user.is_staff
                    if not is_admin:
                        return HttpResponse(
                            '''
                            <html>
                            <head><title>Maintenance Mode</title></head>
                            <body style="background: #111618; color: #f0f0f0; font-family: Arial; text-align: center; padding: 50px;">
                                <h1 style="color: #a98b2d;">Site Under Maintenance</h1>
                                <p>We're currently performing maintenance. Please check back later.</p>
                            </body>
                            </html>
                            ''',
                            status=503
                        )

            # Attach settings to request
            request.site_settings = settings

        except Exception:
            # Safely ignore errors (e.g., model not available during migration)
            pass

        return self.get_response(request)
