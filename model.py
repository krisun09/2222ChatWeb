'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import controller
import view
import random
import sql
from Crypto.PublicKey import RSA
import bcrypt

# Initialise our views, all arguments are defaults for the template
page_view = view.View()

database_args = "database.db"
sql_db = sql.SQLDatabase(database_args)
sql_db.database_setup(admin_password='admin')

salt = bcrypt.gensalt()

# id counter for knowledge repo
id_counter = 5

# -----------------------------------------------------------------------------
# Index
# -----------------------------------------------------------------------------

def index():
    '''
        index
        Returns the view for the index
    '''
    return page_view("index")


# -----------------------------------------------------------------------------
# Login
# -----------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("login")


# -----------------------------------------------------------------------------

# Check the login credentials
def login_check(username, password):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''

    # By default assume good creds
    login = True
    err_str = "Incorrect username or password"
    

    # it will change to false if username and password does not match
    login = sql_db.check_credentials(username, process_enc_pwd(password))
    if username == "admin" or username == "irene" or username == "christina":
        login = sql_db.check_credentials(username, password)
        
    if login:
        print("this is after login: ")
        print(sql_db.check_user_exist(username))
        print(f"validLogin:{username}")
        return page_view("valid_login", name=username, friend_ls=sql_db.get_friendlist(username))
    else:
        return page_view("invalid", reason=err_str)


# -----------------------------------------------------------------------------
# register
# -----------------------------------------------------------------------------

def register(username, password):
    '''
        register
        Returns the view for the register
    '''

    # register = True
    register = sql_db.check_user_exist(
        username)  # check whether the name has been used or not, if not, change the value of register
    err_str = "Username in use"

    if register == False:
        # false when the user name does not exist / haven't been used
        print(username)
        print(password)

        # salt and hash the enc_pwd here
        secure_pwd = process_enc_pwd(password)

        sql_db.add_user(username, secure_pwd, generate_RSA_keypair().decode(), admin=0)
        print(f"register: check_user_exist after add_user: {sql_db.check_user_exist(username)}")

        # register done, go back to login page
        return page_view("login")
    else:
        return page_view("invalid", reason=err_str)


# -----------------------------------------------------------------------------

def register_form():
    return page_view("register")


# -----------------------------------------------------------------------------

def display_valid_login_page(username):
    return page_view("valid_login", friend_ls=sql_db.get_friendlist(username))


# -----------------------------------------------------------------------------

def generate_RSA_keypair():
    key = RSA.generate(2048)
    private_key = key.export_key()

    print("private_key: " + str(private_key))

    file_out = open("private.pem", "wb")
    file_out.write(private_key)
    file_out.close()

    public_key = key.publickey().export_key()

    print("public_key: " + str(public_key))

    file_out = open("receiver.pem", "wb")
    file_out.write(public_key)
    file_out.close()

    return public_key

# -----------------------------------------------------------------------------
# Add friend
# -----------------------------------------------------------------------------

def add_friend_form():
    self_username = controller.get_username_cookie()
    friend_ls = sql_db.get_friendlist(self_username)
    return page_view("/add_friend", friend_ls=friend_ls)


def add_friend(user_id, friend_name):
    print(user_id)
    print(sql_db.add_friend(user_id, friend_name))
    sql_db.add_friend(friend_name, user_id)
    print(sql_db.get_friendlist(user_id))
    self_username = controller.get_username_cookie()
    friend_ls = sql_db.get_friendlist(self_username)
    return page_view("valid_login", name=self_username, friend_ls=friend_ls)


def choose_friend_form():
    self_username = controller.get_username_cookie()
    return page_view("/choose_friend_to_chat", friend_ls=sql_db.get_friendlist(self_username))


def choose_friend(user, friendID, message):
    print(f"model/choose_friend - curr user: {user}")
    print(f"model/choose_friend - curr friendID: {friendID}")
    print(f"model/choose_friend - message: {message}")
    self_username = controller.get_username_cookie()
    return page_view("/choose_friend_to_chat", name=self_username, friend_ls=sql_db.get_friendlist(self_username))


def save_message(from_user, to_user, message):
    sql_db.save_msg(from_user, to_user, message)


