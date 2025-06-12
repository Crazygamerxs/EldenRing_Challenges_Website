# mybackend/api/validators.py
import re
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from urllib.parse import urlparse
import html

def validate_username(username):
    """Validate username format and content"""
    if not username:
        raise ValidationError("Username is required")
    
    if len(username) < 3 or len(username) > 30:
        raise ValidationError("Username must be between 3 and 30 characters")
    
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        raise ValidationError("Username can only contain letters, numbers, underscores, and hyphens")
    
    # Block common admin usernames
    blocked_usernames = [
        'admin', 'administrator', 'root', 'system', 'api', 'www', 'mail',
        'email', 'user', 'test', 'guest', 'demo', 'support', 'help',
        'moderator', 'mod', 'owner', 'superuser', 'staff'
    ]
    if username.lower() in blocked_usernames:
        raise ValidationError("This username is not allowed")
    
    return username

def validate_submission_url(url):
    """Validate submission URL for safety"""
    if not url:
        raise ValidationError("URL is required")
    
    # Basic URL validation
    url_validator = URLValidator()
    try:
        url_validator(url)
    except ValidationError:
        raise ValidationError("Invalid URL format")
    
    # Parse URL
    try:
        parsed = urlparse(url)
    except Exception:
        raise ValidationError("Invalid URL format")
    
    # Check protocol
    if parsed.scheme.lower() not in ['http', 'https']:
        raise ValidationError("URL must use HTTP or HTTPS protocol")
    
    # Check if it's a safe domain
    allowed_domains = [
        'youtube.com', 'www.youtube.com', 'youtu.be', 'm.youtube.com',
        'twitch.tv', 'www.twitch.tv', 'clips.twitch.tv',
        'drive.google.com', 'docs.google.com',
        'vimeo.com', 'www.vimeo.com', 'player.vimeo.com',
        'streamable.com', 'www.streamable.com',
        'imgur.com', 'i.imgur.com',
        'dropbox.com', 'www.dropbox.com'
    ]
    
    if parsed.netloc.lower() not in allowed_domains:
        raise ValidationError("URL must be from an approved video hosting platform")
    
    # Block suspicious patterns in URL
    suspicious_patterns = [
        r'javascript:', r'data:', r'file:', r'ftp:', r'blob:',
        r'<script', r'</script', r'onclick', r'onerror', r'onload',
        r'%3Cscript', r'%3C/script', r'&lt;script', r'&gt;'
    ]
    
    url_lower = url.lower()
    for pattern in suspicious_patterns:
        if re.search(pattern, url_lower):
            raise ValidationError("URL contains suspicious content")
    
    return url

def validate_time_format(time_string):
    """Validate time format (HH:MM:SS)"""
    if not time_string:
        raise ValidationError("Time is required")
    
    if not re.match(r'^\d{2}:\d{2}:\d{2}$', time_string):
        raise ValidationError("Time must be in HH:MM:SS format")
    
    try:
        hours, minutes, seconds = map(int, time_string.split(':'))
        if hours < 0 or hours > 23 or minutes < 0 or minutes >= 60 or seconds < 0 or seconds >= 60:
            raise ValidationError("Invalid time values")
        
        # Check for reasonable maximum time (24 hours)
        total_seconds = hours * 3600 + minutes * 60 + seconds
        if total_seconds > 86400:  # 24 hours
            raise ValidationError("Time cannot exceed 24 hours")
            
    except ValueError:
        raise ValidationError("Invalid time format")
    
    return time_string

def sanitize_text_input(text):
    """Sanitize text input to prevent XSS"""
    if not text:
        return text
    
    # HTML escape the input
    text = html.escape(text)
    
    # Remove null bytes and control characters
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\t\n\r')
    
    # Limit length to prevent DoS
    if len(text) > 10000:
        text = text[:10000]
    
    return text.strip()

def validate_email_format(email):
    """Enhanced email validation"""
    if not email:
        raise ValidationError("Email is required")
    
    # Basic format check
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise ValidationError("Invalid email format")
    
    # Check length
    if len(email) > 254:
        raise ValidationError("Email address too long")
    
    # Split local and domain parts
    try:
        local, domain = email.rsplit('@', 1)
    except ValueError:
        raise ValidationError("Invalid email format")
    
    # Validate local part
    if len(local) > 64:
        raise ValidationError("Email local part too long")
    
    # Validate domain part
    if len(domain) > 253:
        raise ValidationError("Email domain too long")
    
    # Block temporary email domains (optional - you can remove this if needed)
    blocked_domains = [
        '10minutemail.com', 'tempmail.org', 'guerrillamail.com',
        'mailinator.com', 'throwaway.email', 'temp-mail.org',
        'yopmail.com', 'maildrop.cc', '33mail.com'
    ]
    
    if domain.lower() in blocked_domains:
        raise ValidationError("Temporary email addresses are not allowed")
    
    return email.lower()

def validate_challenge_data(name, details):
    """Validate challenge creation data"""
    if not name or not details:
        raise ValidationError("Name and details are required")
    
    # Sanitize inputs
    name = sanitize_text_input(name)
    details = sanitize_text_input(details)
    
    # Check lengths
    if len(name) < 5 or len(name) > 255:
        raise ValidationError("Challenge name must be between 5 and 255 characters")
    
    if len(details) < 10 or len(details) > 2000:
        raise ValidationError("Challenge details must be between 10 and 2000 characters")
    
    return name, details

def validate_rejection_reason(reason):
    """Validate admin rejection reason"""
    if not reason:
        raise ValidationError("Rejection reason is required")
    
    reason = sanitize_text_input(reason)
    
    if len(reason) < 10:
        raise ValidationError("Rejection reason must be at least 10 characters")
    
    if len(reason) > 500:
        raise ValidationError("Rejection reason cannot exceed 500 characters")
    
    return reason