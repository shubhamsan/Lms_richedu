from rest_framework import routers
from .views import UserViewSet
from courses.views import SectionViewSet

from django.urls import path,include
from django.conf.urls import url


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'sections', SectionViewSet)

urlpatterns = [
    url(r'^api/',include(router.urls))
]
