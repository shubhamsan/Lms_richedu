from django.contrib import admin
from .models import Course, Section, Question, Answers


class CourseAdmin(admin.ModelAdmin):
    pass


admin.site.register(Course, CourseAdmin)


class SectionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Section, SectionAdmin)


class QuestionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Question, QuestionAdmin)


class AnswerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Answers, AnswerAdmin)
