from flask import Blueprint, render_template, session, redirect, url_for

from apps.home.home_models import *

from apps.auth.auth_api import *

from apps.user.user_models import *

from apps.stripe.stripe_api import *

from apps.translate.translate_engine import contents

restrictions_renders = Blueprint('restrictions_renders', __name__,
template_folder='templates')