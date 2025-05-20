from django.db import models

class Reviewer(models.Model):
    name      = models.CharField(max_length=150)
    email     = models.EmailField(unique=True)
    expertise = models.CharField(
        max_length=255,
        help_text="Comma-separated list of domains"
    )

    def __str__(self):
        return self.name

class Review(models.Model):
    assignment  = models.OneToOneField(
        'publications.ReviewAssignment',
        on_delete=models.CASCADE,
        related_name='review'
    )
    comments    = models.TextField()
    score       = models.IntegerField()
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.assignment.reviewer} on {self.assignment.publication}"
