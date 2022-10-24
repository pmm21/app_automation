from django.test import TestCase

# Create your tests here.
urlpatterns = [
    path('test/', TestView.as_view()),
]
