from django.urls import path,include
from django.conf.urls import url


from . import views
from courses.views import course_add,course_list,course_detail,do_section,do_test,show_results
urlpatterns = [
    url(r'^course_detail/(?P<pk>\d)/$', course_detail),
    url(r'^$', course_list),
    url(r'^course_add/$', course_add, name='course_add'),
    url(r'^section/(?P<section_id>\d+)/$', do_section, name='do_section'),
    url(r'^section/(?P<section_id>\d+)/test/$', do_test, name='do_test'),
    url(r'^section/(?P<section_id>\d+)/results/$', show_results, name='show_results'),

]