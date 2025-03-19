import os
import django
import sys

# Set up Django environment
sys.path.append('mybackend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mybackend.settings')
django.setup()

from api.models import User

def create_admin_user(username, email, password):
    """Create an admin user if it doesn't exist."""
    try:
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            user.save()
            print(f"Updated existing user '{username}' to admin status.")
        else:
            # Create new admin user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                profile_image=None
            )
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print(f"Created new admin user '{username}'.")
        
        print(f"\nAdmin Login Details:")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"\nYou can now log in as an admin using these credentials.")
        
    except Exception as e:
        print(f"Error creating admin user: {str(e)}")

if __name__ == "__main__":
    username = input("Enter admin username: ")
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    
    create_admin_user(username, email, password)
