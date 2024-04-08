from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import pytz

class Quiz(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration_minutes = models.PositiveIntegerField()
    quiz_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Get the timezone object for Asia/Kolkata
        desired_timezone = pytz.timezone('Asia/Kolkata')

        # Convert the datetime to the desired timezone
        self.quiz_date = timezone.localtime(self.quiz_date, timezone=desired_timezone)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.PositiveIntegerField(default=0)


class QuestionAttempt(models.Model):
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    marks_obtained = models.PositiveIntegerField(null=True, blank=True)

