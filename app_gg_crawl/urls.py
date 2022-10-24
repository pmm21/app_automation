from django.urls import path
from .views import GGSearchAPIView

urlpatterns = [
    path('gg-crawl/', GGSearchAPIView.as_view()),
]