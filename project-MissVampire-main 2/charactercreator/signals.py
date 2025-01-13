import os

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Character


@receiver(post_delete, sender=Character)
def delete_image_on_model_delete(sender, instance, **kwargs):
    """Delete the image file when the model instance is deleted."""
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)


@receiver(pre_save, sender=Character)
def delete_image_on_model_update(sender, instance, **kwargs):
    """Delete the old image file when the image is updated."""
    if not instance.pk:
        return  # Skip if the instance is being created

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    # If a new image is being uploaded, delete the old one
    if old_instance.image and old_instance.image != instance.image:
        if os.path.isfile(old_instance.image.path):
            os.remove(old_instance.image.path)
