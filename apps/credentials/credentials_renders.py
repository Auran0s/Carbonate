from flask import Blueprint, render_template, session, redirect, url_for, flash

from apps.user.user_models import *
from apps.auth.auth_api import *
from apps.stripe.stripe_api import *

from apps.translate.translate_engine import contents

credentials_renders = Blueprint('credentials_renders', __name__,
template_folder='templates')