import os
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from datetime import datetime
from django.db import IntegrityError
from django.http import HttpResponse
from django.db.models import Sum
from django.http import HttpResponse
from django.contrib.auth import logout
from django.views import generic, View
from datetime import datetime


def index(request):
    return render(request, "index.html")

def map(request):
    key = os.environ.get('API_KEY')
    context = {
        'key': key,
    }
    return render(request, 'map.html', context)
