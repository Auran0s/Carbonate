from flask import Flask
from decouple import config
import asyncio
import os

app = Flask(__name__)
app.static_folder = './static'
app.template_folder = './templates'
app.config['SESSION_COOKIE_HTTPONLY'] = True

# INIT RENDERS ROUTING #
from apps.auth.auth_renders import *
from apps.auth.auth_login_renders import *
from apps.auth.auth_register_renders import *
app.register_blueprint(auth_renders)
app.register_blueprint(auth_login_renders)
app.register_blueprint(auth_register_renders)

from apps.home.home_renders import *
app.register_blueprint(home_renders)

from apps.stripe.stripe_renders import *
from apps.stripe.stripe_api import *
from apps.stripe.stripe_models import *
app.register_blueprint(stripe_renders)
app.register_blueprint(stripe_api)

from apps.marketing.marketing_api import *
app.register_blueprint(marketing_api)

from apps.user.user_renders import *
from apps.user.user_api import *
app.register_blueprint(user_renders)
app.register_blueprint(user_api)

from apps.restrictions.restrictions_renders import *
app.register_blueprint(restrictions_renders)


# SECRET KEYS #
app.secret_key = config('SECRET_KEY')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5067))
    app.run(host='0.0.0.0', port=port)