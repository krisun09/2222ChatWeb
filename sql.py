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
    def __init__(self, database_arg='database.db'):
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
            pk TEXT,
            friendlist TEXT,
            admin INTEGER DEFAULT 0
        );""")

        self.commit()
        # Add our admin user
        self.add_user('admin', admin_password, None, admin=1)

    #-----------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------#
    #++++++++++++++++++++++++++++ User handling ++++++++++++++++++++++++++++++++++#
    #-----------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------#

    # Add a user to the database
    def add_user(self,username, password, pk, admin=0):
        sql_cmd = """
                INSERT INTO Users
                (Id,username,password,pk,admin)
                VALUES({id}, '{username}', '{password}', '{pk}',  {admin})
            """

        sql_cmd = sql_cmd.format(id=0,username=username, password=password, pk=pk, admin=admin)

        self.execute(sql_cmd)
        self.commit()

        return True
    
    #--------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------
    #--------------------------------------------------------------------------#
    # Check login credentials
    def check_credentials(self, username, password):
        sql_query = """
                SELECT 1 
                FROM Users
                WHERE username = '{username}' AND password = '{password}'
            """
        sql_query = sql_query.format(username=username, password=password)
        
        self.execute(sql_query)
        self.commit()
        
        # If our query returns
        if self.cur.fetchone():
            return True
        else:
            return False
        
    #--------------------------------------------------------------------------#
    #--------------------------------------------------------------------------#
    #--------------------------------------------------------------------------#
    # check does username already exist or not  
    def check_user_exist(self, username):
        sql_query = """
                SELECT 1 
                FROM Users
                WHERE username = '{username}'
            """
        sql_query = sql_query.format(username=username)
        
        self.execute(sql_query)
        self.commit()
        
        if self.cur.fetchone():
            # username exist in database
            return True
        else:
            return False
    
    #--------------------------------------------------------------------------#
    #--------------------------------------------------------------------------#
    #--------------------------------------------------------------------------#   
    def add_friend(self,user_id, friend_id):
        # check does the friend that we want to add is our web user or not
        if self.check_user_exist(friend_id) == False:
            msg = "Friend does not exist, please enter a valid friend username."
            return msg
                
        # get the friend list for the user     
        str_friendls = self.get_friendlist(user_id) # get the friend list
        if str_friendls == False:
            msg = "Please try to log in, username not found."
            return msg
        
        if str_friendls == None:
            # friend list is empty for this user
            # create a friend list for him/she
            friend_list = []
            friend_list.append(friend_id)
        else:
            # already have a friend list
            friend_list = eval(str_friendls)
            friend_list.append(friend_id)
                
        str_friendls = str(friend_id) 
             
        # update the friend list into database 
        sql_query = """
            UPDATE Users 
            SET friendlist = str_friends,
            WHERE username = '{username}'
        """ 
        sql_query = sql_query.format(username=user_id)
        self.execute(sql_query)
        self.commit()
            
        msg = "Successfully add friend into friend list"
        return msg

        
    def get_friendlist(self, username):
        # get the friend list for the user
        sql_query = """
                SELECT friendlist 
                FROM Users
                WHERE username = '{username}'
            """                   
        sql_query = sql_query.format(username=username)
        self.execute(sql_query)
        self.commit()
        
        if self.cur.fetchone():
            # username exist in database
            friend_list = self.cur.fetchone()
            return friend_list
        else:
            # user not found
            return False
        
    def get_pk(self, username):
        sql_query = """
                SELECT pk 
                FROM Users
                WHERE username = '{username}'
            """                   
        sql_query = sql_query.format(username=username)
        self.execute(sql_query)
        self.commit()
        
        if self.cur.fetchone():
            # username exist in database
            pk = str(self.cur.fetchone())
            return pk
        else:
            # user not found
            return False
"""
# create our database
database = SQLDatabase() 
database.database_setup('admin')
print(database.add_user('irene', 'abc',None,admin=0))
print(database.add_user('kkk', '134',None,admin=0))
print(database.check_credentials('irene','abc'))
print(database.check_credentials('kkk', '123'))
print(database.add_friend('irene', 'kkk'))
"""