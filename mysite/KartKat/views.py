from django.shortcuts import render, redirect, get_object_or_404
from .models import ShoppingList, ShoppingListItem
from .forms import ShoppingListForm, ShoppingListItemForm

def shopping_list(request):
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
    else:
        form = ShoppingListForm()
        item_form = ShoppingListItemForm()

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