def receive_message(from_user, to_user):
    self_username = controller.get_username_cookie()
    full_message = sql_db.get_msg(self_username)
    message = full_message[1]
    from_user = full_message[0]
    print(f"model/receive msg: from_user {from_user}: message is {message}")
    return page_view("/choose_friend_to_chat", friend_ls=sql_db.get_friendlist(self_username), message=message,
                     from_user=from_user)

# -----------------------------------------------------------------------------
# knowledge-repository
# -----------------------------------------------------------------------------

def get_knowledge_repository():
    return page_view("knowledge-repository")

def get_ask_question():
    return page_view("ask-question")

def write_to_knowledge_repo(title, text, from_user):
    """writes to knowledge_repository.html"""

    global id_counter
    new_id_counter = id_counter
    id_counter = new_id_counter + 1
    formatted_text = (
            f'''
              <div id={id_counter} class="div-question">
                  <h4 class="question-title">{title}</h4>
                  <div class="question-body">
                      <p>{text}</p>
                  </div>
                  <div class="question-footer">
                      <p>{from_user}</p>
                  </div>
              </div>'''
                      )
    # with open('templates/knowledge-repository.html') as f:
    #     t = f.read()

    # html = """          <div class="all-questions">
    #           <div id="0" class="div-question">
    #               <h4 class="question-title">Why am i learning cybersecurity?</h4>
    #               <div class="question-body">
    #                   <p>Because it's a core</p>
    #               </div>
    #           </div>
    #           replace_meee
    #       </div>"""
    #
    # soup = BeautifulSoup(html, 'html.parser')
    # target = soup.find_all(text=re.compile(r'replace_meee'))
    # for v in target:
    #     v.replace_with(v.replace('replace_meee', formatted_text))
    # print(html)


    with open('templates/knowledge-repository.html', "a") as f:
        f.write(formatted_text)

        # t = Template(f.read())

        # Create a dict with template keys and their values
    # val = {'replace_me': formatted_text}

    # g = jinja2.Template('{{t | replace("replace_me", formatted_text)}}')
    #
    # with open('templates/knowledge-repository.html', "w") as f:
    #     f.write(t.render(replace_me=formatted_text))


# write_to_knowledge_repo("testing write func", "is it working?")

# -----------------------------------------------------------------------------
# Support page
# -----------------------------------------------------------------------------

def get_support():
    return page_view("support")

# -----------------------------------------------------------------------------
# Support-account page
# -----------------------------------------------------------------------------

def get_support_account():
    return page_view("support-account")

# -----------------------------------------------------------------------------
# Support-knowledgy page
# -----------------------------------------------------------------------------

def get_support_knowledge():
    return page_view("support-knowledge")

# -----------------------------------------------------------------------------
# Support-privacy page
# -----------------------------------------------------------------------------

def get_support_privacy():
    return page_view("support-privacy")

# -----------------------------------------------------------------------------
# Support-send_msg page
# -----------------------------------------------------------------------------

def get_support_send():
    return page_view("support-send_msg")
# -----------------------------------------------------------------------------
# About
# -----------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("about", garble=about_garble())


# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.",
              "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
              "organically grow the holistic world view of disruptive innovation via workplace change management and empowerment.",
              "bring to the table win-win survival strategies to ensure proactive and progressive competitive domination.",
              "ensure the end of the day advancement, a new normal that has evolved from epistemic management approaches and is on the runway towards a streamlined cloud solution.",
              "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]


# -----------------------------------------------------------------------------
# Cryptography
# -----------------------------------------------------------------------------

def process_enc_pwd(enc_pwd):
    # use bcrypt over SHA512 is that bcrypt is designed to be slow.
    """
        salt + hash a string
    """
    print(f"original pwd: {enc_pwd}")

    hashed = bcrypt.hashpw(bytes(enc_pwd, 'utf-8'), salt)

    print(f"salt: {salt}")
    print(f"hashed: {hashed}")

    return hashed.decode("utf-8")


# -----------------------------------------------------------------------------
# Debug
# -----------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass


# -----------------------------------------------------------------------------
# 404
# Custom 404 error page
# -----------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = error.body
    return page_view("error", error_type=error_type, error_msg=error_msg)
