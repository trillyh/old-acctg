from ..utils.nlp_utils.preprocessor import Preprocessor
from typing import List, Set

class SubEntries:  
    debit_asset_keywords: List[str] = ["received", "earned", "income", "deposit", "increase"]
    credit_asset_keywords: List[str] = ["bought", "purchase", "paid", "expense", "withdraw", "decrease"]
    def __init__(self, entry_description):
        self.entry_description = entry_description
        self.debit_amount = 0
        self.credit_amount = 0
        self.debit_account = ""
        self.credit_account = ""

    def analyze(self):
        preprocessor = Preprocessor() 
        clean_tokenized_description: List[str] = []
        clean_tokenized_description = preprocessor.preprocess(self.entry_description)
        print(clean_tokenized_description)
        self.analyze_debits()
        self.analyze_credits()
        assert self.debit_amount == self.credit_amount, f"Expect debit = credit, instead got {self.debit_amount} != {self.credit_account}"
    
    def analyze_debits(self):
        pass

    def analyze_credits(self):
        pass

    def save_to_db(self):
        pass

    """
    For testing
    """
if __name__ == "__main__":
    entry_description = "Bought 10$ of boba"
    subentries = SubEntries(entry_description)
    subentries.analyze()

