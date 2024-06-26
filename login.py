import utils
import psycopg2

# Login function
def login(self):
  connection = utils.get_connection()
  cur = connection.cursor()

  while True:
    print("Type 'back' to return to previous menu")

    username = input("Please enter your username")
    if is_back(username, connection, cur) : break

    password = input("Please enter your password")
    if is_back(password, connection, cur) : break
    try:
      cur.execute("""
        SELECT UserID
        FROM Users
        WHERE Username = %s AND Password = %s
      """, (username, password))

      user = cur.fetchone()
      if user is None:
        print("Wrong username or password")
      else:
        print("Login successful! UserID:", user[0])
        break

    except psycopg2.Error as e:
      print("An error occurred: ", e)
      break
  cur.close()
  connection.close()

# Create account function
def create_account(self):
  connection = utils.get_connection()
  cur = connection.cursor()

  print("Type 'back' to return to previous menu")
  username = input("Please enter your new username")
  if is_back(username, connection, cur) : return
  password = input("Please enter your new password")
  if is_back(password, connection, cur) : return
  try:
    cur.execute("""
      INSERT INTO Users (Username, Password)
      VALUES (%s, %s) 
    """, (username, password))
  except psycopg2.Error as e:
    print("An error occurred: ", e)
  cur.close()
  connection.close()

  print("Succesfully created a new account")

def is_back(self, input, connection, cur):
  if input.lower() == "back":
    connection.close()
    cur.close()
    return true
  return false

