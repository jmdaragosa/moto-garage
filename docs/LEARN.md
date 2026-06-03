# How this project teaches you Django

You are not here to memorize Django — you are learning **how web apps think**:

1. **Data** (models + database)
2. **Rules** (validation, who owns what)
3. **HTTP** (URLs → views → templates)
4. **Auth** (only you see your bikes)

Work through `YOUR_TURN.md` in order. Use admin as a sandbox until your UI exists.

---

## Project layout (what each folder is)

| Path | Role |
|------|------|
| `manage.py` | CLI entry point: runserver, migrate, createsuperuser |
| `config/` | Project settings, root URLs, WSGI |
| `garage/` | Your app: models, views, forms, admin |
| `templates/` | HTML with Django template language |
| `static/` | CSS/JS served as static files |
| `docs/` | Learning guides (you are here) |

**Mental model:** `config` = wiring; `garage` = your product.

---

## Models (read `garage/models.py`)

A **model** is a Python class → a **table** in the database.

| Concept | In this project |
|---------|-----------------|
| `CharField`, `DateField`, … | Column types |
| `ForeignKey` | Link rows together (event → motorcycle) |
| `related_name` | Reverse lookup: `bike.maintenance_events.all()` |
| `TextChoices` | Enum-like strings (`diy` / `shop`) |
| `clean()` | Validation before save |
| `save()` | Hook to update odometer after logging service |

**Try in Django shell** (after Exercise 2):

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from garage.models import Motorcycle, MaintenanceEvent, LineItem, ServiceType
from decimal import Decimal

u = User.objects.get(username="you")
bike = Motorcycle.objects.create(user=u, brand="Honda", model="CB500X", year=2020)
event = MaintenanceEvent.objects.create(
    motorcycle=bike,
    service_date="2024-06-01",
    odometer_km=12000,
    title="Oil change",
    service_type=ServiceType.DIY,
)
LineItem.objects.create(
    event=event,
    description="Motul 7100 1L",
    quantity=Decimal("1"),
    unit_cost=Decimal("850.00"),
)
event.total_php  # should reflect line items
bike.current_odometer_km  # should be 12000
```

---

## Migrations

When you change `models.py`, Django needs a **migration** (recipe to alter tables):

```bash
python manage.py makemigrations
python manage.py migrate
```

**Rule:** never edit applied migrations by hand until you understand them. Generate new ones instead.

---

## Admin

`/admin/` is Django’s built-in staff UI. You registered models in `garage/admin.py`.

Use it to:

- Confirm fields feel right
- Log real maintenance while learning
- See validation errors (e.g. Shop without shop name)

---

## Views & URLs (you will build these)

| Piece | Job |
|-------|-----|
| `urls.py` | Map path → view |
| `view` | Run logic, return `render()` or redirect |
| `template` | HTML + `{{ variables }}` |

**Class-based views (CBVs)** save boilerplate for CRUD. Official tutorial:
https://docs.djangoproject.com/en/stable/topics/class-based-views/

---

## Forms (you will build these)

**ModelForm** = HTML form ↔ model fields.

**Formset** = multiple `LineItem` rows on one maintenance form.

Docs:

- https://docs.djangoproject.com/en/stable/topics/forms/
- https://docs.djangoproject.com/en/stable/topics/forms/modelforms/
- https://docs.djangoproject.com/en/stable/topics/forms/formsets/

---

## Security habits (single-user app, still public when deployed)

1. Filter querysets: `Motorcycle.objects.filter(user=request.user)`
2. On create, set `user=request.user` in the view — never trust hidden form fields
3. Use `@login_required` or `LoginRequiredMixin`
4. `DEBUG=False` and real `SECRET_KEY` in production

---

## PHP and km in the UI (later)

- Store money as `Decimal` (already done on `LineItem`)
- Display with a template filter or `locale` formatting (Exercise 10)
- Always label odometer fields **km**

---

## Deploy (later phase)

Rough path: GitHub → Render web service → Neon Postgres → set env vars.

See `README.md` § Deploy when you reach Exercise 12.

---

## When you are stuck

1. Read the error traceback **bottom to top**
2. Check `docs/YOUR_TURN.md` hints for that exercise
3. Django docs search: https://docs.djangoproject.com/
4. Ask in chat with: what you tried, the error, which exercise number
