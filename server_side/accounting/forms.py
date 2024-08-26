from django import forms
from .models import JournalEntry
from .models import SubEntry

class JournalEntryForm(forms.ModelForm):
    entry_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    class Meta:
        model = JournalEntry
        fields = ["entry_date", "description"]

class SubEntryEditingForm(forms.ModelForm):
        ACCOUNTS_CHOICES = [
            ('Accounts Receivable', 'Accounts Receivable'),
            ('Cash', 'Cash'),
            ('Inventories', 'Inventories'),
        ]
        account = forms.ChoiceField(choices=ACCOUNTS_CHOICES, required=True)
        class Meta:
            model = SubEntry
            fields = ["account"]
            
