from _global import *
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FileField, TextAreaField, RadioField
from wtforms.validators import InputRequired, ValidationError

from _global import *


class NewProductForm(FlaskForm):
    name = StringField(validators=[InputRequired()])
    description = TextAreaField(validators=[InputRequired()])

    brands = []

    for brand in db.fetch_all_from_table("brands"):
        brands.append(brand["name"])

    brand = RadioField(choices=brands, validators=[InputRequired()])

    price = IntegerField(validators=[InputRequired()])
    qty = IntegerField(validators=[InputRequired()])
    image = FileField(validators=[InputRequired()])
    submit = SubmitField("Create Product")


class NewBrandForm(FlaskForm):
    name = StringField(validators=[InputRequired()])
    image = FileField(validators=[InputRequired()])
    submit = SubmitField("Create Product")


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    address = StringField(validators=[InputRequired()])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        existing_username = db.fetch_one_from_table("users", "username",
                                                    username)
        if existing_username:
            raise ValidationError("Username already exists")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField("Sign In")


class ProductForm(FlaskForm):
    submit = SubmitField("Add to cart")


class CartForm(FlaskForm):
    submit = SubmitField("Proceed to checkout")


class PaymentForm(FlaskForm):
    card_number = StringField(validators=[InputRequired()])
    cvv = StringField(validators=[InputRequired()])
    expiry_date = StringField(validators=[InputRequired()])
    address = StringField(validators=[InputRequired()])
    submit = SubmitField("Make payment")


class SuccessReturnForm(FlaskForm):
    submit = SubmitField("Return to shop")
