from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Users

@receiver(post_migrate)
def create_admin_user(sender, **kwargs):
    if sender.name == 'app':
        Users.objects.get_or_create(
            login='admin',
            defaults={
                'name': 'Admin',
                'admin': True,
                'password': '1',
            }
        )
