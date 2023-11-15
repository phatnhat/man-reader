from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Chapter
from accounts.models import Notification, UserReading, User

@receiver(post_save, sender=Chapter)
def post_save_create_chapter_receiver(sender, instance, created, **kwargs):
    if created:
        user_reading = UserReading.objects.filter(book=instance.book).all()
        if user_reading:
            users = User.objects.filter(users_reading__in=user_reading).all()
            notifications = [Notification(user=user, chapter=instance) for user in users]
            Notification.objects.bulk_create(notifications)
