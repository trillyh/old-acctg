
class JournalEntry:

  def __init__(self): 
    self.dr = {"Nothing": 0}   
    self.cr = {"Nothing": 0}
    self.dr_amount = 0
    self.cr_amount = 0

  def debit(self, account, amount):
      assert isinstance(account, str), "Account must be a string"
      assert isinstance(amount, int, float), "Entry amount must be a float"       

      dr["Account"] = amount

  def credit(self, account, amount):
      assert isinstance(account, str), "Account must be a string"
      assert isinstance(amount, int, float), "Entry amount must be a float"       

      dr["Account"] = amount

  def finalize(self): 
    """ 
    This function first check if the debit amount and credit amount balanced according to the 
    US GAAP rule. 

    Insert to database to finalize.
    """
    if (dr_amount != cr_amount):
      print(f"Expecting Debit and Credit to equal \n Dr: {dr_amount}$ Credit: {cr_amount}$")
      return

    try:
      insert_to_db(self)
    except: 
      print("Error occured when inserting entry to database")
    else:
      print("Successfully finalized and inserted entry to database")

  def insert_to_db(self):
      print("Inserting to databse")
    
