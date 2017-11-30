from flask import Flask, request, redirect, render_template, url_for
import cgi

app = Flask(__name__)

app.config['DEBUG'] = True 

@app.route('/')

def index():
    if request.args.get('username') is None:
        username = ''
    else:
        username = request.args.get('username')
    if request.args.get('email') is None:
        email = ''
    else:
        email = request.args.get('email')
    username_error = request.args.get('username_error')
    password_error = request.args.get('password_error')
    verify_password_error = request.args.get('verify_password_error')
    email_error = request.args.get('email_error')
    return render_template('index.html', username=username, email=email, username_error=username_error, password_error=password_error, verify_password_error=verify_password_error, email_error=email_error)

@app.route('/welcome', methods=['POST'])


def welcome():
    username = request.form['enter_username']
    username_escaped = cgi.escape(username, quote=True)
    password = request.form['enter_password']
    password_escaped = cgi.escape(password, quote=True)
    verify_password = request.form['verify_password']
    verify_password_escaped = cgi.escape(verify_password, quote=True)
    email = request.form['enter_email']
    email_escaped = cgi.escape(email, quote=True)

    def validate_username(username):
        if username == '':
            return False
        elif len(username) < 3 or len(username) > 20:
            return False
        elif (' ' in username) == True:
            return False
        else:
            return True

    def validate_password(password):
        if password == '':
            return False
        elif len(password) < 3 or len(password) > 20:
            return False
        else:
            return True

    def validate_email(email):
        if len(email) == 1 or len(email) ==2 or len(email) > 20:
            return False
        elif (' ' in email) == True:
            return False
        elif ('@' in email) < 1 or ('@' in email) > 1:
            return False
        elif ('.' in email) < 1 or ('.' in email) > 1:
            return False
        else:
            return True

    def password_match(verify_password, password):
        if verify_password != password:
            return False
        else:
            return True
        
    
    if validate_username(username) == False:
        username_error = 'That is not a valid username.'
    else:
        username_error = ''

    if validate_password(password) == False:
        password_error = 'That is not a valid password.'
    else:
        password_error = ''   

    if password_match(verify_password, password) == False:
        verify_password_error = 'Passwords do not match.'
    else:
        verify_password_error = ''

    if validate_email(email) == True or email == '':
        email_error = ''
    else:
        email_error = 'That is not a valid email address.'
 
    if validate_username(username) == True and validate_password(password) == True and password_match(verify_password, password)==True and (validate_email(email) == True or email == ''):
        return render_template('welcome.html', username=username_escaped)
    else: 
        return redirect('/?username={0}&email={1}&username_error={2}&password_error={3}&verify_password_error={4}&email_error={5}'.format(username, email, username_error, password_error, verify_password_error, email_error))
        
app.run()

#return redirect(url_for('index', username = username, email = email, username_error = username_error, password_error = password_error, password_match_error = password_match_error, email_error = email_error))