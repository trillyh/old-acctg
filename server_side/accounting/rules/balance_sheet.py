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

        self.account_to_balance_sheet_mapping = {
            "Account receivable": ("Assets", "Current assets", "Notes and Accounts receivable"),
            "Cash": ("Assets", "Current assets", "Cash and cash equivalents"),
            "Inventory": ("Assets", "Current assets", "Inventories"),
            "Prepaid expenses": ("Assets", "Current assets", "Prepaid expenses"),
            "Other current assets": ("Assets", "Current assets", "Other current assets"),
            "Investments": ("Assets", "Non-current assets", "Investments, advances and long-term receivables"),
            "Property": ("Assets", "Non-current assets", "Property"),
            "Equipment": ("Assets", "Non-current assets", "Equipment"),
            "Intangibles": ("Assets", "Non-current assets", "Intangibles"),
            "Other non-current assets": ("Assets", "Non-current assets", "Other non-current assets"),
            "Accounts payable": ("Liabilities", "Current liabilities", "Accounts payable"),
            "Notes payable": ("Liabilities", "Current liabilities", "Notes payable"),
            "Income taxes payable": ("Liabilities", "Current liabilities", "Income taxes payable"),
            "Dividends payable": ("Liabilities", "Current liabilities", "Dividends payable"),
            "Accrued expenses": ("Liabilities", "Current liabilities", "Accrued expenses"),
            "Deferred revenues": ("Liabilities", "Current liabilities", "Deferred revenues"),
            "Other current liabilities": ("Liabilities", "Current liabilities", "Other current liabilities"),
            "Long-term debt": ("Liabilities", "Non-current liabilities", "Long-term debt"),
            "Deferred tax liabilities": ("Liabilities", "Non-current liabilities", "Deferred tax liabilities"),
            "Other non-current liabilities": ("Liabilities", "Non-current liabilities", "Other non-current liabilities"),
            "Common stock": ("Equities", "Common stock"),
            "Common stock without par value": ("Equities", "Common stock without par value"),
            "Common stock held in treasury": ("Equities", "Common stock held in treasury"),
            "Preferred stock": ("Equities", "Preferred stock"),
            "Additional paid-in capital": ("Equities", "Additional paid-in capital"),
            "Retained earnings": ("Equities", "Retained earnings"),
            "Accumulated other comprehensive income": ("Equities", "Accumulated other comprehensive income")
        }

    def generate(self):
        sub_entries = SubEntry.objects.filter(user_id=self.business_id)
        assert sub_entries is not None, "Is empty"

        for subentry in sub_entries:
            isDebit = subentry.sub_entry_type == "Debit"
            account = subentry.account

            if account in self.account_to_balance_sheet_mapping:

                if len(self.account_to_balance_sheet_mapping[account]) == 3:
                    section, group, item = self.account_to_balance_sheet_mapping[account]
                else: # Equities just section and items, no group
                    section, group, item = (self.account_to_balance_sheet_mapping[account][0], None, self.account_to_balance_sheet_mapping[account][1]) 

                isEquities = group == None

                if isEquities:
                    if isDebit:
                        self.balance_sheet[section][item] += subentry.amount
                    else:
                        self.balance_sheet[section][item] -= subentry.amount
                else:
                    if isDebit:
                        self.balance_sheet[section][group][item] += subentry.amount if isDebit else ((-1) * subentry.amount)
                    else:
                        self.balance_sheet[section][group][item] -= subentry.amount

