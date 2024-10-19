
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

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import ShoppingList, ShoppingListItem
from .forms import ShoppingListForm, ShoppingListItemForm
from openai import OpenAI


client = OpenAI(
    api_key = "key here"
)

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message},
                ]
            )
            chatbot_response = response.choices[0].message.content.strip()
            return JsonResponse({'response': chatbot_response})
        except Exception as e:
            return JsonResponse({'response': 'An error occurred'}, status=500)
    return JsonResponse({'response': 'Invalid request method'}, status=400)

def index(request):
    return render(request, 'index.html')

def shopping_list(request):
    form = ShoppingListForm()
    item_form = ShoppingListItemForm()

    if request.method == 'POST':
        if 'add_list' in request.POST:
            form = ShoppingListForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('index')
        elif 'add_item' in request.POST:
            list_id = request.POST.get('list_id')
            shopping_list = get_object_or_404(ShoppingList, id=list_id)
            item_form = ShoppingListItemForm(request.POST)
            if item_form.is_valid():
                item = item_form.save(commit=False)
                item.shopping_list = shopping_list
                item.save()
                return redirect('index')

    shopping_lists = ShoppingList.objects.all()
    context = {
        'shopping_lists': shopping_lists,
        'form': form,
        'item_form': item_form,
    }
    return render(request, 'index.html', context)

def delete_item(request, item_id):
    item = get_object_or_404(ShoppingListItem, id=item_id)
    item.delete()
    return redirect('index')

def delete_list(request, list_id):
    shopping_list = get_object_or_404(ShoppingList, id=list_id)
    shopping_list.delete()
    return redirect('index')

def map(request):
    key = os.environ.get('API_KEY')
    context = {
        'key': key,
    }
    return render(request, 'map.html', context)