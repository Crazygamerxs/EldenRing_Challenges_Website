from django.core.management.base import BaseCommand
from api.models import User

class Command(BaseCommand):
    help = 'Make a user an admin (staff and superuser)'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to make admin')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
            
            # Show current status
            self.stdout.write(f"Current status for user '{username}':")
            self.stdout.write(f"  - is_staff: {user.is_staff}")
            self.stdout.write(f"  - is_superuser: {user.is_superuser}")
            self.stdout.write(f"  - is_active: {user.is_active}")
            
            # Make user admin
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f"Successfully made '{username}' an admin!")
            )
            
            # Show new status
            self.stdout.write(f"New status for user '{username}':")
            self.stdout.write(f"  - is_staff: {user.is_staff}")
            self.stdout.write(f"  - is_superuser: {user.is_superuser}")
            self.stdout.write(f"  - is_active: {user.is_active}")
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"User '{username}' does not exist!")
            )
            
            # Show all users
            self.stdout.write("\nAvailable users:")
            for user in User.objects.all():
                self.stdout.write(f"  - {user.username} (staff: {user.is_staff}, superuser: {user.is_superuser})")
