from django.urls import path
from .views import GGSearchAPIView, GGSRStructure, GKeySearchAPIView, TestGGSearch, CheckQclusterStatus

# /gg-crawl/
urlpatterns = [
    path('check-task/', CheckQclusterStatus.as_view()),
    path('gg-crawl/', GGSearchAPIView.as_view()),
    path('ggsr-structure/', GGSRStructure.as_view()),
    path('g-key-search/', GKeySearchAPIView.as_view()),
    path('test-gg-search/', TestGGSearch.as_view())
]