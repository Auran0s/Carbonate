from wtforms import Form, BooleanField, StringField, validators
from apps.translate.translate_engine import contents

class UpdateEmail(Form):
    email = StringField('Email Address', [validators.DataRequired(), validators.Length(min=6, max=35), validators.Email(message=(contents['email_not_OK']))], render_kw={"placeholder": contents['email_placeholder']})

class UpdateData(Form):
    name = StringField('Your Name', [validators.DataRequired(), validators.regexp("^\w+$", message=(contents['use_numbers_or_letters']))], render_kw={"placeholder": contents['name_placeholder']})
    surname = StringField('Your Surame', [validators.DataRequired(), validators.regexp("^\w+$", message=(contents['use_numbers_or_letters']))], render_kw={"placeholder": contents['surname_placeholder']})
    optinNLTrue = BooleanField('OptinNL', render_kw={"placeholder": contents['optinNL_placeholder']}, default=True)
    optinNLFalse = BooleanField('OptinNL', render_kw={"placeholder": contents['optinNL_placeholder']}, default=False)