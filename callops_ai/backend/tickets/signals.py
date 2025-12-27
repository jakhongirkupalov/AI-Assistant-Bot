from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ticket
from bot.telegram_sender import send_telegram_message


@receiver(post_save, sender=Ticket)
def ticket_post_save_handler(sender, instance, created, **kwargs):
    # Yangi ticket bo‘lsa – hech narsa qilmaymiz
    if created:
        return

    # Operator javob berganda
    if instance.status == "answered" and instance.answer:
        send_telegram_message(
            user_id=instance.user_id,
            text=f"📩 Operator javobi:\n\n{instance.answer}"
        )

    # Ticket yopilganda
    elif instance.status == "closed":
        send_telegram_message(
            user_id=instance.user_id,
            text="🔒 Sizning murojaatingiz yopildi.\nAgar yana savol bo‘lsa, yozishingiz mumkin 😊"
        )
