from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import JournalEntry
from .utils import get_data_utils
from .forms import JournalEntryForm


def show_about_page(request):
    return render(request, "accounting/about.html")

def show_playground_page(request):
    playground_id = 2
    user = get_object_or_404(User, id=playground_id)
    form = JournalEntryForm()
    if request.method == 'POST':
        if 'add' in request.POST:
            print(f"{request.POST.dict()}")
            form = JournalEntryForm(request.POST)
            entry = form.save(commit=False)
            entry.user = User.objects.get(id=playground_id)
            entry.save()
            print(f"User with ID {playground_id} added new entry")
            return redirect(show_playground_page)


    entries = None
    try:
        entries = get_data_utils.get_entries(playground_id)
    except JournalEntry.DoesNotExist: 
        raise Http404("No entries")
    context = {
        "form": form,
        "entries": entries,
        "user": user
    } 
    return render(request, "accounting/playground.html", context) 

def show_concepts_page(request):
    return render(request, "accounting/concepts.html")

def show_entries(request, business_id):
    try:
        entries = get_data_utils.get_entries(business_id)
    except JournalEntry.DoesNotExist: 
        raise Http404("No entries")
    return render(request, "accounting/playground.html", {"entries": entries})
    
def generate_financial_statement(request, business_id): 
    return render(request, "accounting/playground.html")

"""
------------- Utils function -------------
"""


