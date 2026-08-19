# Luxury Tree Nuts & Dry Fruits — Ordering App

A Flask web app for browsing the product catalog, building a cart,
capturing customer details, and paying online via Razorpay.

## Features

- Product catalog loaded from `products.py` (from the rate list dated 17 Aug 2026)
- Session-based shopping cart (add / update / remove items)
- Checkout form that captures **Name, Phone Number, and Delivery Address**
  before payment
- Razorpay Checkout integration (order creation + server-side signature
  verification, so payments can't be spoofed from the browser)
- Orders and order items persisted to a local SQLite database (`orders.db`)

## Setup

```bash
cd luxury-nuts-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and fill in:

- `FLASK_SECRET_KEY` — any random string (used to sign session cookies)
- `RAZORPAY_KEY_ID` / `RAZORPAY_KEY_SECRET` — from your
  [Razorpay Dashboard](https://dashboard.razorpay.com/) → Settings → API Keys.
  Use the **Test Mode** keys first to try the flow with test cards before
  going live.

## Run

```bash
python app.py
```

Visit http://127.0.0.1:5000 — the SQLite database and tables are created
automatically on first run.

## How the payment flow works

1. Customer adds products to cart and goes to Checkout.
2. Customer enters Name, Phone, and Delivery Address (validated server-side).
3. The server creates a Razorpay Order (`/checkout` POST) and stores a
   `created` order row + line items in SQLite.
4. The `pay.html` page opens Razorpay's Checkout widget with that order id.
5. On successful payment, Razorpay returns a payment id + signature to the
   browser, which is POSTed to `/payment/verify`.
6. The server recomputes the HMAC-SHA256 signature using your Razorpay
   secret and only marks the order `paid` if it matches — this is what
   prevents a customer from faking a successful payment.
7. The customer is redirected to an order confirmation page.

## Going to production

- Switch to your **Live Mode** Razorpay keys once testing is done.
- Serve over HTTPS (required by Razorpay for live mode).
- Consider also registering a
  [Razorpay webhook](https://razorpay.com/docs/webhooks/) pointing at a new
  endpoint as a second, server-to-server confirmation of payment status —
  useful if a customer closes the browser right after paying, before the
  client-side handler fires.
- Replace the dev Flask server (`app.run`) with a production WSGI server
  such as `gunicorn` behind a reverse proxy (e.g. `gunicorn app:app`).
- Update prices in `products.py` whenever the rate list changes.

## Project structure

```
luxury-nuts-app/
├── app.py              # Flask routes: catalog, cart, checkout, payment verification
├── products.py         # Product catalog data
├── requirements.txt
├── .env.example
├── templates/
│   ├── base.html
│   ├── index.html       # Product catalog
│   ├── cart.html
│   ├── checkout.html     # Name / phone / address form
│   ├── pay.html          # Razorpay Checkout widget
│   └── success.html
└── static/
    └── style.css
```
