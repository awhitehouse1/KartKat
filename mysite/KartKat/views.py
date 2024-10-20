
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
from .models import ShoppingList, ShoppingListItem, Recipe, GroceryItem, Reward
from .forms import ShoppingListForm, ShoppingListItemForm
from openai import OpenAI
from dotenv import load_dotenv
from fuzzywuzzy import process

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ShoppingListForm, ShoppingListItemForm
from .models import ShoppingList
load_dotenv()


client = OpenAI(
    api_key = os.getenv('OPEN_API_KEY')
)

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        try:
            chatbot_response = ""

            # Check if the user is asking for shopping lists
            if "shopping list" in message.lower():
                shopping_lists = ShoppingList.objects.all()
                
                # If user is asking for items from a specific list
                if "items in" in message.lower():
                    list_name = message.lower().replace("shopping list items in", "").strip()
                    try:
                        shopping_list = ShoppingList.objects.get(name__iexact=list_name)
                        items = shopping_list.items.all()
                        if items.exists():
                            item_names = [item.name for item in items]
                            # Append items with commas and 'and' before the last item
                            if len(item_names) == 1:
                                item_str = item_names[0]
                            elif len(item_names) == 2:
                                item_str = " and ".join(item_names)
                            else:
                                item_str = ", ".join(item_names[:-1]) + ", and " + item_names[-1]
                            chatbot_response = f"The items in {shopping_list.name} {item_str}"
                        else:
                            chatbot_response = f"The shopping list '{shopping_list.name}' has no items yet."
                    except ShoppingList.DoesNotExist:
                        chatbot_response = f"I couldn't find a shopping list named '{list_name}'."

                # Check if the user is asking for recipes based on a specific shopping list
                elif "recipe" in message.lower() and "from shopping list" in message.lower():
                    list_name = message.lower().replace("recipe from shopping list", "").strip()
                    try:
                        shopping_list = ShoppingList.objects.get(name__iexact=list_name)
                        items = shopping_list.items.all()
                        if items.exists():
                            # Collect item names for recipe suggestion
                            item_names = [item.name for item in items]
                            item_str = ", ".join(item_names[:-1]) + ", and " + item_names[-1] if len(item_names) > 1 else item_names[0]
                            
                            # Call OpenAI API to generate a recipe using the items
                            response = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {"role": "system", "content": "You are a helpful assistant that provides recipes based on given ingredients. Aim to use all or most of the provided ingredients in your recipe. You are a feminist. Your name is Kat and you are a cat assistant. Make cat puns and meow occasionally. Make the responses concise, but be a girl boss. Do not use markup. When the user asks for recipes, return in this format: 'Here is a recipe for [recipe name]' give each ingredient a new line using the '\\n' char, then list the steps with numbers on their own line."},
                                    {"role": "user", "content": f"Can you give me a recipe that uses the following ingredients: {item_str}?"},
                                ]
                            )
                            recipe_response = response.choices[0].message.content.strip()
                            chatbot_response = f"{recipe_response}"
                        else:
                            chatbot_response = f"The shopping list '{shopping_list.name}' has no items, so I can't suggest any recipes."
                    except ShoppingList.DoesNotExist:
                        chatbot_response = f"I couldn't find a shopping list named '{list_name}'."

                # User just asked for shopping lists
                elif shopping_lists.exists():
                    shopping_list_names = [shopping_list.name for shopping_list in shopping_lists]
                    # Append shopping list names with commas and 'and' before the last item
                    if len(shopping_list_names) == 1:
                        shopping_list_str = shopping_list_names[0]
                    elif len(shopping_list_names) == 2:
                        shopping_list_str = " and ".join(shopping_list_names)
                    else:
                        shopping_list_str = ", ".join(shopping_list_names[:-1]) + ", and " + shopping_list_names[-1]
                    
                    chatbot_response = f"You have shopping lists called {shopping_list_str}. Would you like to see the items for any specific list?"
                else:
                    chatbot_response = "You don't have any shopping lists right now. Try creating one!"

            # Handle other chatbot interactions
            else:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant. You can answer questions about recipes, shopping lists, and saving money. You are a feminist. Your name is Kat and you are a cat assistant. Make cat puns and meow occasionally. Make the responses concise, but be a girl boss. Do not use markup. When the user asks for recipes, return in this format: 'Here is a recipe for [recipe name]' give each ingredient a new line using the '\\n' char, then list the steps with numbers on their own line."},
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
    print("here")

    if request.method == 'POST':
        print("request", request.POST)
        # Adding a new shopping list
        if 'add_list' in request.POST:
            form = ShoppingListForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('index')

        # Adding a new item to an existing shopping list
        else:
            
            list_id = request.POST.get('list_id')
            shopping_list = get_object_or_404(ShoppingList, id=list_id)
            item_form = ShoppingListItemForm(request.POST)
            if item_form.is_valid():
                item = item_form.save(commit=False)
                item.shopping_list = shopping_list
                item.save()

                # If the request is AJAX, return JSON response
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'item': {
                            'id': item.id,
                            'name': item.name,
                        }
                    })

                # If not an AJAX request, redirect to index
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
    unlocked_rewards = Reward.objects.filter(unlocked=True)
    return render(request, 'rewards.html', {'unlocked_rewards': unlocked_rewards})


@csrf_exempt
def delete_crossed_off_items(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))  # decode the bytes to string
        for item in data["items"]:
            list_id = item['listId']
            item_id = item['itemId']
            shopping_list_item = get_object_or_404(ShoppingListItem, id=item_id, shopping_list_id=list_id)
            ShoppingListItem.objects.filter(id=item_id, shopping_list_id=list_id).delete()
            grocery_items = GroceryItem.objects.all()
            grocery_item_names = [grocery_item.name for grocery_item in grocery_items]
            closest_match, score = process.extractOne(shopping_list_item.name, grocery_item_names)
            if score >= 80:  # Example threshold for a good match
                rewards = Reward.objects.all()
                grocery_item = get_object_or_404(GroceryItem, name=closest_match)
                ShoppingListItem.objects.filter(id=item_id, shopping_list_id=list_id).delete()
                print("grocery item", grocery_item)
            grocery_items = GroceryItem.objects.all()
            grocery_item_names = [grocery_item.name for grocery_item in grocery_items]
            closest_match, score = process.extractOne(shopping_list_item.name, grocery_item_names)

            if score >= 80:  # Example threshold for a good match
                rewards = Reward.objects.all()

                grocery_item = get_object_or_404(GroceryItem, name=closest_match)
                print("grocery item", grocery_item)

                # Check the calcium content
                if grocery_item.calcium > 260:  # Example threshold
                    # Perform some action if the calcium content is above the threshold
                    print(f"Item {grocery_item.name} has high calcium content: {grocery_item.calcium}mg")
                    rewards.filter(name="Calcium Champion").update(unlocked=True)
                elif grocery_item.is_woman_owned:
                    print("women owned")
                    rewards.filter(name="Supporter of Women's Business").update(unlocked=True)
                elif grocery_item.type == "Fresh Produce":
                    print("Fresh Produce")
                    rewards.filter(name="Healthy Shopper").update(unlocked=True)
                elif grocery_item.type == "Seafood":
                    print("Seafood")
                    rewards.filter(name="Seafood Lover").update(unlocked=True)     

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
