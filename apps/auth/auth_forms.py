from wtforms import Form, BooleanField, StringField, validators
from apps.translate.translate_engine import contents

class RegisterForm(Form):
    email = StringField('Email Address', [validators.DataRequired(), validators.Length(min=6, max=35), validators.Email(message=(contents["email_not_OK"]))], render_kw={"placeholder": contents["email_placeholder"]})
    name = StringField('Your Name', [validators.DataRequired(), validators.regexp("^\w+$", message=(contents['use_numbers_or_letters']))], render_kw={"placeholder": contents["name_placeholder"]})
    surname = StringField('Your Name', [validators.DataRequired(), validators.regexp("^\w+$", message=(contents['use_numbers_or_letters']))], render_kw={"placeholder": contents["surname_placeholder"]})
    optinNL = BooleanField('OptinNL', render_kw={"placeholder": contents['optinNL_placeholder']})
    terms = BooleanField('Terms', [validators.DataRequired()], render_kw={"placeholder": contents['terms_placeholder']})

class LoginForm(Form):
    email = StringField('Email Address', [validators.DataRequired(), validators.Length(min=6, max=35), validators.Email(message=(contents['email_not_OK']))], render_kw={"placeholder": contents['email_placeholder']})