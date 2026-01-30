from django.db import models
from accounts.models import User

class Resume(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='resumes'
    )
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Education(models.Model):
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='educations'
    )
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=150)
    start_year = models.IntegerField()
    end_year = models.IntegerField(null=True, blank=True)
    order = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

class Experience(models.Model):
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='experiences'
    )
    company = models.CharField(max_length=150)
    role = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    order = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

class Skill(models.Model):
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='skills'
    )
    name = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    
class Project(models.Model):
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    title = models.CharField(max_length=150)
    description = models.TextField()
    tech_stack = models.CharField(max_length=200)
    project_link = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']
    