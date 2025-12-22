# Django Authentication System

A simple Django authentication system with **email-based registration, email verification, login, logout**, and **automated testing using pytest**.

---

## 🚀 Setup & Run

### 1. Activate virtual environment
```bash
source ./venv/Scripts/activate
```

### 2. Run the development server
```bash
python ./manage.py runserver
```

The server will be available at:
```
http://127.0.0.1:8000/
```

---

## 🔐 Authentication Flow

### Register
- Users register using **email and password**
- A verification email is sent
- The account is activated only after email verification

### Verify Account
- Users enter the verification code received via email
- The account is created and verified

### Login
- Users log in using **email + password**
- Only verified users can log in

---

## 🧪 Automated Testing (pytest)

Run the following commands to test specific features:

```bash
pytest -k "test_register_user"
```

```bash
pytest -k "test_verify_account_valid_code"
```

```bash
pytest -k "test_verify_account_invalid_code"
```

```bash
pytest -k "test_login_valid_credentials"
```

```bash
pytest -k "test_login_invalid_credentials"
```

---

## 🛠 Tech Stack

- Python
- Django
- pytest
- pytest-django
- SQLite (default database)

---

## ✅ Notes

- Email-based authentication
- Passwords are securely hashed
- Email verification required before login
- Fully tested authentication flow
