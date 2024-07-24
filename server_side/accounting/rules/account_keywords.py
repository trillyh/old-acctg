from typing import Dict, Set
from nltk import PorterStemmer
from nltk.stem import porter

account_keywords: Dict[str, Set[str]] = {
    "Food Expense": {"burger", "boba", "coffee", "lunch", "dinner", "meal", "snack", "drink", "restaurant"},
    "Inventory": {"truck", "machine", "equipment", "tools", "supplies", "raw materials", "merchandise", "goods", "stock"},
    "Office Supplies": {"paper", "pen", "pencil", "notebook", "stapler", "envelope", "printer", "toner", "folder", "stationery"},
    "Travel Expense": {"flight", "hotel", "taxi", "uber", "train", "bus", "gas", "mileage", "ticket", "lodging"},
    "Utilities Expense": {"electricity", "water", "gas", "internet", "phone", "cable", "utility"},
    "Rent Expense": {"rent", "lease", "rental"},
    "Advertising Expense": {"advertising", "marketing", "promotion", "ad"},
    "Insurance Expense": {"insurance", "premium", "coverage"},
    "Maintenance and Repairs": {"repair", "maintenance", "fix", "service", "upkeep"},
    "Depreciation Expense": {"depreciation", "amortization"},
    "Interest Expense": {"interest", "loan", "mortgage"},
    "Salaries and Wages": {"salary", "wages", "payroll", "compensation", "earnings"},
    "Miscellaneous Expense": {"miscellaneous", "other"},
    "Income": {"income", "revenue", "sales", "earned"}
}

stemmer = PorterStemmer()
stemmed_account_keywords: Dict[str, Set[str]] = {
    account: {stemmer.stem(word) for word in words}
    for account, words in account_keywords.items()
}
