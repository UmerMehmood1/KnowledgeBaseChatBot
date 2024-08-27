# llm_app/urls.py

from django.urls import path
from .views import query_form

urlpatterns = [
    path('', query_form, name='query_form'),
]
