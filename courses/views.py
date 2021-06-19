from django.shortcuts import render,redirect
from . models import Course, Question, Section, UserAnswer
from django.http import HttpResponseRedirect
from django.db import models, transaction
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.views.generic import ListView,DetailView,CreateView
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .forms import CourseForm
from .serializers import SectionSerializer
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.

"""def course_detail(request,course_id):
    course=Course.objects.get(id=course_id)
    return render (request,'courses/course_details.html',{'course':course})"""


class CourseDetailView(DetailView):
    model = Course
course_detail=CourseDetailView.as_view()


class CourseListView(ListView):
    model = Course
    queryset=Course.objects.all()
course_list=CourseListView.as_view()


def course_add(request):
    if request.POST:
        form = CourseForm(request.POST)
        if form.is_valid():
            new_course = form.save()
            return HttpResponseRedirect(new_course.get_absolute_url())
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {
        'form': form,
    })

class CourseAddView(CreateView):
    model=Course
    fields='__all__'
course_add=CourseAddView.as_view()



def do_section(request, section_id):
    section = Section.objects.get(id=section_id)
    return render(request, 'courses/do_section.html', {
        'section': section,
    })


def do_test(request, section_id):
    if not request.user.is_authenticated:
        raise PermissionDenied
    section = Section.objects.get(id=section_id)
    if request.method == 'POST':
        data = {}
        for key, value in request.POST.items():
            if key == 'csrfmiddlewaretoken':
                continue
            # {'question-1': '2'}
            question_id = key.split('-')[1]
            answer_id = request.POST.get(key)
            data[question_id] = answer_id
        perform_test(request.user, data, section)
        return redirect(reverse('show_results', args=(section.id,)))
    return render(request, 'courses/do_test.html', {
        'section': section,
    })


def perform_test(user, data, section):
    with transaction.atomic():
        UserAnswer.objects.filter(user=user,
                                  question__section=section).delete()
        for question_id, answers_id in data.items():
            question = Question.objects.get(id=question_id)
            answers_id = int(answers_id)
            if answers_id not in question.answers_set.values_list('id', flat=True):
                raise SuspiciousOperation('Answer is not valid for this question')
            user_answer = UserAnswer.objects.create(
                user=user,
                question=question,
                answers_id=answers_id,
            )


def calculate_score(user, section):
    questions = Question.objects.filter(section=section)
    correct_answers = UserAnswer.objects.filter(
        user=user,
        question__section=section,
        answers__correct=True
    )
    return (correct_answers.count() / questions.count()) * 100


def show_results(request, section_id):
    if not request.user.is_authenticated:
        raise PermissionDenied
    section = Section.objects.get(id=section_id)
    return render(request, 'courses/show_results.html', {
        'section': section,
        'score': calculate_score(request.user, section)
    })


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    @action(detail=True, methods=['GET'])
    def questions(self, request, *args, **kwargs):
        section = self.get_object()
        data = []
        for question in section.question_set.all():
            question_data = {'id': question.id, 'answers': []}
            for answers in question.answers_set.all():
                answers_data = {'id': answers.id, 'text': str(answers), }
                question_data['answers'].append(answers_data)
            data.append(question_data)
        return Response(data)

    @action(detail=True, methods=['PUT'])
    def test(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        section = self.get_object()
        perform_test(request.user, request.data, section)
        return Response()

    @action(detail=True, methods=['GET'])
    def result(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        return Response({
            'score': calculate_score(request.user, self.get_object())
        })
