from flask import Blueprint, redirect, render_template
from decouple import config
import stripe
import yaml

from apps.auth.auth_api import *
from .stripe_models import *
from .stripe_api import *

from apps.translate.translate_engine import contents

stripe.api_key = config('STRIPE_API_KEY')

stripe_renders = Blueprint('stripe_renders', __name__)

@stripe_renders.route('/billing/')
@auth_user
async def stripe_choice_subscription_page(user):
    if user.customer.stripe_customer_id is None:
        return render_template('pages/page_stripe_plans.html', products=stripe_product_listing(), user=user, customer=user.customer, content=contents)
    if user.customer.stripe_customer_id:
        if user.active_plan != False:
            return redirect(url_for('home_renders.home_root_page'))
        flash(contents['stripe_plan_expired'])
        return render_template('pages/page_stripe_plans.html', products=stripe_product_listing(), user=user, customer=user.customer, content=contents)
        
@stripe_renders.route('/welcome/')
@auth_user
async def stripe_waiting_subscription(user):
    resp = make_response(render_template('pages/page_welcome.html', content=contents, user=user))
    resp.headers['Refresh'] = '1;url=/'
    return resp
    
@stripe_renders.route('/create-customer-portal-session/', methods=['POST'])
@auth_user
async def stripe_customer_portal_page(user):
    session = stripe.billing_portal.Session.create(
        customer=user.customer.stripe_customer_id,
        return_url=config('APP_DOMAIN'),
    )
    return redirect(session.url)

@stripe_renders.route('/create-checkout-session/', methods=['POST'])
@auth_user
async def stripe_checkout_session_page(user):
    price_id = request.form.get('priceId')
    
    session = stripe.checkout.Session.create(
    success_url=f"{config('APP_DOMAIN')}welcome",
    mode='subscription',
    line_items=[{
        'price': price_id,
        # For metered billing, do not pass quantity
        'quantity': 1
    }],
    client_reference_id=user.customer.client_reference_id,
    customer_email=user.email
    )
    # Redirect to the URL returned on the session
    return redirect(session.url)