from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import JournalEntry, User
from .utils import get_data_utils
from .forms import JournalEntryForm
# Create your views here.

def show_about_page(request):
    return render(request, "accounting/about.html")

def show_playground_page(request):
    business_id = 2
    user = get_object_or_404(User, id=business_id)
    if request.method == 'POST':
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = user
            entry.save()
            return redirect('show_playground_page')
    else:
        form = JournalEntryForm()
    
    entries = None
    try:
        entries = get_data_utils.get_entries(business_id)
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
