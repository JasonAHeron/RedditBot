"""
                     ____           __    ___ __  ____        __ 
                    / __ \___  ____/ /___/ (_) /_/ __ )____  / /_
                   / /_/ / _ \/ __  / __  / / __/ __  / __ \/ __/
                  / _, _/  __/ /_/ / /_/ / / /_/ /_/ / /_/ / /_  
                 /_/ |_|\___/\__,_/\__,_/_/\__/_____/\____/\__/  
                                                                 
                        Written by Jason Heron & Nick Wood         
                                     (c) 2014
                                     
botgen/forms.py -- Flask forms for the bot generator app
"""

from flask.ext.wtf import Form, TextField, PasswordField
from flask.ext.wtf import Required, EqualTo, Length

class RegisterForm(Form):
    # Define validators for form fields
    validators = {
        'name'   : [Required(), Length(min=6, max=25)],
        'email'  : [Required(), Length(min=6, max=40)],
        'passwd' : [Required(), Length(min=6, max=40)],
        'passrp' : [
                Required(), 
                EqualTo('password', message='Passwords must match')
            ]
    }

    # Define form fields
    name     = TextField('Username', validators=validators['name'])
    email    = TextField('Email', validators=validators['email'])
    password = PasswordField('Password', validators=validators['passwd'])
    confirm  = PasswordField('Repeat Password', validators=validators['passrp'])

class LoginForm(Form):
    name     = TextField('Username', [Required()])
    password = PasswordField('Password', [Required()])

class ForgotForm(Form):
    email = TextField('Email', validators = [Required(), Length(min=6, max=40)])

class SearchBotForm(Form):
    subreddits  = TextField('buildapcsales, hardwareswap')
    searchwords = TextField('cpu, gpu')
    frequency   = TextField('20')
    recipient   = TextField('jason')