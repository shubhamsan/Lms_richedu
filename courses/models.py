from django.conf import settings
from django.db import models
from students.models import User
from django.urls import reverse
# Create your models here.


class Course(models.Model):
    name=models.CharField(max_length=300)
    student=models.ManyToManyField(User)
    def get_absolute_url(self):
        #return reverse('course_detail', args=(self.id, ))
        return f"/courses/course_detail/{self.id}/"

    def __str__(self):
        return self.name


class Section(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    number=models.IntegerField()
    text=models.TextField()

    class Meta:
        unique_together=('course','number', )
    
    def get_test_url(self):
        return reverse('do_test',  args=(self.id,))

    def get_absolute_url(self):
        return reverse('do_section', args=(self.id, ))

    def get_next_section_url(self):
        next_section = Section.objects.get(number=self.number+1)
        return reverse('do_section', args=(next_section.id,))

    def __str__(self):
        return self.title

class Question(models.Model):
    section=models.ForeignKey(Section, on_delete=models.CASCADE)
    text=models.TextField(max_length=500)

    def __str__(self):
        return self.text

class Answers(models.Model):
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    text=models.TextField(max_length=1000)
    correct=models.BooleanField()

    def __str__(self):
        return self.text

class UserAnswer(models.Model):
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    answers=models.ForeignKey(Answers, on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    class Meta:
        unique_together=('question','user', )

    def __str__(self):
        return self.text


