from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator

class Question(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.CharField(max_length=200, blank=True)
	datetime = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
		return self.question

class Solutions(models.Model):
	answer = models.CharField(max_length = 400, blank = True)
	datetime = models.DateTimeField(auto_now_add=True, blank=True)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	upvotes = models.IntegerField(blank = True)

	def __str__(self):
		return "By {} on {} as {}".format(self.author, self.question, self.answer)

	def get_comments(self):
		q = Comment.objects.filter(answer=self)
		return q
		
	class Meta:
		verbose_name_plural = 'Solutions'

class Upvote(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	answer = models.ForeignKey(Solutions, on_delete=models.CASCADE)

class Comment(models.Model):
	answer = models.ForeignKey(Solutions, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	datetime = models.DateTimeField(auto_now_add=True, blank=True)
	comment = models.TextField()

	def __str__(self):
		return "By {} on '{}' as {}".format(self.author, self.answer, self.comment)

		