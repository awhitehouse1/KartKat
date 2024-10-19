
import os
import json
#from django.db.models.fields import json
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
from .models import ShoppingList, ShoppingListItem, Recipe
from .forms import ShoppingListForm, ShoppingListItemForm
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


client = OpenAI(
    api_key = os.getenv('OPEN_API_KEY')
)

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. You can answer questions about recipes, shopping lists, and saving money. You are a feminist. Your name is Kat and you are a cat assistant. Make cat puns and meow occaisionally. make the responses concise, but be a girl boss. Do not use markup. When the user asks for recipes, return in this format: 'Here is a recipe for [recipe name]' give each ingredient a new line using the '\\n' char, then list the steps with numbers on their own line."},
                    {"role": "user", "content": message},
                ]
            )
            chatbot_response = response.choices[0].message.content.strip()
            is_recipe = "Here is a recipe for" in chatbot_response
            return JsonResponse({'response': chatbot_response, 'is_recipe': is_recipe})
        except Exception as e:
            return JsonResponse({'response': 'An error occurred'}, status=500)
    return JsonResponse({'response': 'Invalid request method'}, status=400)

def index(request):
    return render(request, 'index.html')

def save_recipe(request):
    if request.method == 'POST':
        recipe_name = request.POST.get('recipe_name')
        ingredients = request.POST.get('ingredients')
        steps = request.POST.get('steps')
    
        Recipe.objects.create(name=recipe_name, ingredients=ingredients, steps=steps)
        return JsonResponse({'status': 'Recipe saved successfully'})
    return JsonResponse({'status': 'Invalid request method'}, status=400)

@csrf_exempt
def delete_recipe(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        recipe.delete()
        return JsonResponse({'status': 'Recipe deleted successfully'})
    return JsonResponse({'status': 'Invalid request method'}, status=400)

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe_list.html', {'recipes': recipes})


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

def logout_view(request):
    logout(request)
    return redirect('index')


def rewards(request):
    return render(request, 'rewards.html')


@csrf_exempt
def delete_crossed_off_items(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))  # decode the bytes to string
        for item in data["items"]:
            list_id = item['listId']
            item_id = item['itemId']
            ShoppingListItem.objects.filter(id=item_id, shopping_list_id=list_id).delete()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
