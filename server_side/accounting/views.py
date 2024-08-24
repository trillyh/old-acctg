from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import JournalEntry
from .models import SubEntry
from .forms import JournalEntryForm
from .rules.subentries import SubEntries
from .rules.balance_sheet import BalanceSheet

"""
--- All views endpoint ---
"""
def show_about_page(request):
    return render(request, "accounting/about.html")

"""
1. Handle add, delete and edit forms of entries
2. Get all entries and pass them to context
3. Get balance sheet and pass them to context
"""
def show_playground_page(request):
    playground_id = 2
    curr_user = get_object_or_404(User, id=playground_id)

    editing_entry = None  # Entry being editied, none by default

    form = JournalEntryForm()
    if request.method == 'POST':
        if 'add' in request.POST:
            form = JournalEntryForm(request.POST)
            add_entry(form, curr_user)
            return redirect(show_playground_page)

        elif 'delete' in request.POST:
            entry_id = request.POST.get("entry_id") 
            delete_entry(entry_id, curr_user)
            return redirect(show_playground_page)

        elif 'edit' in request.POST:
            print(request.POST.dict())
            entry_id = request.POST.get('entry_id')
            editing_entry = get_object_or_404(JournalEntry, id=entry_id)
            form = JournalEntryForm(instance=editing_entry)

        elif 'save' in request.POST:
            entry_id = request.POST.get('entry_id') 
            editing_entry = get_object_or_404(JournalEntry, id=entry_id)
            print(f"form received {request.POST}")
            print(f"The editing entry is {editing_entry}")
            form = JournalEntryForm(request.POST, instance=editing_entry)
            if form.is_valid():
                form.save()
                return redirect(show_playground_page)

    entries = None
    try:
        entries = get_entries(playground_id)
    except JournalEntry.DoesNotExist: 
        raise Http404("No entries")

    entry_subentries = {}
    for entry in entries:
        subentries = entry.subentry_set.all()
        entry_subentries[entry.id] = subentries
    balance_sheet = get_and_analyze_balance_sheet(business_id=playground_id)
    context = {
        "form": form,
        "entries": entries,
        "entry_subentries": entry_subentries,
        "user": curr_user,
        "balance_sheet": balance_sheet,
        "editing_entry": editing_entry
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
------------- Helper functions -------------
"""
def add_entry(form: JournalEntryForm, user):
    if form.is_valid():
        journal_entry = form.save(commit=False)
        journal_entry.user = user
        journal_entry.save()
        print(f"User with ID {user.username} added new entry")
        
        print(type(JournalEntry.objects.filter(user_id=2).first()))
        subentries = SubEntries(journal_entry=journal_entry)
        subentries.analyze()
        subentries.save_to_db()
        print(f"Subentries added for JournalEntry ID {journal_entry.id}")
    else:
        print("Form is not valid")
        print(form.errors)

def delete_entry(entry_id, user):
        entry = get_object_or_404(JournalEntry, id=entry_id, user=user)
        entry.delete()
        print(f"Entry {entry_id} deleted")

def get_and_analyze_balance_sheet(business_id) -> BalanceSheet: 
    balance_sheet = BalanceSheet(business_id=business_id, date="07-30-2024")
    balance_sheet.generate()
    return balance_sheet 

"""
Return all journal entries from a business base on business's ID
"""
def get_entries(business_id: int):
    entries = JournalEntry.objects.filter(user_id=business_id).order_by("-entry_date")
    return entries
