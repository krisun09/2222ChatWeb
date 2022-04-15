from operator import truediv
import sqlite3

# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call 
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise

class SQLDatabase():
    '''
        Our SQL Database

    '''

    # Get the database running
    def __init__(self, database_arg):
        self.conn = sqlite3.connect(database_arg) # create a connection object, creat a database
        # the cursor object allow us to excute the commands and queries in the database
        self.cur = self.conn.cursor()

    # SQLite 3 does not natively support multiple commands in a single statement
    # Using this handler restores this functionality
    # This only returns the output of the last command
    def execute(self, sql_string):
        out = None
        for string in sql_string.split(";"):
            try:
                out = self.cur.execute(string)
            except:
                pass
        return out

    # Commit changes to the database
    def commit(self):
        # similar to git commit
        self.conn.commit()

    #-----------------------------------------------------------------------------
    
    # Sets up the database
    # Default admin password
    def database_setup(self, admin_password='admin'):

        # Clear the database if needed
        self.execute("DROP TABLE IF EXISTS Users")
        self.commit()

        # Create the users table
        # add column public key
        self.execute("""CREATE TABLE Users(
            Id INT,
            username TEXT,
            password TEXT,
            admin INTEGER DEFAULT 0
        );""")

        self.commit()
        # Add our admin user
        self.add_user('admin', admin_password, admin=1)

    #-----------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------#
    #++++++++++++++++++++++++++++ User handling ++++++++++++++++++++++++++++++++++#
    #-----------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------#

    # Add a user to the database
    def add_user(self,username, password, admin=0):
        sql_cmd = """
                INSERT INTO Users
                (Id,username,password,admin)
                VALUES({id}, '{username}', '{password}', {admin})
            """

        sql_cmd = sql_cmd.format(id=0,username=username, password=password, admin=admin)

        self.execute(sql_cmd)
        self.commit()

        return True

    #-----------------------------------------------------------------------------

    # Check login credentials
    def check_credentials(self, username, password):
        sql_query = """
                SELECT 1 
                FROM Users
                WHERE username = '{username}' AND password = '{password}'
            """

        sql_query = sql_query.format(username=username, password=password)
        
        self.execute(sql_query)
        
        # If our query returns
        if self.cur.fetchone():
            return True
        else:
            return False
        
    def check_username_exist(self, username):
        sql_query = """
                SELECT 1 
                FROM Users
                WHERE username = '{username}'
            """

        sql_query = sql_query.format(username=username)
        
        self.execute(sql_query)
        
        if self.cur.fetchone():
            # username exist in database
            return True
        else:
            return False
        
    def add_friend(self,user_id, friend_id):
        # check friend exist in the database
        # if exist, get the public key 
        return 
        
    def get_friendlist(self, username):
        
        
        return 
"""
# create our database
database = SQLDatabase() 
database.database_setup(admin_password='admin')
print(database.add_user('irene', 'abc', admin=0))
print(database.check_credentials('irene','abc'))
print(database.check_credentials('kkk', '123'))

"""