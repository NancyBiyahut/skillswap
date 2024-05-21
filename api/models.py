from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , null = False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Educator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , null = False)
    name = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag)
    description = models.TextField()
    charges = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class Session(models.Model):
    DURATION_CHOICES = [
        ('15', '15 minutes'),
        ('30', '30 minutes'),
        ('60', '1 hour'),
        ('120', '2 hours'),
    ]
    SESSION_STATUS_CHOICES = [
        ('sent', 'Sent Request'),
        ('accepted', 'Accepted Request'),
        ('canceled', 'Canceled Request'),
        ('completed' , 'Session Completed'),
        ('scheduled' , 'Session Scheduled'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    ]
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    educator = models.ForeignKey(Educator, on_delete=models.CASCADE)
    duration = models.CharField(max_length=3, choices=DURATION_CHOICES)
    tags = models.ManyToManyField(Tag)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    problem_description = models.TextField()
    session_status = models.CharField(max_length=10, choices=SESSION_STATUS_CHOICES, default='sent')
    payment_status = models.CharField(max_length=8, choices=PAYMENT_STATUS_CHOICES, default='pending')
    def __str__(self):
        return f"{self.educator.name} - {self.session_status}"

class Review(models.Model):
    desc = models.TextField()
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    educator = models.ForeignKey(Educator, on_delete=models.CASCADE)
    session= models.ForeignKey(Session , on_delete=models.CASCADE)
    def __str__(self):
        return self.learner
    def __str__(self):
        return f"Review by {self.learner.name} for {self.session}"