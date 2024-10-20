from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Reward

@receiver(post_migrate)
def create_default_rewards(sender, **kwargs):
    if sender.name == 'KartKat':  # Replace 'kartkat' with your app name
        Reward.objects.get_or_create(name='Calcium Champion', description='Unlocked for buying items with high calcium content.')
        Reward.objects.get_or_create(name='Healthy Shopper', description='Unlocked for buying fresh produce.')
        Reward.objects.get_or_create(name='Seafood Lover', description='Unlocked for buying seafood.')
        Reward.objects.get_or_create(name="Supporter of Women's Business", description='Unlocked for buying items from women-owned businesses.')
        # Add more rewards as needed