from django.shortcuts import render
from datetime import datetime

# Create your views here.
def add_common_context(context=None):
    if context is None:
        context = {}
    context['current_year'] = datetime.now().year

    return context

def home(request):
    current_hour = datetime.now().hour - 5

    if current_hour < 12:
        greeting = "Good Morning!"
    elif 12 <= current_hour <= 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    context = add_common_context({
        'greeting': greeting,
        'page_heading': 'Welcome to My Website',
    })
    return render(request, 'pages/home.html', context)


def about(request):
    context = add_common_context()
    return render(request, 'pages/about.html', context)

def contact(request):
    context = add_common_context()
    return render(request, 'pages/contact.html', context)