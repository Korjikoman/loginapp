from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import TextFromAudio


@receiver(signal=post_save, sender=TextFromAudio)
def text_created(sender, instance, created,**kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'transcriptions',
            {
                "type": "send_transcription",
                "message": instance.text
            }
        )