from django.db import models
from django.contrib.auth.models import User
# Create your models here.

"""
  EntryID SERIAL PRIMARY KEY,
  UserID INTEGER NOT NULL,
  TransactionDate DATE NOT NULL,
  Description VARCHAR(255),
  CreateAt TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
  FOREIGN KEY (UserID) REFERENCES Users(UserID)
"""

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    entry_date = models.DateTimeField()
    description = models.CharField(max_length=250)
    create_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.description} created at {self.create_at}"

"""
The details of an entry, indicates debit and credit of an entry.
  EntryAccountID SERIAL PRIMARY KEY,
  EntryID INTEGER NOT NULL,
  Type VARCHAR(255) CHECK (Type IN ('Debit', 'Credit')),
  Account VARCHAR(255) NOT NULL,
  Amount DECIMAL(15, 2) NOT NULL CHECK(Amount >= 0),
  FOREIGN KEY (EntryID) REFERENCES JournalEntry(EntryID)
"""

class SubEntry(models.Model):
    DEBIT = 'Debit'
    CREDIT = 'Credit'
    TYPE_CHOICES = [
        (DEBIT, 'Debit'),
        (CREDIT, 'Credit')
    ]
    journal_entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE)
    sub_entry_type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    account = models.CharField(max_length=255) 
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.sub_entry_type} ${self.amount} in {self.account}"    
