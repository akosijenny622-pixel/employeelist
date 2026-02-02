# Creating Admin Account

This guide explains how to create an admin/superuser account for your Django application on Render.

## Method 1: Using Render Shell (Recommended)

1. Go to your [Render Dashboard](https://dashboard.render.com)
2. Click on your web service (`employeelist`)
3. Click on **Shell** in the left sidebar
4. Run the following commands:

```bash
cd config
python manage.py create_admin --username admin --email admin@example.com --password YourSecurePassword123
```

Replace `YourSecurePassword123` with your desired password.

## Method 2: Using Environment Variables

You can set environment variables in Render and the superuser will be created automatically:

1. Go to your Render Dashboard → Your Web Service
2. Go to **Environment** tab
3. Add these environment variables:
   - `DJANGO_SUPERUSER_USERNAME`: `admin`
   - `DJANGO_SUPERUSER_EMAIL`: `admin@example.com`  
   - `DJANGO_SUPERUSER_PASSWORD`: `YourSecurePassword123`

4. In Render Shell, run:
```bash
cd config
python manage.py create_admin
```

## Method 3: Django's Default Command

Use Django's built-in interactive command:

```bash
cd config
python manage.py createsuperuser
```

Then follow the prompts to enter:
- Username
- Email (optional)
- Password

## After Creating Admin

1. Visit: `https://employeelist-mn4y.onrender.com/admin/`
2. Login with your admin credentials
3. You now have full access to the Django admin panel

---

## Custom Command Options

The `create_admin` command supports:

```bash
# With arguments
python manage.py create_admin --username myuser --email user@example.com --password mypass

# With environment variables (set DJANGO_SUPERUSER_* vars first)
python manage.py create_admin

# Help
python manage.py create_admin --help
```

**Note**: The command will not create duplicate users - if the username already exists, it will show a warning message.
