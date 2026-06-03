# Moto Garage

Personal **motorcycle** maintenance tracker (PHP, km, DIY or shop per service).

Built with **Django** so you learn web development while shipping something useful.

## Quick start

```bash
cd /Users/jmdaragosa/Documents/moto-garage
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Learning path

| Doc | Purpose |
|-----|---------|
| [docs/YOUR_TURN.md](docs/YOUR_TURN.md) | **Start here** — hands-on exercises |
| [docs/LEARN.md](docs/LEARN.md) | Concepts: models, views, forms, security |

## What is already built vs what you build

| Done for you | You implement (exercises) |
|--------------|---------------------------|
| Models, migrations, validation | — |
| Django admin + inline line items | — |
| Settings, home page shell | Motorcycle CRUD UI |
| Project structure | Maintenance forms + formset |
| | Login, dashboard, deploy |

## Domain summary

- **Motorcycle** — brand, model, year, odometer (km), owned by one user
- **MaintenanceEvent** — date, km, DIY/shop, optional shop name
- **LineItem** — parts/labor/fees in PHP; `amount = quantity × unit_cost`

## Deploy (later)

See Exercise 12 in `docs/YOUR_TURN.md`. Target: Render + Neon (free tiers).
