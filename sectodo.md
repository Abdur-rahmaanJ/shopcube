# Security Audit: ShopCube

> Generated: June 12, 2026

---

## 🚨 CRITICAL

### 1. SQL Injection via `field` parameter in Product Search ✅ FIXED

**File:** `src/shopcube/modules/box__ecommerce/product/view.py`

**Fix applied:** Added a `_SEARCHABLE_FIELDS` allowlist (`barcode`, `name`, `description`, `date`, `price`, `selling_price`, `in_stock`, `min_stock`, `cost_price`, `discontinued`, `is_onsale`, `is_featured`). The `field` parameter is now validated against this set before being passed to `getattr()`. Invalid fields return a 400 error. Field names are normalized (spaces → underscores) to handle the frontend display format.

---

### 2. Hardcoded/Guessable Secret Key

**File:** `src/shopcube/config.py`

```python
# Development
SECRET_KEY = "secret"

# Production
SECRET_KEY = os.environ.get("SECRET_KEY", "prod-secret-key")
```

The production fallback `"prod-secret-key"` is trivially guessable. If the env var isn't set (common in deployment), Flask's session signing, CSRF tokens, and `itsdangerous` are all compromised.

**Fix:** Remove the fallback default — raise an error if `SECRET_KEY` is not set in production. Generate a strong random key for development.

---

## 🔴 HIGH

### 3. No Ownership/Access Checks (IDOR) ✅ FIXED

**Files:** `shopman/view.py`, `customer/view.py`, `pos/view.py`

**Fixes applied:**
- **`shopman/view.py`** — Replaced `.get()` with `.get_or_404()` on all delete/update operations (orders, delivery options, payment options, coupons) to return 404 for non-existent resources. Admin-level access is already guarded by `@admin_required`.
- **`customer/view.py`** — Added ownership check on `/order/<order_id>/view` that verifies `order.logged_in_customer_email` (or `billing_detail.email` for guest orders) matches `current_user.email` before allowing access. Unauthorized users are redirected with a warning flash.
- **`pos/view.py`** — `/transactions/<tx_id>/view` already used `get_or_404` and is admin-only, so no changes were needed.

---

### 4. Default Admin Password is "pass"

**File:** `wsgi.py` (lines ~106-109)

```python
application.config['SHOPYO_AUTH_SEED_ADMIN_PASSWORD'] = 'pass'
```

The first-run database seed creates an admin account with password `"pass"`. This is trivial to brute force and extremely common in deployed instances.

**Fix:** Generate a strong random password on first-run and print it to the console/require immediate password change.

---

### 5. Stored XSS in Contact Messages

**File:** `src/shopcube/modules/contact/view.py`

```python
name = form.name.data
email = form.email.data
message = form.message.data
contact_message = ContactMessage(name=name, email=email, message=message)
```

User-submitted contact messages are stored and displayed in the admin dashboard without sanitization. While Jinja2 auto-escapes by default, if `|safe` is used in templates or if inserted into JavaScript contexts, this becomes exploitable.

**Fix:** Sanitize HTML on output (e.g., with bleach) or strip HTML tags before storage. Verify templates don't use `|safe` on user data.

---

### 6. Path Traversal in `send_from_directory`

**Files:** `resource/view.py`, `category/view.py`

```python
@module_blueprint.route("/product/<filename>", methods=["GET"])
def product_image(filename):
    return send_from_directory(UPLOADED_PRODUCTPHOTOS_DEST, filename)
```

While `send_from_directory` is generally safe in Werkzeug 2.x, these endpoints serve files from user-controlled filenames without adequate validation that `filename` is a simple filename (not containing `../`).

**Fix:** Validate filename contains no path separators before passing to `send_from_directory`.

---

## 🟡 MEDIUM

### 7. No Rate Limiting on Login/Auth Endpoints

There is no rate limiting on any authentication endpoint. An attacker can brute force login credentials without restriction. No lockout mechanism exists.

**Fix:** Implement rate limiting on login routes (e.g., Flask-Limiter) and/or account lockout after N failed attempts.

---

### 8. Weak Password Policy

- Registration minimum is only **6 characters** (in `shop/forms.py`)
- No requirement for mixed case, numbers, or special characters
- No password history check or rotation enforcement
- No password strength meter

