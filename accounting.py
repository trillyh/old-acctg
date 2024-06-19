""" 
Initialize tables if not exist.

Tables to be initialized:
- User: Store users data
- JournalEntry: Store the journal entries, but will not store the 
  the effects of an entry to accounts. Instead JournalEntryAccount table will store these effects.
- JournalEntryAccount: Store the effects of journal entries to accounts. (Debits, Credits and the amount)
"""
import psycopg2

connection = psycopg2.connect(host="localhost",
                              dbname="postgres",
                              user="postgres",
                              password="8383")

cur = connection.cursor()

connection.commit()

user_table = """ User (
  UserID SERIAL PRIMARY KEY,
  Username VARCHAR(255) UNIQUE NOT NULL,
  EMAIL VARCHAR(255) UNIQUE NOT NULL
);
"""

# Note: CreatedAt will not perform any timezone conversion
journal_entry = """ JournalEntry (
  EntryID SERIAL PRIMARY KEY,
  UserID INTEGER NOT NULL,
  TransactionDate DATE NOT NULL,
  Description VARCHAR(255),
  CreateAt TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
  FOREIGN KEY (UserID) REFERENCES User(UserID)
);
"""

journal_entry_account =  """ JournalEntryAccount(
  EntryAccountID SERIAL PRIMARY KEY,
  EntryID INTEGER NOT NULL,
  AccountType 
);
"""

check_and_create_query = """ 


"""

cur.execute()

connection.commit()

print("Close")
cur.close()
connection.close()
