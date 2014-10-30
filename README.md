# Hacker School API Playground

Allow HSers to play with HS API endpoints.

The Hacker School API is documented here: https://wiki.hackerschool.com/index.php/Hacker_School_API

## Setup

1. Clone this repo and use `pip install -r requirements.txt` to get the dependencies; you may wish to do this in a [virtual environment](https://docs.python.org/dev/library/venv.html)
1. Create a new Heroku application
1. Do *Create an OAuth application* on https://www.hackerschool.com/settings
   1. Enter the redirect URL as something like `https://[app-name].herokuapp.com/oauth_authorized`
2. Create a `keys.sh` file and put the **ID**, **Secret** and **redirect** values into it
   ```bash
   export CONSUMER_KEY='[your.application.id]'
   export CONSUMER_SECRET='[your.application.secret]'
   export REDIRECT_URI='[your.redirect.uri]'
   ```

3. Put those variables in your environment with `$ source keys.sh` and set them on Heroku with `$ heroku config:set CONSUMER_KEY="$CONSUMER_KEY" CONSUMER_SECRET="$CONSUMER_SECRET" REDIRECT_URI="$REDIRECT_URI"`
4. Run the dev server with `$ foreman start`
5. Visit the server in your browser using your IP address in something like `http://localhost:5000/`. You will need to correct the URL to localhost when you are redirected.
