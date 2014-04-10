# HackerSchool Flask-OAuthlib Example

Demonstrate use of OAuth2 to connect to Hacker School accounts.

The Hacker School API is documented here: https://wiki.hackerschool.com/index.php/Hacker_School_API

## Setup

1. Do *Create an OAuth application* on https://www.hackerschool.com/settings
   1. Find your IP with something like `$ ifconfig en1 inet`
   2. Enter the redirect URL as something like `http://[your.ip.addr]:5000/oauth_authorized`
2. Create a `keys.sh` file and put the **ID** and **Secret** values into it
   ```bash
   export CONSUMER_KEY='[your.application.id]'
   export CONSUMER_SECRET='[your.application.secret]'
   ```

3. Put those variables in your environment with `$ source keys.sh`
4. Run the dev server with `$ ./example.py`

## Todo/Fixme

* Fails to get authorized username from hacker school api
