# Proiect 3 — Website cu Django

Un magazin online minimal (`pyshop`), construit pentru a înțelege structura unui proiect
Django: proiect → aplicație → model → view → template.

## Structura

```
manage.py
pyshop/                  # configurarea proiectului (settings, urls, wsgi)
products/                # aplicația propriu-zisă
├── models.py            # Product (nume, preț, stoc, imagine) și Offer (cod, descriere, discount)
├── views.py             # index — listează produsele; new — pagină simplă
├── urls.py              # rutele aplicației
├── admin.py             # înregistrarea modelelor în panoul de admin
├── migrations/          # 0001_initial, 0002_offer
└── templates/index.html # lista de produse
templates/base.html      # layout comun (Bootstrap)
db.sqlite3               # baza de date de test, cu produsele demo
```

`views.index` face `Product.objects.all()` și trimite lista către `index.html`, care o
randează sub forma unor carduri.

## Rulare

```bash
pip install django
python manage.py migrate
python manage.py runserver
```

Aplicația pornește pe <http://127.0.0.1:8000/>. Pentru panoul de admin
(`/admin`) e nevoie de un superuser creat local cu `python manage.py createsuperuser`.
