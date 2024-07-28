from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import JournalEntry
from .utils import get_data_utils
from .forms import JournalEntryForm
from .rules.subentries import SubEntries

"""
--- All views endpoint ---
"""

def show_about_page(request):
    return render(request, "accounting/about.html")

def show_playground_page(request):
    playground_id = 2
    curr_user = get_object_or_404(User, id=playground_id)
    form = JournalEntryForm()
    if request.method == 'POST':
        if 'add' in request.POST:
            form = JournalEntryForm(request.POST)
            handle_add_entry_form(form, curr_user)
            return redirect(show_playground_page)

        elif 'delete' in request.POST:
            entry_id = request.POST.get("entry_id") 
            handle_delete_entry_form(entry_id, curr_user)
            return redirect(show_playground_page)

        elif 'edit' in request.POST:
            print(request.POST.dict())
            pk = request.POST.get('entry_id')
            form = handle_edit_entry_form(pk)

    entries = None
    try:
        entries = get_data_utils.get_entries(playground_id)
    except JournalEntry.DoesNotExist: 
        raise Http404("No entries")
    context = {
        "form": form,
        "entries": entries,
        "user": curr_user 
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
def handle_add_entry_form(form: JournalEntryForm, user):
    if form.is_valid():
        entry = form.save(commit=False)
        entry.user = user
        entry.save()
        print(f"User with ID {user.username} added new entry")
        
        print(type(JournalEntry.objects.filter(user_id=2).first()))
        print(type(entry))
        subentries = SubEntries(journal_entry=entry)
        subentries.analyze()
        subentries.save_to_db()
        print("Two subentries saved")
    else:
        print("Form is not valid")
        print(form.errors)

def handle_delete_entry_form(entry_id, user):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=user)
    entry.delete()
    print(f"Entry {entry_id} deleted")

def handle_edit_entry_form(entry_id: int):
    entry = JournalEntry.objects.get(id = entry_id)
    return JournalEntryForm(instance=entry) 

