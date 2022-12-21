from django.urls import path
from .views import TestView, CPUInfoView

urlpatterns = [
    path('test/', TestView.as_view()),
    path('cpu-info/', CPUInfoView),
    # path('cpu-info-activate/', cpuinfoviewactivate),
]