**Fix:** Enforce minimum 8+ characters with complexity requirements. Use a password strength library.
 
---

### 9. Hardcoded Password Salt

```python
PASSWORD_SALT = "abcdefghi"       # BaseConfig
PASSWORD_SALT = "some pasword salt" # DevelopmentConfig (note typo)
```

The salt is hardcoded in config. If using password hashing schemes that rely on this salt (separate from werkzeug's built-in salt), this weakens protection.

**Fix:** Use a unique, randomly generated salt per deployment. Remove hardcoded salts from config.

---

### 10. `request.form["key"]` Instead of `.get("key")`

Multiple views access form data via direct key access (`request.form["key"]`), which raises `KeyError` if the field is missing. This happens in:

- `product/view.py` (lines 96-107, 222-223)
- `shop/view.py` (line 211)
- `category/view.py` (lines 66, 168, 266, etc.)

This can cause 500 errors and potentially bypass validation logic.

**Fix:** Use `request.form.get("key")` with sensible defaults and error handling.

---

### 11. No Security Headers

No security-related HTTP headers are configured:
- ❌ No `Content-Security-Policy`
- ❌ No `X-Content-Type-Options: nosniff`
- ❌ No `X-Frame-Options: DENY`
- ❌ No `Strict-Transport-Security`
- ❌ No `X-XSS-Protection`

**Fix:** Add security headers via Flask middleware or a reverse proxy (nginx/apache).

---

### 12. No Server-side Session Storage

Flask uses **client-side sessions** (signed cookies) by default. All session data (cart, checkout data, wishlist) is stored in the session cookie. While signed, it's not encrypted — the data is only base64-encoded and signed. An attacker who obtains the secret key can decode and tamper with session data.

**Fix:** Use server-side sessions (e.g., Flask-Session with Redis/filesystem).

---

### 13. Mass Assignment Risk in Product Update

**File:** `product/view.py`

```python
p.barcode = barcode
p.name = name
p.description = description
# ... many fields set directly from form data
```

Several fields are set directly from `request.form` without explicit allowlisting. If new fields are added to the model, they might be set from form data without proper validation.

**Fix:** Use form validation to control which fields can be updated. Avoid setting model attributes directly from raw form data.

---

## 🟢 LOW

### 14. Outdated Dependencies

Key packages with known CVEs or outdated versions:
- **Flask 2.2.0** (current stable → 3.x)
- **Werkzeug 2.2.2**
- **SQLAlchemy 1.4.46**
- **Flask-Login 0.6.2**
- **Pillow 9.x/10.x** — has had several CVEs in recent versions

**Fix:** Run `pip-compile --upgrade` and test thoroughly.

---

### 15. Debug Mode Details Exposed in Development

While `DEBUG = True` is normal in development, some endpoints return raw Python errors or tracebacks without a custom error handler.

**Fix:** Ensure custom error pages are configured for 400/403/404/500 in all environments.

---

### 16. Weak Test Credentials in conftest.py

All test fixtures use `password = "pass"` for admin, non-admin, and unconfirmed users. This encourages the same weak password pattern in production configurations.

**Fix:** Use strong random passwords in test fixtures.

---

### 17. Email Configuration Has Placeholder Values

```python
MAIL_DEFAULT_SENDER = "ma@mail.com"
MAIL_USERNAME = ""
MAIL_PASSWORD = ""
```

The development config uses empty/placeholder email credentials which could be accidentally used in non-development environments.

**Fix:** Add environment checks that fail loudly if email config is incomplete in production.

---

## ✅ What's Done Well

- **CSRF protection** is globally enabled via `Flask-WTF`'s `CSRFProtect`
- **`secure_filename`** from Werkzeug is used on file uploads
- **UUID prefix** added to uploaded filenames (prevents overwrite attacks)
- **`login_required`** decorator is used on admin-facing routes
- **Admin-level** routes are protected with `@admin_required`
- **Safe redirect** via `get_safe_redirect()` in shop views
- **SQLAlchemy ORM** (not raw SQL) is used throughout, which parameterizes queries by default
- **Jinja2 auto-escaping** is on by default, mitigating most reflected XSS
- **Migrations** track database schema changes via Alembic
