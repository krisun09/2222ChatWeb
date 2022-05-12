'''
    This file will handle our typical Bottle requests and responses 
    You should not have anything beyond basic page loads, handling forms and 
    maybe some simple program logic
'''
import bottle
from bottle import route, get, post, error, request, static_file, response

import model

#-----------------------------------------------------------------------------
# Static file paths
#-----------------------------------------------------------------------------

# Allow image loading
import sql


@route('/img/<picture:path>')
def serve_pictures(picture):
    '''
        serve_pictures

        Serves images from static/img/

        :: picture :: A path to the requested picture

        Returns a static file object containing the requested picture
    '''
    return static_file(picture, root='static/img/')

#-----------------------------------------------------------------------------

# Allow CSS
@route('/css/<css:path>')
def serve_css(css):
    '''
        serve_css

        Serves css from static/css/

        :: css :: A path to the requested css

        Returns a static file object containing the requested css
    '''
    return static_file(css, root='static/css/')

#-----------------------------------------------------------------------------

# Allow javascript
@route('/js/<js:path>')
def serve_js(js):
    '''
        serve_js

        Serves js from static/js/

        :: js :: A path to the requested javascript

        Returns a static file object containing the requested javascript
    '''
    return static_file(js, root='static/js/')

#-----------------------------------------------------------------------------
# Pages
#-----------------------------------------------------------------------------

# Redirect to login
@get('/')
@get('/home')
def get_index():
    '''
        get_index
        
        Serves the index page
    '''
    return model.index()

#-----------------------------------------------------------------------------

# Display the login page
@get('/login')
def get_login_controller():
    '''
        get_login
        
        Serves the login page
    '''
    return model.login_form()

#-----------------------------------------------------------------------------

# Attempt the login
@post('/login')
def post_login():
    '''
        post_login
        
        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')
    print(f"postLogin pwd: {password}")

    # Call the appropriate method
    bottle.response.set_cookie("username", username, None, max_age=60*60*24*30)

    return model.login_check(username, password)

#-----------------------------------------------------------------------------

# A cookie is a named piece of text stored in the user’s browser profile.
# You can access previously defined cookies via Request.get_cookie() and set new cookies with Response.set_cookie():
def get_username_cookie():
    """
        returns the current user
    """

    print(f"cookie user: {request.get_cookie('username')}")
    return request.get_cookie("username")
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------

@get('/about')
def get_about(): 
    '''
        get_about
        
        Serves the about page
    '''
    return model.about()

#-----------------------------------------------------------------------------

# Display the register page
@get('/register')
def get_register_controller():
    '''
        get_register
        
        Serves the login page
    '''
    return model.register_form()

#-----------------------------------------------------------------------------

# Attempt the register
@post('/register')
def post_register():
    '''
         get_register
        
         Handles register attempts
         Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')
    
    # Call the appropriate method
    return model.register(username, password)

#-----------------------------------------------------------------------------
@get('/add_friend')
def get_add_friend_controller():
    return model.add_friend_form()
# Attempt to add friend
@post('/add_friend')
def post_add_friend():
    friend_username = request.forms.get("friendUsername")
    user = get_username_cookie()
    return model.add_friend(user, friend_username)

#-----------------------------------------------------------------------------
@get('/choose_friend_to_chat')
def get_choose_friend():
    return model.choose_friend_form()

@post('/send_message')
def post_choose_friend():
    user = get_username_cookie()
    friend_name = request.forms.get("friendName")
    message = request.forms.get("message")

    model.save_message(user, friend_name, message)

    print(f"calling post_choose_friend, message is{message}")

    return model.choose_friend(user, friend_name, message)

@post('/receive_message')
def receive_friend_message():
    print(f"calling receive_friend_message")
    user = get_username_cookie()
    friend_name = request.forms.get("friendName")

    return model.receive_message(user, friend_name)


#-----------------------------------------------------------------------------
@get('/knowledge-repository')
def get_knowledge_repository():
    return model.get_knowledge_repository()


#-----------------------------------------------------------------------------
@get('/support')
def get_support():
    return model.get_support()

#-----------------------------------------------------------------------------
@get('/support-account')
def get_support_account():
    return model.get_support_account()

#-----------------------------------------------------------------------------
@get('/support-knowledgy')
def get_support_knowledgy():
    return model.get_support_knowledgy()

#-----------------------------------------------------------------------------
@get('/support-privacy')
def get_support_privacy():
    return model.get_support_privacy()

#-----------------------------------------------------------------------------
@get('/support-send_msg')
def get_support_send():
    return model.get_support_send()

#-----------------------------------------------------------------------------
# Help with debugging
@post('/debug/<cmd:path>')
def post_debug(cmd):
    return model.debug(cmd)

#-----------------------------------------------------------------------------

# 404 errors, use the same trick for other types of errors
@error(404)
def error(error): 
    return model.handle_errors(error)
