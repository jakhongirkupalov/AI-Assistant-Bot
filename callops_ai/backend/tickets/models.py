from django.db import models

class Ticket(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("ai_answered", "AI Answered"),
        ("answered", "Answered by Operator"),
    ]

    user_id = models.CharField(max_length=50)
    message = models.TextField()              # 👤 User savoli

    ai_answer = models.TextField(blank=True)  # 🤖 AI javobi
    operator_reply = models.TextField(blank=True)  # 🧑‍💼 Operator javobi

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new"
    )
    answer = models.TextField(blank=True, null=True)


    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket #{self.id} | {self.status}"
