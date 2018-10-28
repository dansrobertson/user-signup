from flask import Flask, request
import os
import jinja2
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def display_signup_form():
    template = jinja_env.get_template('signup_form.html')
    return template.render(username='', username_error='',
        password='', password_error='', verify_password='', verify_password_error='',
        email='', email_error='')

@app.route('/validate_signup', methods=['POST'])
def validate_signup():

    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify_password']
    email = request.form['email']

    username_error = ''
    password_error = ''
    verify_password_error = ''
    email_error = ''

    """username verification"""
    if username == "":
        username_error = "Please fill out a username."
    elif len(username) < 3 or len(username) > 20:
        username_error = "Not a valid username. Must be between 3 and 20 characters long."
        username = ""
    elif " " in username:
        username_error = "Username cannot have any spaces."
        username = ""
    
    """password varification"""
    if password == "":
        password_error = "Please fill out a password."
    elif len(password) < 3 or len(password) > 20:
        password_error = "Not a valid password. Must be between 3 and 20 characters long."
    elif " " in password:
        password_error = "Password cannot have any spaces."

    """2nd password entered verification"""
    #if not password_error:
    if verify_password == "":
        verify_password_error = "Please re-enter password."
    elif verify_password != password:
        verify_password_error = "Passwords do not match."

    """email verification"""
    if email != "":
        if len(email) < 3 or len(email) > 20:
            email_error = "Not a valid email. Ensure email is greater than 3 and less than 20 characters."

        match = re.match('^[_a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$', email)
        if match == None:
            email_error = "Not a valid email. Ensure proper email format such as test@test.com."

    """clear passwords if error"""
    if username_error or password_error or verify_password_error or email_error:
        password = ""
        verify_password = ""
    
    if not username_error and not password_error and not verify_password_error and not email_error:
        template = jinja_env.get_template('greeting.html')
        return template.render(username=username)
    else:
        template = jinja_env.get_template('signup_form.html')
        return template.render(username_error=username_error, password_error=password_error,
            verify_password_error=verify_password_error, email_error=email_error,
            username=username, password=password, verify_password=verify_password, email=email)

app.run()