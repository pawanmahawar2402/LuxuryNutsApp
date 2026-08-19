import hashlib
import hmac
import os
import sqlite3
from datetime import datetime
from pathlib import Path

import razorpay
from dotenv import load_dotenv
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

from products import CATEGORIES, PRODUCTS, PRODUCTS_LIST

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "orders.db"

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")

RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "")

razorpay_client = (
    razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET
    else None
)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            total_amount INTEGER NOT NULL,
            razorpay_order_id TEXT NOT NULL,
            razorpay_payment_id TEXT,
            status TEXT NOT NULL DEFAULT 'created',
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id TEXT NOT NULL,
            product_name TEXT NOT NULL,
            quantity_label TEXT NOT NULL,
            qty INTEGER NOT NULL,
            unit_price INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id)
        );
        """
    )
    conn.commit()
    conn.close()


init_db()


def get_cart():
    return session.setdefault("cart", {})


def cart_details():
    cart = get_cart()
    items = []
    total = 0
    for product_id, qty in cart.items():
        product = PRODUCTS.get(product_id)
        if not product:
            continue
        line_total = product["price"] * qty
        total += line_total
        items.append({**product, "qty": qty, "line_total": line_total})
    return items, total


@app.route("/")
def index():
    products_by_category = {
        category: [p for p in PRODUCTS_LIST if p["category"] == category] for category in CATEGORIES
    }
    cart_count = sum(get_cart().values())
    return render_template("index.html", products_by_category=products_by_category, cart_count=cart_count)


@app.route("/cart/add/<product_id>", methods=["POST"])
def add_to_cart(product_id):
    if product_id not in PRODUCTS:
        flash("Product not found.")
        return redirect(url_for("index"))
    try:
        qty = max(1, int(request.form.get("qty", 1)))
    except ValueError:
        qty = 1
    cart = get_cart()
    cart[product_id] = cart.get(product_id, 0) + qty
    session["cart"] = cart
    flash(f"Added {PRODUCTS[product_id]['name']} to cart.")
    return redirect(url_for("index"))


@app.route("/cart")
def view_cart():
    items, total = cart_details()
    return render_template("cart.html", items=items, total=total)


@app.route("/cart/remove/<product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = get_cart()
    cart.pop(product_id, None)
    session["cart"] = cart
    return redirect(url_for("view_cart"))


@app.route("/cart/update/<product_id>", methods=["POST"])
def update_cart(product_id):
    cart = get_cart()
    try:
        qty = int(request.form.get("qty", 1))
    except ValueError:
        qty = 1
    if qty <= 0:
        cart.pop(product_id, None)
    else:
        cart[product_id] = qty
    session["cart"] = cart
    return redirect(url_for("view_cart"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, total = cart_details()
    if not items:
        flash("Your cart is empty.")
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()

        errors = []
        if not name:
            errors.append("Name is required.")
        if not phone.isdigit() or len(phone) != 10:
            errors.append("Enter a valid 10-digit phone number.")
        if not address:
            errors.append("Delivery address is required.")

        if errors:
            for e in errors:
                flash(e)
            return render_template(
                "checkout.html", items=items, total=total, name=name, phone=phone, address=address
            )

        if not razorpay_client:
            flash("Payment gateway is not configured yet. Set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET.")
            return render_template(
                "checkout.html", items=items, total=total, name=name, phone=phone, address=address
            )

        amount_paise = total * 100
        razorpay_order = razorpay_client.order.create(
            {"amount": amount_paise, "currency": "INR", "payment_capture": 1}
        )

        conn = get_db()
        cur = conn.execute(
            """INSERT INTO orders
               (customer_name, phone, address, total_amount, razorpay_order_id, status, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (name, phone, address, total, razorpay_order["id"], "created", datetime.utcnow().isoformat()),
        )
        order_id = cur.lastrowid
        for item in items:
            conn.execute(
                """INSERT INTO order_items
                   (order_id, product_id, product_name, quantity_label, qty, unit_price)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (order_id, item["id"], item["name"], item["quantity_label"], item["qty"], item["price"]),
            )
        conn.commit()
        conn.close()

        return render_template(
            "pay.html",
            razorpay_key_id=RAZORPAY_KEY_ID,
            razorpay_order_id=razorpay_order["id"],
            amount_paise=amount_paise,
            name=name,
            phone=phone,
            address=address,
            order_id=order_id,
        )

    return render_template("checkout.html", items=items, total=total, name="", phone="", address="")


@app.route("/payment/verify", methods=["POST"])
def verify_payment():
    order_id = request.form.get("order_id")
    razorpay_order_id = request.form.get("razorpay_order_id")
    razorpay_payment_id = request.form.get("razorpay_payment_id")
    razorpay_signature = request.form.get("razorpay_signature")

    conn = get_db()
    order = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()

    if not order or order["razorpay_order_id"] != razorpay_order_id:
        conn.close()
        return jsonify({"status": "failed", "message": "Order mismatch."}), 400

    generated_signature = hmac.new(
        RAZORPAY_KEY_SECRET.encode(),
        f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(generated_signature, razorpay_signature or ""):
        conn.execute("UPDATE orders SET status = ? WHERE id = ?", ("failed", order_id))
        conn.commit()
        conn.close()
        return jsonify({"status": "failed", "message": "Signature verification failed."}), 400

    conn.execute(
        "UPDATE orders SET status = ?, razorpay_payment_id = ? WHERE id = ?",
        ("paid", razorpay_payment_id, order_id),
    )
    conn.commit()
    conn.close()

    session["cart"] = {}
    return jsonify({"status": "success", "redirect": url_for("order_success", order_id=order_id)})


@app.route("/order/<int:order_id>/success")
def order_success(order_id):
    conn = get_db()
    order = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    items = conn.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,)).fetchall()
    conn.close()
    if not order:
        flash("Order not found.")
        return redirect(url_for("index"))
    return render_template("success.html", order=order, items=items, products=PRODUCTS)


if __name__ == "__main__":
    app.run(debug=True)
