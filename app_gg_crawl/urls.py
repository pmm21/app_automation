from django.urls import path
from .views import GGSearchAPIView, GGSRStructure,  Test,TestCallBack

urlpatterns = [
    path('gg-crawl/', GGSearchAPIView.as_view()),
    path('ggsr-structure/', GGSRStructure.as_view()),
    path('test/', TestCallBack.as_view()),
]