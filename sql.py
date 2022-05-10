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
            pk TEXT,
            friendlist TEXT,
            admin INTEGER DEFAULT 0
        );""")

        self.commit()
        # Add our admin user
        self.add_user('admin', admin_password, None, admin=1)
        
        # new table for message
        self.execute("DROP TABLE IF EXISTS Messages")
        self.commit()

        # Create the users table
        # add column public key
        self.execute("""CREATE TABLE Messages(
            
            Id INT,
            username TEXT,
            from_user Text,
            msg Text
            
        );""")

        self.commit()

    #-----------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------#
    #++++++++++++++++++++++++++++ User handling ++++++++++++++++++++++++++++++++++#
    #-----------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------#

    # Add a user to the database
    def add_user(self,username, password, pk, admin=0):
        sql_cmd =   """INSERT INTO Users(Id,username,password,pk,admin)
                     VALUES({id}, '{username}', '{password}', '{pk}',  {admin})
                    """

        sql_cmd = sql_cmd.format(id=0,username=username, password=password, pk=pk, admin=admin)

        self.execute(sql_cmd)
        self.commit()
        
        #print(self.check_user_exist(username))
        return True
    
    #--------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------
    #--------------------------------------------------------------------------#
    # Check login credentials
    def check_credentials(self, username, password):
        sql_query = """SELECT 1 
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
        sql_query = """ SELECT 1 
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
        friendls = self.get_friendlist(user_id) # get the friend list
        friendls = list(friendls)
        if friendls == False:
            msg = "Please try to log in, username not found."
            return msg
        
        if friendls[0] == None:
            # friend list is empty for this user
            # create a friend list for him/she
            print("I have no friend: ")
            print(friendls)
            friendls[0] = friend_id
            print(friendls)
        else:
            print("I have friend already: ")
            print(friendls)
            # already have a friend list     
            friendls.append(friend_id)
        
          
        str_friendlist = ""
        i = 0
        while i < len(friendls):
            if i == len(friendls) - 1:
                str_friendlist += friendls[i]
                
            else:
                str_friendlist += friendls[i]
                str_friendlist += ", "
                
            i += 1
            
        
        
        # update the friend list into database 
        sql_query = """ UPDATE Users
                        SET friendlist = '{str_friendls}'
                        WHERE username = '{username}'
                    """ 
        sql_query = sql_query.format(str_friendls=str_friendlist, username=user_id)
        self.execute(sql_query)
        self.commit()

        msg = "Successfully add friend into friend list"


        return msg

        
    def get_friendlist(self, username):
        # get the friend list for the user
        sql_query = """SELECT friendlist
                       FROM Users
                       where username = '{username}'
                    """   
                                    
        sql_query = sql_query.format(username=username)
        self.execute(sql_query)
        self.commit()


        friend_list = self.cur.fetchone()
        if len(friend_list) > 0:
            # username exist in database
            return friend_list
        else:
            # user not found
            return False
        
    def get_pk(self, username):
        sql_query = """SELECT pk 
                       FROM Users
                       WHERE username = '{username}'
                    """                   
        sql_query = sql_query.format(username=username)
        self.execute(sql_query)
        self.commit()
        
        
        pk = self.cur.fetchone()
        if len(pk) > 0:
            # username exist in database
            
            return pk
        else:
            # user not found
            return False


    def delete_user(self, username):
        '''
        This function is only accessable by the admin.
        Users other than admin must not able to use this function.
        '''
        
        sql_query = """DELETE FROM Users WHERE Username = '{username}'"""
        
        
        sql_query = sql_query.format(username=username)
        self.execute(sql_query)
        self.commit() 
        
        msg = "Remove user {} from database".format(username)
        return msg  
            
    
    def save_msg(self, from_username, to_username, msg):
        '''
        把信息存到对应的用户的database里
        :parm: from_usernane : the user who send the message
        :parm: to_username: the user who will receive the message
        :parm: msg: the message that need to be saved
        '''
        
        # check does friend exist or not
        friend_exist = self.check_user_exist(to_username)
        
        if friend_exist:
            # friend exist
            sql_cmd =   """ INSERT INTO Messages(id,username,from_user,msg)
                            Values({id}, '{username}', '{from_user}', '{msg}'
                        """
                    
            sql_cmd = sql_cmd.format(id=0, username=to_username, from_user=from_username, msg=msg)
        
            self.execute(sql_cmd)
            self.commit()
        
            message = "Message successfully send."
        
        else:
            # friend does not exist
            message = "Sorry, enter friend does not exist, please try again."
            
        return message
    
    def get_msg(self, username):
        '''
        用户取出发给自己的信息
        :parm: username: the user who need to receive message
        '''
        sql_query = """SELECT msg 
                       FROM Messages
                       WHERE username = '{username}'
                    """                   
        sql_query = sql_query.format(username=username)
        self.execute(sql_query)
        self.commit()
        
        
        receive_msg = self.cur.fetchone()
        if len(receive_msg) > 0:
            # username exist in database
            receive_msg = str(receive_msg)
            return receive_msg
        
        else:
            # user not found
            return False


'''
# create our database
database = SQLDatabase("data.db") 
database.database_setup('admin')
database.add_user('irene', 'abc','xswl',admin=0) #true
database.add_user('kkk', '134',None,admin=0)  #true
#print(database.check_credentials('irene','abc')) #true
#print(database.check_credentials('kkk', '123')) #false
#print(database.add_friend('irene', 'kkk'))
#print(database.get_friendlist('irene'))
#print(database.delete_user('irene'))

database.add_friend('irene', 'kkk')

print(database.get_friendlist('irene'))

'''