#!/usr/bin/env python3

import os
import binascii
import json
from functools import wraps

from flask import Flask, session, url_for, flash, redirect, request, render_template
from flask_oauthlib.client import OAuth

## flask app and an oauth object  ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

app = Flask(__name__)
app.secret_key = binascii.hexlify(os.urandom(16))

auth = OAuth(app).remote_app(
    'hackerschool'
    , base_url         = 'https://www.hackerschool.com/api/v1/'
    , access_token_url = 'https://www.hackerschool.com/oauth/token'
    , authorize_url    = 'https://www.hackerschool.com/oauth/authorize'
    , consumer_key     = os.environ.get('CONSUMER_KEY', None)
    , consumer_secret  = os.environ.get('CONSUMER_SECRET', None)
    , access_token_method='POST'
    )

## internal auth mechanics ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

def get_login():
    # our internal function to retrieve login data
    # knowledge of session['login'] is only in here, oauth_authorized, and logout
    return session.get('login')

@auth.tokengetter
def get_token(token=None):
    # a decorated tokengetter function is required by the oauth module
    return get_login()['oauth_token']

def protected(route):
    # in large apps it is probably better to use the Flask-Login extension than
    # this route decorator because this decorator doesn't provide you with
    # 1. user access levels or
    # 2. the helpful abstraction of an "anonymous" user (not yet logged in)
    @wraps(route)
    def wrapper(*args, **kwargs):
        kwargs.update(login=get_login())
        return route(*args, **kwargs) if kwargs['login'] \
            else redirect(url_for('login', next=request.url))
        # redirect includes "next=request.url" so that after logging in the
        # user will be sent to the page they were trying to access
    return wrapper

## external auth mechanics  ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

@app.route('/login')
def login():
    if get_login():
        flash('You are already logged in.')
        return redirect(request.referrer or url_for('index'))
    else:
        afterward = request.args.get('next') or request.referrer or None
        landing = '%s?next=%s' % (os.environ.get('REDIRECT_URI'), afterward)
        return auth.authorize(callback=landing)

@app.route('/oauth_authorized')
@auth.authorized_handler
def oauth_authorized(resp):
    try:
        # make a partial login session here, get the username later if this part works
        # keys into resp are probably different for different oauth providers, unfortunately
        session['login'] = dict(oauth_token=(resp['access_token'], resp['refresh_token']))
    except TypeError as exc:
        flash('The login request was gracefully declined. (TypeError: %s)' % exc)
        return redirect(url_for('index'))
    except KeyError as exc:
        flash('There was a problem with the response dictionary. (KeyError: %s) %s' % (exc, resp))
        return redirect(url_for('index'))
    # now get their username
    me = auth.get('people/me')
    if me.status == 200:
        session['login']['user'] = '{first_name} {last_name}'.format(**me.data)
        session['login']['email'] = me.data['email']
        session['login']['image'] = me.data['image']
    else:
        session['login']['user'] = 'Hacker Schooler'
    flash('You are logged in.')
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    # the important bit here is to remove the login from the session
    flash('You have logged out.') if session.pop('login', None) \
        else flash('You aren\'t even logged in.')
    return redirect(url_for('index'))

## pages ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

@app.route('/', methods=["GET", "POST"])
@protected
def index(login=None):
    res = None
    if 'endp' in request.form:
        res = json.dumps(auth.get(request.form['endp']).data, indent=4)
    return render_template('index.html', login=login, res=res)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

# eof
