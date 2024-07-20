from django import forms
from .models import JournalEntry

class JournalEntryForm(forms.ModelForm):
    entry_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    class Meta:
        model = JournalEntry
        fields = ["entry_date", "description"]
