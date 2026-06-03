# Your turn — exercises (do in order)

Do not skip ahead. Each step teaches one idea. **You** type the code unless it says "already done."

---

## Exercise 1 — Run the project

**Goal:** See the request/response cycle.

```bash
cd /Users/jmdaragosa/Documents/moto-garage
source .venv/bin/activate
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit http://127.0.0.1:8000/ and http://127.0.0.1:8000/admin/

**Check:** Home page loads; you can log into admin.

**Learn:** `migrate` applies DB schema; `runserver` is dev-only.

---

## Exercise 2 — Explore the shell

**Goal:** Manipulate data without a UI.

Follow the shell snippet in `docs/LEARN.md` § Models.

**Check:** One motorcycle, one event, one line item; `event.total_php` is correct.

---

## Exercise 3 — Admin workflow

**Goal:** Use the app like a user (via admin).

1. In admin, add your real (or sample) motorcycle under **Motorcycles**.
   - Set **User** to your superuser.
2. Add a **Maintenance event** with inline line items.
3. Try **Shop** without shop name — confirm validation fails.
4. Add a valid shop service.

**Check:** Motorcycle `current_odometer_km` updated after save.

**Learn:** `ModelAdmin`, `TabularInline`, `clean()` on the model.

---

## Exercise 4 — Read the models

**Goal:** Understand relationships without typing yet.

Open `garage/models.py` and draw on paper:

- Boxes: User, Motorcycle, MaintenanceEvent, LineItem
- Arrows for ForeignKeys

**Question to answer in a comment in your notebook:** What happens if you delete a motorcycle?

<details>
<summary>Hint</summary>
`on_delete=models.CASCADE` on events and line items.
</details>

---

## Exercise 5 — Motorcycle form

**Goal:** First ModelForm.

In `garage/forms.py`, implement `MotorcycleForm` (see commented skeleton).

Requirements:

- All fields except `user`
- Widget for `notes` as `Textarea`

**Check:** In shell, `MotorcycleForm()` renders HTML fields.

---

## Exercise 6 — Create motorcycle view

**Goal:** POST → validate → save → redirect.

1. Create `garage/views/motorcycle.py` OR add to `views.py` a `MotorcycleCreateView` (subclass `LoginRequiredMixin`, `CreateView`).
2. Set `form_class = MotorcycleForm`, `template_name = "garage/motorcycle_form.html"`.
3. Override `form_valid`: `form.instance.user = self.request.user`.
4. Wire URL: `path("motorcycles/new/", ...)`.

**Check:** Logged-in user can create a bike from your site (not only admin).

**Learn:** CBV method flow `get` → `post` → `form_valid`.

Docs: https://docs.djangoproject.com/en/stable/ref/class-based-views/generic-editing/#createview

---

## Exercise 7 — List your motorcycles

**Goal:** Filter by owner.

`MotorcycleListView` with:

```python
def get_queryset(self):
    return Motorcycle.objects.filter(user=self.request.user)
```

Template `garage/motorcycle_list.html` — loop `{% for bike in object_list %}`.

Link from home page to this list.

---

## Exercise 8 — Motorcycle detail + timeline

**Goal:** One bike page with maintenance history.

`MotorcycleDetailView` — show bike fields and `motorcycle.maintenance_events.all` in the template.

Show per event: date, km, title, DIY/Shop, `total_php`.

**Stretch:** Sum all events’ totals for “lifetime spend” on this bike.

---

## Exercise 9 — Login for normal users

**Goal:** Stop using admin login for daily use.

Use Django’s built-in auth views:

- `LoginView` / `LogoutView`
- Templates in `templates/registration/login.html`
- Update `LOGIN_URL` in settings to your login route
- Protect all garage views with `LoginRequiredMixin`

**Check:** Anonymous users hitting `/motorcycles/` get redirected to login.

---

## Exercise 10 — Maintenance event + line item formset

**Goal:** Hardest MVP form — one event, many lines.

1. `MaintenanceEventForm` (exclude `motorcycle` — set in view from URL kwarg).
2. `LineItemFormSet` with `inlineformset_factory(MaintenanceEvent, LineItem, ...)`.
3. Create view at `/motorcycles/<id>/services/new/`.
4. In template, `{{ form }}` and `{{ formset.management_form }}` + loop forms.

**Check:** Saving creates event + lines; shop name required when type is shop.

**Learn:** formsets, `formset.is_valid()` together with `form.is_valid()`.

---

## Exercise 11 — Display PHP nicely

**Goal:** Format money in templates.

Option A: custom template filter `format_php` in `garage/templatetags/`.

Option B: `{% load l10n %}` and locale (more setup).

**Check:** `850` displays as `₱850.00` (or your preferred format).

---

## Exercise 12 — Deploy (when MVP works locally)

**Goal:** Free hosting.

1. Push to GitHub (no `.env` in repo).
2. Create Neon Postgres; set `DATABASE_URL` on Render.
3. Add `gunicorn`, `whitenoise`, `dj-database-url` to requirements.
4. `DEBUG=False`, `ALLOWED_HOSTS`, `collectstatic` in build command.

Document steps you took in `docs/DEPLOY.md` (you write this file).

---

## How to get help without spoon-feeding

When asking for help, include:

1. Exercise number
2. What you expected vs what happened
3. Traceback or screenshot
4. Snippet of *your* code (view or form)

Good: "Exercise 6: CreateView saves but user is null."
Bad: "Django doesn't work."
