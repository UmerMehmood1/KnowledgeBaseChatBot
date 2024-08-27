# llm_app/views.py

from django.shortcuts import render

def query_form(request):
    return render(request, 'query_form.html')


 