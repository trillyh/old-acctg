### Need to figure where to put these setting
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server_side.settings')
django.setup()

from operator import is_
from nltk.featstruct import substitute_bindings
from ..utils.nlp_utils.preprocessor import Preprocessor
from .account_keywords import stemmed_account_keywords
from ..models import JournalEntry, SubEntry
from typing import List, Set, Optional
from django.contrib.auth.models import User

class SubEntries:  
    debit_liquid_related_keyword: Set[str] = {"received", "earned", "income", "deposit", "increase", "sold", "sell"}
    credit_liquid_related_keyword: Set[str] = {"bought", "purchase", "paid", "expense", "withdraw", "decrease"}

    def __init__(self, journal_entry: Optional[JournalEntry] = None, entry_description: Optional[str] = None):
        
        if journal_entry is not None:
            self.journal_entry: Optional[JournalEntry] = journal_entry #Set Union[JournalEntry, None] to fix mypy complaining journal_entry type can't be None
            self.entry_description =  journal_entry.description

        elif entry_description is not None:
            playground_user_id = 2
            self.journal_entry = JournalEntry.objects.filter(user_id=playground_user_id).first()
            self.entry_description = entry_description

        else:
            raise ValueError("Either journal_entry or entry_description must be provided")

        assert self.journal_entry is not None, "Journal Entry is none"
        self.user: Optional[User] = self.journal_entry.user
        self.debit_amount = 0
        self.credit_amount = 0
        self.debit_account = ""
        self.credit_account = ""

    """
    For simplicity, NLP is not implemented yet, and simple algorithm will be use to analyze simple entries
    Analyze the entry description:
        First part of the analysis is to determine whether it is debit or credit to liquid related asset (Cash, AR, etc..)
        Second part of the analysis is figure out whether to debit or credit based on what was on the first part:
            If first part was debited -> second is credit
            If first part was credited -> second is debit
            Figure out which account will be effected (Inventory, equipment, land, liabilities, stockholder's equity, etc..)
        Lastly, set debit and credit amount, and do assertion check dr.amount == credit.amount (Redundant for now, but again, we will need this in future)
    """
    def analyze(self):
        preprocessor = Preprocessor() 
        clean_tokenized_description: List[str] = []
        clean_tokenized_description = preprocessor.preprocess(self.entry_description)

        is_on_account = self.check_is_on_account(clean_tokenized_description)
        is_debit_liquid_related = self.check_is_debit_liquid_asset(clean_tokenized_description)

        liquid_amount = 0 
        try:
            liquid_amount = self.get_liquid_amount(clean_tokenized_description)
        except Exception as e:
            print("Indexing error occured when getting liquid amount") 
   
        debited = False # If debited in the first part, then credit in second part
        
        # Analyze the first part of journal entry
        if is_debit_liquid_related:
            self.debit_account = "Account Receivable" if is_on_account else "Cash"
            debited = True 

        else:
            self.credit_account = "Account Payable" if is_on_account else "Cash"
            debited = False
        
        account_involved: Set[str] = self.get_account_involved(clean_tokenized_description)
        # Analyze the second part of the journal entry
        if debited: # Second part will be credit
            self.credit_account = account_involved.pop()
        else: # Second part will be debit
            self.debit_account = account_involved.pop()

        self.debit_amount, self.credit_amount = liquid_amount, liquid_amount

        assert self.debit_amount == self.credit_amount, f"Expect debit = credit, instead got {self.debit_amount} != {self.credit_account}"


    def check_is_debit_liquid_asset(self, tokenized_description: List[str]): 
        return tokenized_description[0] in self.debit_liquid_related_keyword

    def check_is_on_account(self, tokenized_description: List[str]): 
        return tokenized_description[-1] == "account"

    def get_liquid_amount(self, tokenized_description) -> int:
        for i in range(len(tokenized_description)):
            if tokenized_description[i] == "$":
                return tokenized_description[i+1]
        return 0

    """
    Traverse the entry's description, return account involved in the transaction
    For now, this function is only expect to return a single account (List of 1 element)
    """
    def get_account_involved(self, tokenized_description: List[str]) -> Set[str]:
        assert stemmed_account_keywords, "Account keywords dictionary is empty"
        account_involved: Set[str] = set()

        for word in tokenized_description:
            for account, keyword in stemmed_account_keywords.items():
                if word in keyword:
                    account_involved.add(account)
        
        if not len(account_involved):
            account_involved.add("Unknown")
        return account_involved

    def save_to_db(self):
        # Test cases with JournalEntry being None, could raise error
        debit_entry = SubEntry(
            user=self.user,
            journal_entry=self.journal_entry,
            sub_entry_type='Debit',
            account = self.debit_account,
            amount = self.debit_amount)
        credit_entry = SubEntry(
            user=self.user,
            journal_entry=self.journal_entry,
            sub_entry_type='Credit',
            account = self.credit_account,
            amount = self.credit_amount)
        debit_entry.save()
        credit_entry.save()
        
    """
    For testing
    """
if __name__ == "__main__":
    test_cases = [
        "Bought $10 of boba on account",
        "Bought $50 of truck on account",
        "Received $20 for coffee",
        "Sold $30 of equipment on account",
        "Earned $100 from sales",
        "Paid $60 for rent",
        "Purchase $70 of supplies on account",
        "Withdraw $200 from account",
        "Deposit $150 to account",
        "Increase $90 in stock"
    ]
    
    for entry_description in test_cases:
        print(f"Test case: {entry_description}")
        subentries = SubEntries(entry_description=entry_description)
        subentries.analyze()
        print(f"Debit ${subentries.debit_amount} to {subentries.debit_account}")
        print(f"Credit ${subentries.credit_amount} to {subentries.credit_account}")
        print("\n" + "-"*38 + "\n")

    """
    Testing save to database
    """
    subentry = SubEntries(entry_description=test_cases[0])
    subentry.analyze()
    print(f"Debit ${subentry.debit_amount} to {subentry.debit_account}")
    print(f"Credit ${subentry.credit_amount} to {subentry.credit_account}")
