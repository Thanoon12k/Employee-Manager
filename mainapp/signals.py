from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Answer, AnswerStatistics

@receiver(post_save, sender=Answer)
def update_statistics(sender, instance, **kwargs):
    question = instance.question
    stats, created = AnswerStatistics.objects.get_or_create(question=question)
    stats.calculate_percentages()
