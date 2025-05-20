from django.db import models
from django.conf import settings

class Publication(models.Model):
    title = models.CharField(max_length=255)
    abstract = models.TextField(blank=True)
    authors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='publications'
    )
    published_date = models.DateField()
    # reviewers assigned via a through-model:
    reviewers = models.ManyToManyField(
        'reviewers.Reviewer',
        through='ReviewAssignment',
        related_name='assigned_publications'
    )

    def __str__(self):
        return self.title

class ReviewAssignment(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('in_review', 'In Review'),
        ('completed', 'Completed'),
    ]
    publication   = models.ForeignKey(Publication, on_delete=models.CASCADE)
    reviewer      = models.ForeignKey('reviewers.Reviewer', on_delete=models.CASCADE)
    assigned_at   = models.DateTimeField(auto_now_add=True)
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('publication', 'reviewer')

    def __str__(self):
        return f"{self.reviewer} → {self.publication} ({self.status})"