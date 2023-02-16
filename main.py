# IMPORTS
import json
from flask import Flask, render_template as rt, url_for, request, redirect
from forms import *

from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, logout_user, current_user, UserMixin
import uuid

from _global import *

# SETUP
app = Flask(__name__)
app.config["SECRET_KEY"] = str(uuid.uuid4())
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"


# =================
#  USER MANAGEMENT
# =================
class User(UserMixin):

    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data

    def get_id(self):
        return self.user_data["id"]


@login_manager.user_loader
def load_user(user_id):
    return User(db.fetch_one_from_table("users", "id", user_id))


# ========
#  ROUTES
# ========


# HOME PAGE
@app.route("/", methods=["GET"])
def home_page():
    return rt("index.html", current_user=current_user)


# ABOUT PAGE
@app.route("/about", methods=["GET"])
def about_page():
    return rt("about.html", current_user=current_user)


# LOGIN PAGE
@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        user = db.fetch_one_from_table("users", "username",
                                       str(form.username.data))
        if user:
            if bcrypt.check_password_hash(user["password"],
                                          form.password.data):
                login_user(User(user))
                return redirect(url_for("brands_page"))
        else:
            return redirect(url_for("register_page"))

    return rt("login.html", form=form)


# LOGOUT ROUTE
@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login_page"))


# REGISTER PAGE
@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        db.add_to_table(
            "users", {
                "username": form.username.data,
                "password": hashed_password.decode("utf8"),
                "cart": [],
                "orders": []
            })

        return redirect(url_for("login_page"))

    return rt("register.html", form=form)


# BRANDS PAGE
@app.route("/brands", methods=["GET"])
def brands_page():
    return rt("brands.html", brands=db.fetch_all_from_table("brands"))


# BRAND PRODUCTS PAGE
@app.route("/<brand_name>/products", methods=["GET"])
def brand_products_page(brand_name):
    brand_name = brand_name.capitalize()

    products = db.fetch_all_from_table("products", "brand", brand_name)
    brand = db.fetch_one_from_table("brands", "name", brand_name)

    return rt("brand_products.html",
              props={
                  'products': products,
                  'brand': brand,
                  'current_user': current_user,
              })


# PRODUCT VIEW PAGE
@app.route("/<brand_name>/products/<product_id>", methods=["GET", "POST"])
def product_page(brand_name, product_id):
    product = db.fetch_one_from_table("products", "id", product_id)
    form = ProductForm()

    if form.is_submitted():
        qty = request.args.get("qty") or 1
        current_user_data = None

        try:
            current_user_data = current_user.user_data
        except:
            return redirect(url_for("login_page"))

        current_user_data['cart'].append({"product": product, "qty": qty})
        db.update_on_table("users", current_user_data['username'],
                           current_user_data)
        current_user.user_data = current_user_data

        return redirect(url_for("cart_page"))

    return rt("product.html",
              props={
                  'product': product,
                  'qty': request.args.get("qty") or 1,
                  'current_user': current_user,
                  'form': form
              })


# CART PAGE
@app.route("/cart", methods=["GET", "POST"])
def cart_page():
    if current_user.is_authenticated:
        form = CartForm()
        catch_update = {
            'id': request.args.get("id"),
            'qty': request.args.get("qty")
        }

        for i, item in enumerate(current_user.user_data["cart"]):
            if item["product"]["id"] == catch_update["id"]:
                if int(catch_update["qty"]) == 0:
                    del current_user.user_data["cart"][i]
                    break

                item["qty"] = catch_update["qty"]
                break

        db.update_on_table("users", current_user.user_data['username'],
                        current_user.user_data)

        if form.is_submitted():
            price = 0

            for item in current_user.user_data["cart"]:
                price += float(item["product"]["price"]) * int(item["qty"])
                print(price,
                    float(item["product"]["price"]) * int(item["qty"]))

            return redirect(url_for("payment_page", price=price))

        return rt("cart.html",
                props={
                    'current_user': current_user,
                    'form': form,
                })
    else:
        return redirect(url_for("login_page"))


# ORDER PAGE
@app.route("/orders", methods=["GET"])
def order_page():
    if current_user.is_authenticated:
        return rt("orders.html", current_user=current_user)
    else:
        return redirect(url_for("login_page"))


# PAYMENT PAGE
@app.route("/payment", methods=["GET", "POST"])
def payment_page():
    form = PaymentForm()
    item_price = request.args.get("price")

    if form.validate_on_submit():
        # ADD TO ORDERS PAGE
        current_user.user_data["orders"].append(current_user.user_data["cart"])
        current_user.user_data["cart"] = []
        db.update_on_table("users", current_user.user_data['username'],
                           current_user.user_data)

        # REDIRECT TO SUCCESS PAGE
        return redirect(url_for("payment_success_page"))

    return rt("payment.html", props={'form': form, 'item_total': item_price})


# PAYMENT SUCCESS PAGE
@app.route("/paymentsuccess", methods=["GET", "POST"])
def payment_success_page():
    form = SuccessReturnForm()
    if form.is_submitted():
        return redirect(url_for("brands"))
    return rt("payment_success.html", form=form)


# STATIC URLS
with app.test_request_context():
    url_for("static", filename="")

# RUN APPLICATION ON PORT 5000
app.run(debug=True)