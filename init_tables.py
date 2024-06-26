""" 
Initialize tables if not exist.

Tables to be initialized:
- User: Store users data
- JournalEntry: Store the journal entries, but will not store the 
  the effects of an entry to accounts. Instead JournalEntryAccount table will store these effects.
- JournalEntryAccount: Store the effects of journal entries to accounts. (Debits, Credits and the amount)
"""
import utils
import psycopg2

connection = utils.get_connection()
cur = connection.cursor()

user_table_def = """ (
  UserID SERIAL PRIMARY KEY,
  Username VARCHAR(255) UNIQUE NOT NULL,
  Password VARCHAR(255) NOT NULL
  EMAIL VARCHAR(255) UNIQUE NOT NULL
);
"""

# Note: CreatedAt will not perform any timezone conversion
journal_entry_def = """ (
  EntryID SERIAL PRIMARY KEY,
  UserID INTEGER NOT NULL,
  TransactionDate DATE NOT NULL,
  Description VARCHAR(255),
  CreateAt TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
  FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
"""

journal_entry_account_def =  """ (
  EntryAccountID SERIAL PRIMARY KEY,
  EntryID INTEGER NOT NULL,
  Type VARCHAR(255) CHECK (Type IN ('Debit', 'Credit')),
  Account VARCHAR(255) NOT NULL,
  Amount DECIMAL(15, 2) NOT NULL CHECK(Amount >= 0),
  FOREIGN KEY (EntryID) REFERENCES JournalEntry(EntryID)
);
"""

tables_query = [
    ("Users", user_table_def),
    ("JournalEntry", journal_entry_def),
    ("JournalEntryAccount", journal_entry_account_def)
]

print("Initialzing tables if not exist...")
try:
   for table_name, table_definition in tables_query:
     create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} {table_definition} "
     cur.execute(create_table_query)
   connection.commit()
   print("Tables created successfully")
except psycopg2.Error as e:
   print("An error occurred: ", e)
   connection.rollback()  # Roll back the transaction on error

cur.close()
connection.close()
