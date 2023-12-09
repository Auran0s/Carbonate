from flask import Blueprint, redirect, request, url_for, session, flash, current_app, jsonify, make_response
from decouple import config
from functools import wraps
import stripe
import asyncio
import time

from apps.stripe.stripe_models import *
from apps.user.user_models import *
from apps.auth.auth_api import *
from apps.restrictions.restrictions_models import *

stripe.api_key = config('STRIPE_API_KEY')
endpoint_secret = config('STRIPE_ENDPOINT_SECRET')

stripe_api = Blueprint('stripe_api', __name__)

def stripe_need_subscription(f):
    @wraps(f)
    def stripe_wrap(user, *args, **kwargs):
        if user.active_plan is False:
            return "<script>window.location.replace('/billing')</script>"
        return current_app.ensure_sync(f)(user, *args, **kwargs)
    return stripe_wrap

@stripe_api.route('/api/webhooks/stripe', methods=['POST'])
async def stripe_webhooks():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        # Invalid payload or signature
        return jsonify(success=False, error=str(e))

    # Handle the event
    if event['type'] == 'checkout.session.completed': #Event when a customer pass link payment  
        session = event['data']['object']

        if customer := await stripe_find_w_client_reference_id(session['client_reference_id']):
            await stripe_update_customer_id(customer, session['customer'])

    elif event['type'] == 'customer.subscription.updated': #Event if a sbuscription is updated
        session = event['data']['object']
        
        if customer := await stripe_find_w_stripe_customer_id(session['customer']):

            await stripe_update_subscription_id(customer, session['items']['data'][0]['id'])

            productId = stripe_product_id()
            
            user = await user_change_plan(customer, eval(productId[session['items']['data'][0]['plan']['product']]))
            await restrictions_init_uses(user)
            await user_change_active_plan(customer, True)
            
            date = datetime.fromtimestamp(session['current_period_end'])
            formatted_date = date.strftime('%m-%d-%Y')
            
            await stripe_update_subscription_data(customer, formatted_date, session['items']['data'][0]['plan']['interval'])

    elif event['type'] == 'customer.subscription.deleted': #Event if a subscription is deleted
        session = event['data']['object']

        if customer := await stripe_find_w_stripe_customer_id(session['customer']):
            user = await user_change_active_plan(customer, False)

    elif event['type'] == 'invoice.paid': #Event when a payment occur - reset USER uses
        session = event['data']['object']

        if customer := await stripe_find_w_stripe_customer_id(session['customer']):
            user = await stripe_find_user_w_customer(customer)
            await restrictions_reset_uses(user)

    elif event['type'] == 'invoice.payment_failed': #Event when the payment is failed - pass user to NO_ACCOUNT account
        session = event['data']['object']

        if customer := await stripe_find_w_stripe_customer_id(session['customer']):
            user = await user_change_active_plan(customer, False)
    else:
        print(f"Unhandled event type {event['type']}")

    return jsonify(success=True)