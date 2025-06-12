# mybackend/api/middleware/security.py
import time
import logging
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import json

logger = logging.getLogger('django.security')

# Custom HTTP 429 response class since Django doesn't provide one
class HttpResponseTooManyRequests(HttpResponse):
    status_code = 429

class RateLimitMiddleware(MiddlewareMixin):
    """Rate limiting middleware to prevent abuse"""
    
    def process_request(self, request):
        # Skip rate limiting in development
        if getattr(settings, 'DEBUG', False):
            return None
            
        # Get client IP
        ip = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
        
        # Different limits for different endpoints
        if request.path.startswith('/api/login/'):
            return self.rate_limit(ip, 'login', max_requests=5, window=300, user_agent=user_agent)
        elif request.path.startswith('/api/signup/'):
            return self.rate_limit(ip, 'signup', max_requests=3, window=3600, user_agent=user_agent)
        elif request.path.startswith('/api/submit_run/'):
            return self.rate_limit(ip, 'submit', max_requests=10, window=3600, user_agent=user_agent)
        elif request.path.startswith('/api/password-reset/'):
            return self.rate_limit(ip, 'password_reset', max_requests=3, window=3600, user_agent=user_agent)
        elif request.path.startswith('/api/admin/'):
            return self.rate_limit(ip, 'admin', max_requests=100, window=3600, user_agent=user_agent)
        
        return None
    
    def get_client_ip(self, request):
        """Get the real client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        
        # Validate IP format
        import ipaddress
        try:
            ipaddress.ip_address(ip)
            return ip
        except ValueError:
            return '0.0.0.0'
    
    def rate_limit(self, ip, action, max_requests, window, user_agent):
        """Check and enforce rate limits"""
        cache_key = f'rate_limit_{action}_{ip}'
        current_time = time.time()
        
        try:
            # Get existing requests
            requests = cache.get(cache_key, [])
            
            # Remove old requests outside the window
            requests = [req_time for req_time in requests if current_time - req_time < window]
            
            # Check if limit exceeded
            if len(requests) >= max_requests:
                logger.warning(
                    f'Rate limit exceeded for {ip} on {action}. '
                    f'User-Agent: {user_agent[:100]}'
                )
                return JsonResponse({
                    'error': 'Rate limit exceeded. Please try again later.',
                    'retry_after': window
                }, status=429)
            
            # Add current request
            requests.append(current_time)
            cache.set(cache_key, requests, window)
            
        except Exception as e:
            logger.error(f'Rate limiting error: {e}')
            # Fail open - don't block if cache is down
            pass
        
        return None

class SecurityHeadersMiddleware(MiddlewareMixin):
    """Add security headers to all responses"""
    
    def process_response(self, request, response):
        # Security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = (
            'geolocation=(), microphone=(), camera=(), '
            'payment=(), usb=(), magnetometer=(), gyroscope=()'
        )
        
        # Content Security Policy
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com",
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
            "font-src 'self' https://fonts.gstatic.com",
            "img-src 'self' data: https:",
            "connect-src 'self'",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'"
        ]
        
        # Only add CSP to HTML responses
        if 'text/html' in response.get('Content-Type', ''):
            response['Content-Security-Policy'] = '; '.join(csp_directives)
        
        # Remove server information
        if 'Server' in response:
            del response['Server']
        
        return response

class AdminAccessMiddleware(MiddlewareMixin):
    """Log and monitor admin access attempts"""
    
    def process_request(self, request):
        # Monitor admin access
        if request.path.startswith('/admin/') or request.path.startswith('/api/admin/'):
            ip = self.get_client_ip(request)
            user = getattr(request, 'user', None)
            user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')[:200]
            
            # Log all admin access attempts
            if user and user.is_authenticated:
                if user.is_staff or user.is_superuser:
                    logger.info(
                        f'Admin access: {user.username} from {ip} to {request.path} '
                        f'User-Agent: {user_agent}'
                    )
                else:
                    logger.warning(
                        f'Unauthorized admin access attempt: {user.username} from {ip} '
                        f'to {request.path} User-Agent: {user_agent}'
                    )
            else:
                logger.warning(
                    f'Unauthenticated admin access attempt from {ip} to {request.path} '
                    f'User-Agent: {user_agent}'
                )
        
        return None
    
    def get_client_ip(self, request):
        """Get the real client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        return ip

class SecurityMonitoringMiddleware(MiddlewareMixin):
    """Monitor for suspicious activities"""
    
    def process_request(self, request):
        ip = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Check for suspicious patterns
        suspicious_patterns = [
            'sqlmap', 'nikto', 'nmap', 'masscan', 'zap',
            'burp', 'dirb', 'gobuster', 'wfuzz', 'hydra'
        ]
        
        for pattern in suspicious_patterns:
            if pattern.lower() in user_agent.lower():
                logger.warning(
                    f'Suspicious user agent detected from {ip}: {user_agent[:200]}'
                )
                break
        
        # Monitor for suspicious request patterns
        if request.method == 'POST':
            try:
                body = request.body.decode('utf-8')[:1000]  # First 1000 chars
                
                # Check for common attack patterns
                attack_patterns = [
                    '<script', 'javascript:', 'union select', 'drop table',
                    'insert into', 'update set', 'delete from', '../../',
                    'cmd.exe', '/bin/bash', 'eval(', 'base64_decode'
                ]
                
                for pattern in attack_patterns:
                    if pattern.lower() in body.lower():
                        logger.warning(
                            f'Suspicious POST content from {ip} to {request.path}: '
                            f'Pattern "{pattern}" detected'
                        )
                        break
                        
            except Exception:
                # Ignore decoding errors
                pass
        
        return None
    
    def get_client_ip(self, request):
        """Get the real client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        return ip
