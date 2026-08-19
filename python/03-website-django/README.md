# Project 3 — Django Website

A minimal online store (`pyshop`), built to understand the structure of a Django project:
project → app → model → view → template.

> 🇷🇴 Documentul în limba română: [README.ro.md](README.ro.md)

## Structure

```
manage.py
pyshop/                  # project configuration (settings, urls, wsgi)
products/                # the app itself
├── models.py            # Product (name, price, stock, image) and Offer (code, description, discount)
├── views.py             # index — lists the products; new — a simple page
├── urls.py              # the app's routes
├── admin.py             # registering the models in the admin panel
├── migrations/          # 0001_initial, 0002_offer
└── templates/index.html # the product list
templates/base.html      # shared layout (Bootstrap)
db.sqlite3               # the test database, with the demo products
```

`views.index` calls `Product.objects.all()` and passes the list to `index.html`, which renders it as
a set of cards.

## Running

```bash
pip install django
python manage.py migrate
python manage.py runserver
```

The app starts at <http://127.0.0.1:8000/>. The admin panel (`/admin`) needs a superuser created
locally with `python manage.py createsuperuser`.
