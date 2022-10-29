from django.urls import path
from .views import GGSearchAPIView, GGSRStructure,  Test

urlpatterns = [
    path('gg-crawl/', GGSearchAPIView.as_view()),
    path('ggsr-structure/', GGSRStructure.as_view()),
    path('test/', Test.as_view()),
]