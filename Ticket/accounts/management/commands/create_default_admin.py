from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Creates a default admin user if one does not exist'

    def handle(self, *args, **options):
        User = get_user_model()
        email = os.getenv('DEFAULT_ADMIN_EMAIL', 'admin@example.com')
        password = os.getenv('DEFAULT_ADMIN_PASSWORD', 'admin')
        
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email=email,
                password=password
            )
            admin_user.role = User.Role.ADMIN
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully created admin user: {email}'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists.'))
