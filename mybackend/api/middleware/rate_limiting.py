import time
from django.core.cache import cache
from django.http import JsonResponse
from django.conf import settings
import logging

logger = logging.getLogger('security')

class RateLimitMiddleware:
    """
    Rate limiting middleware to prevent abuse
    """
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Rate limits per endpoint type (requests per minute)
        self.rate_limits = {
            'api/login/': 5,           # Login attempts
            'api/signup/': 3,          # Signup attempts
            'api/submit_run/': 10,     # Submission attempts
            'api/password-reset/': 2,  # Password reset attempts
            'default': 60,             # Default for other API endpoints
        }
        
        # Burst limits (requests per 10 seconds)
        self.burst_limits = {
            'api/login/': 3,
            'api/signup/': 2,
            'api/submit_run/': 5,
            'default': 20,
        }

    def __call__(self, request):
        # Skip rate limiting for admin users and health checks
        if (request.user.is_authenticated and request.user.is_staff) or \
           request.path.startswith('/api/health/'):
            return self.get_response(request)
        
        # Get client IP
        client_ip = self.get_client_ip(request)
        
        # Check rate limits for API endpoints
        if request.path.startswith('/api/'):
            if not self.check_rate_limit(request, client_ip):
                logger.warning(f"Rate limit exceeded for IP {client_ip} on {request.path}")
                return JsonResponse({
                    'error': 'Rate limit exceeded. Please try again later.',
                    'retry_after': 60
                }, status=429)
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Get the real client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def check_rate_limit(self, request, client_ip):
        """Check if request is within rate limits"""
        # Determine endpoint type
        endpoint_type = 'default'
        for endpoint in self.rate_limits.keys():
            if endpoint != 'default' and endpoint in request.path:
                endpoint_type = endpoint
                break
        
        # Check minute-based rate limit
        minute_key = f"rate_limit:{client_ip}:{endpoint_type}:minute"
        minute_count = cache.get(minute_key, 0)
        minute_limit = self.rate_limits[endpoint_type]
        
        if minute_count >= minute_limit:
            return False
        
        # Check burst rate limit (10 seconds)
        burst_key = f"rate_limit:{client_ip}:{endpoint_type}:burst"
        burst_count = cache.get(burst_key, 0)
        burst_limit = self.burst_limits.get(endpoint_type, self.burst_limits['default'])
        
        if burst_count >= burst_limit:
            return False
        
        # Increment counters
        cache.set(minute_key, minute_count + 1, 60)  # 1 minute
        cache.set(burst_key, burst_count + 1, 10)    # 10 seconds
        
        return True


class SecurityHeadersMiddleware:
    """
    Add security headers to all responses
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Content Security Policy
        if not settings.DEBUG:
            csp_policy = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' data:; "
                "connect-src 'self'; "
                "frame-ancestors 'none'; "
                "base-uri 'self'; "
                "form-action 'self';"
            )
            response['Content-Security-Policy'] = csp_policy
        
        # HSTS header for HTTPS
        if request.is_secure():
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response


class FailedLoginTracker:
    """
    Track failed login attempts and implement temporary lockouts
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.max_attempts = 5
        self.lockout_duration = 900  # 15 minutes

    def __call__(self, request):
        response = self.get_response(request)
        
        # Track failed login attempts
        if request.path == '/api/login/' and request.method == 'POST':
            if response.status_code == 401:  # Unauthorized
                self.record_failed_attempt(request)
            elif response.status_code == 200:  # Success
                self.clear_failed_attempts(request)
        
        return response
    
    def record_failed_attempt(self, request):
        """Record a failed login attempt"""
        client_ip = self.get_client_ip(request)
        username = request.POST.get('username', 'unknown')
        
        # Track by IP
        ip_key = f"failed_login_ip:{client_ip}"
        ip_attempts = cache.get(ip_key, 0) + 1
        cache.set(ip_key, ip_attempts, self.lockout_duration)
        
        # Track by username
        user_key = f"failed_login_user:{username}"
        user_attempts = cache.get(user_key, 0) + 1
        cache.set(user_key, user_attempts, self.lockout_duration)
        
        # Log security event
        logger.warning(f"Failed login attempt from IP {client_ip} for user {username}")
        
        # Check if lockout threshold reached
        if ip_attempts >= self.max_attempts or user_attempts >= self.max_attempts:
            logger.critical(f"Account lockout triggered for IP {client_ip} / user {username}")
    
    def clear_failed_attempts(self, request):
        """Clear failed attempts on successful login"""
        client_ip = self.get_client_ip(request)
        username = request.POST.get('username', 'unknown')
        
        cache.delete(f"failed_login_ip:{client_ip}")
        cache.delete(f"failed_login_user:{username}")
    
    def get_client_ip(self, request):
        """Get the real client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def is_locked_out(self, request):
        """Check if IP or user is locked out"""
        client_ip = self.get_client_ip(request)
        username = request.POST.get('username', 'unknown')
        
        ip_attempts = cache.get(f"failed_login_ip:{client_ip}", 0)
        user_attempts = cache.get(f"failed_login_user:{username}", 0)
        
        return ip_attempts >= self.max_attempts or user_attempts >= self.max_attempts
