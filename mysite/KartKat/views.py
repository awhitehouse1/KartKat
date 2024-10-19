from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import ShoppingList
from .forms import ShoppingListForm


def shopping_list(request):
    if request.method == 'POST':
        form = ShoppingListForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ShoppingListForm()

    shopping_lists = ShoppingList.objects.all()
    context = {
        'shopping_lists': shopping_lists,
        'form': form,
    }
    return render(request, 'index.html', context)


def create_shopping_list(request):
    # Define this view if needed
    pass

