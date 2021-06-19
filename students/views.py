from django.shortcuts import render

# Create your views here.
from collections import OrderedDict

from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.shortcuts import render


from .models import User
from courses.models import Course
from courses.views import calculate_score


User = get_user_model()


def get_all_scores_for_user(user):
    scores = []
    for course in Course.objects.all():
        course_scores = []
        for section in course.section_set.order_by('number'):
            course_scores.append((section, calculate_score(user, section),))
        scores.append((course, course_scores),)
    return scores


def student_detail(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    student = request.user
    return render(request, 'students/student_details.html', {
        'scores': get_all_scores_for_user(student),
        'student': student,
    })

