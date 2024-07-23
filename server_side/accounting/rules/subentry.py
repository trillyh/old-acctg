class SubEntry:  
    def __init__(self, entry_description):
        self.entry_description = entry_description
        self.debit_amount = 0
        self.credit_amount = 0
        self.debit_account = 0
        self.credit_account = 0

    def analyze(self):
        self.analyze_debits()
        self.analyze_credits()
        assert self.debit_amount == self.credit_amount, f"Expect debit = credit, instead got {self.debit_amount} != {self.credit_account}"
    
    def analyze_debits(self):
        pass

    def analyze_credits(self):
        pass
