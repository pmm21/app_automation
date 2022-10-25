from django.urls import path
from .views import GGSearchAPIView, Test

urlpatterns = [
    path('gg-crawl/', GGSearchAPIView.as_view()),
    path('test/', Test.as_view()),
]