from prisma import Prisma
import stripe
import yaml
import calendar
import time

from prisma.enums import Plan

def stripe_get_subscription_product(product):
    return stripe.Product.retrieve(product)

def stripe_product_listing():
    with open("apps/stripe/config/stripe_products.yml", "r") as f:
        products_listing = yaml.safe_load(f)
    return products_listing['PRODUCTS_INFOS']

def stripe_product_id():
    with open("apps/stripe/config/stripe_products.yml", "r") as f:
        products_id = yaml.safe_load(f)
    return products_id['PRODUCTS_ID']

async def stripe_create_customer(user):
    """Creat a customer

    Args:
        user (User Object): the user

    Returns:
        customer Object
    """
    async with Prisma() as db:
        customer = await db.customer.create(data={'user_id':user.id})
    return customer

async def stripe_update_customer_id(customer, stripe_customer_id):
    """Update Customer Stripe ID

    Args:
        customer (Customer Object): the customer
        stripe_customer_id (String): the customer Stripe ID

    Returns:
        customer Object
    """
    async with Prisma() as db:
        customer = await db.customer.update(where={'id':customer.id}, data={'stripe_customer_id':stripe_customer_id})
    return customer

async def stripe_update_subscription_id(customer, stripe_subscription_id):
    """Update customer subscription ID

    Args:
        customer (Customer Object): the customer
        stripe_subscription_id (String): the subscription Stripe ID

    Returns:
       Customer Object
    """
    async with Prisma() as db:
        customer = await db.customer.update(where={'user_id':customer.id}, data={'stripe_subscription_id':stripe_subscription_id})
    return customer

async def stripe_update_subscription_data(customer, end_date, interval):
    """Update customer data

    Args:
        customer (Customer Object): the customer

    Returns:
       Customer Object
    """
    async with Prisma() as db:
        customer = await db.customer.update(where={'id':customer.id}, data={'end_date':end_date, 'interval':interval})
    return customer

async def stripe_find_customer_w_user(user):
    """Find customer by his user

    Args:
        user (User Object): the user

    Returns:
        Customer Object
    """
    async with Prisma() as db:
        customer = await db.customer.find_first(where={'user_id':user.id}, include={'user': True})
    return customer

async def stripe_find_user_w_customer(customer):
    """Find user by his customer

    Args:
        customer (Customer Object): the customer

    Returns:
        User Object
    """
    async with Prisma() as db:
        customer = await db.customer.find_unique(where={'id':customer.id})
        user = await db.user.find_unique(where={'id':customer.user_id})
    return user

async def stripe_find_w_stripe_customer_id(stripe_customer_id): # update when it's uses
    """Find customer with Stripe customer ID

    Args:
        stripe_customer_id (String): The Stripe customer ID

    Returns:
        Customer Object
    """
    async with Prisma() as db:
        customer = await db.customer.find_first(where={'stripe_customer_id':stripe_customer_id})
    return customer

async def stripe_find_w_client_reference_id(client_reference_id):
    """Find customer by his client reference ID

    Args:
        client_reference_id (String): the client reference ID his created by defaut at the user creation

    Returns:
        Customer Object
    """
    async with Prisma() as db:
        customer = await db.customer.find_first(where={'client_reference_id':client_reference_id})
    return customer

async def stripe_add_uses(user, used):
    """Add uses to an user

    Args:
        user (User Object)
        used (Int): the number of uses

    Returns:
        Stripe usage
    """
    customer = await stripe_find_customer_w_user(user)

    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)

    usage = stripe.SubscriptionItem.create_usage_record(
        customer.stripe_subscription_id,
        quantity=used,
        timestamp= time_stamp
    )
    return usage