from ..models import JournalEntry

"""
Return all journal entries from a business base on business's ID
"""
def get_entries(business_id: int):
    entries = JournalEntry.objects.filter(user_id=business_id).order_by("-entry_date")
    return entries
