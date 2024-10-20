from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Reward

@receiver(post_migrate)
def create_default_rewards(sender, **kwargs):
    if sender.name == 'KartKat':  # Replace 'kartkat' with your app name
        Reward.objects.get_or_create(name='Calcium Champion', description='Unlocked for buying items with high calcium content.', link="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGFnZWVkZnltaTlubDE4ZjBnaHdkeTVicWg2aG5sNnJmZDBxMjBlMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/2IAL5pvqPY8tr5lYqT/giphy.gif")
        Reward.objects.get_or_create(name='Healthy Shopper', description='Unlocked for buying fresh produce.', link="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExajlsdGRwb3RoODhzcjg1NGpmNHl2N3d2aWVoaG44OGRsM3BmaTFicCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/S6R9nYaxk2TDfgB6Ad/giphy.gif")
        Reward.objects.get_or_create(name='Seafood Lover', description='Unlocked for buying seafood.', link="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExaWJrMDU2dndscTE5aG9ueDA4a2Nmbnl3dHl0ZnZ0MHhud3JkMGc5dSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/UCSTEVX8GGCYlFp0ld/giphy.gif")
        Reward.objects.get_or_create(name="Supporter of Women's Business", description='Unlocked for buying items from women-owned businesses.', link="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZWh2MmV0aG5tb242bWE4NDNwdjgyaG94bmxrMTBpaHdteHA1ZWRxYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/4ZxTQzEK1ORUpuLzFz/giphy.gif")
        # Add more rewards as needed