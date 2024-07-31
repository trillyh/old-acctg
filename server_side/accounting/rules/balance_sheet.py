from ..models import SubEntry
from typing import List, Dict, Set, Union
class BalanceSheet():
    def __init__(self, business_id: int, date=""):
        self.business_id = business_id 
        self.date = date
        self.balance_sheet = {
            "Assets": {
                "Current assets": {
                    "Cash and cash equivalents": 0,
                    "Notes and Accounts receivable": 0,
                    "Inventories": 0,
                    "Prepaid expenses": 0,
                    "Other current assets": 0
                },
                "Non-current assets": {
                    "Investments, advances and long-term receivables": 0,
                    "Property": 0,
                    "Equipment": 0,
                    "Intangibles": 0,
                    "Other non-current assets": 0
                }
            },
            "Liabilities": {
                "Current liabilities": {
                    "Accounts payable": 0,
                    "Notes payable": 0,
                    "Income taxes payable": 0,
                    "Dividends payable": 0,
                    "Accrued expenses": 0,
                    "Deferred revenues": 0,
                    "Other current liabilities": 0
                },
                "Non-current liabilities": {
                    "Long-term debt": 0,
                    "Deferred tax liabilities": 0,
                    "Other non-current liabilities": 0
                }
            },
            "Equities": {
                "Common stock": 0,
                "Common stock without par value": 0,
                "Common stock held in treasury": 0,
                "Preferred stock": 0,
                "Additional paid-in capital": 0,
                "Retained earnings": 0,
                "Accumulated other comprehensive income": 0
            }
        }
        # We prob don't need these sets... I just created them for fun and to learn Set comprehension
        self.assets_keyword = {account for account, asset_group in self.balance_sheet["Assets"].items() for account in asset_group}
        self.liabilities_keyword = {account for account, liability_group in self.balance_sheet["Liabilities"].items() for account in liability_group}
        self.equities_keyword = {account for account in self.balance_sheet["Equities"].keys()}


        print(self.assets_keyword)
        print(self.equities_keyword)
    def generate(self):
        print("getting")
        sub_entries = SubEntry.objects.filter(user_id=self.business_id)
        print(sub_entries)
        assert sub_entries is not None, "Is empty"

        for subentry in sub_entries:
            isDebit = subentry.sub_entry_type == "Debit"
            account = subentry.account
            
            if account == "Account receivable" and isDebit:
                self.balance_sheet["Assets"]["Current assets"]["Notes and Accounts receivable"] += subentry.amount

            elif account == "Cash" and isDebit:
                self.balance_sheet["Assets"]["Current assets"]["Cash and cash equivalents"] += subentry.amount



