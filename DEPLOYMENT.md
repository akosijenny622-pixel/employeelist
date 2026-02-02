# Deploying Employee Management System to Render

This guide will walk you through deploying your Django Employee Management System to Render.

## Prerequisites

- A GitHub account
- A Render account (free tier available at https://render.com)
- Your project pushed to a GitHub repository

## Step 1: Push Your Code to GitHub

If you haven't already, push your code to GitHub:

```powershell
cd c:\Users\Janna\OneDrive\Desktop\employeelist
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

> [!NOTE]
> If you don't have a Git repository set up yet, initialize one first:
> ```powershell
> git init
> git add .
> git commit -m "Initial commit"
> git branch -M main
> git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
> git push -u origin main
> ```

## Step 2: Create a PostgreSQL Database on Render

1. Go to https://dashboard.render.com
2. Click **"New +"** button
3. Select **"PostgreSQL"**
4. Configure the database:
   - **Name**: `employeelist-db` (or any name you prefer)
   - **Database**: `employeelist`
   - **User**: (auto-generated)
   - **Region**: Choose closest to you
   - **PostgreSQL Version**: 16 (or latest)
   - **Plan**: Free
5. Click **"Create Database"**
6. **IMPORTANT**: Copy the **Internal Database URL** - you'll need this later

## Step 3: Create a Web Service on Render

1. On Render Dashboard, click **"New +"** button
2. Select **"Web Service"**
3. Connect your GitHub repository:
   - Click **"Connect account"** if you haven't connected GitHub
   - Find and select your `employeelist` repository
   - Click **"Connect"**

## Step 4: Configure the Web Service

Fill in the following settings:

### Basic Settings
- **Name**: `employeelist` (or your preferred name)
- **Region**: Same as your database
- **Branch**: `main`
- **Root Directory**: Leave blank
- **Runtime**: `Python 3`

### Build & Deploy Settings
- **Build Command**: `./build.sh`
- **Start Command**: `cd config && gunicorn config.wsgi:application`

### Plan
- Select **"Free"** tier

## Step 5: Set Environment Variables

Scroll down to the **Environment Variables** section and add the following:

| Key | Value | Notes |
|-----|-------|-------|
| `SECRET_KEY` | (Generate a random string) | Use https://djecrety.ir/ to generate |
| `DEBUG` | `False` | **Must be False for production** |
| `ALLOWED_HOSTS` | `.onrender.com` | Allows all Render subdomains |
| `DATABASE_URL` | (Paste Internal Database URL) | From Step 2 |
| `RENDER_EXTERNAL_URL` | `https://YOUR-APP-NAME.onrender.com` | Replace with your actual URL |

> [!IMPORTANT]
> For `SECRET_KEY`, generate a new secure random key. You can use https://djecrety.ir/ or run this Python command:
> ```python
> from django.core.management.utils import get_random_secret_key
> print(get_random_secret_key())
> ```

> [!WARNING]
> **Never use the default SECRET_KEY from settings.py in production!**

### Example RENDER_EXTERNAL_URL
If your app name is `employeelist`, your URL would be:
```
https://employeelist.onrender.com
```

## Step 6: Deploy

1. Click **"Create Web Service"** at the bottom
2. Render will automatically:
   - Clone your repository
   - Run `build.sh` (install dependencies, collect static files, migrate database)
   - Start the application with Gunicorn
3. Wait for deployment to complete (first deployment may take 5-10 minutes)

## Step 7: Create a Superuser

After deployment succeeds, you need to create an admin account:

1. In your Render Dashboard, go to your web service
2. Click **"Shell"** in the left sidebar
3. Run these commands:
   ```bash
   cd config
   python manage.py createsuperuser
   ```
4. Follow the prompts to create your admin account:
   - Username: (your choice)
   - Email: (your email)
   - Password: (secure password)
   - Password (again): (confirm)

## Step 8: Access Your Application

1. Click the URL at the top of your Render service page (e.g., `https://employeelist.onrender.com`)
2. You should see the login page
3. Log in with the superuser credentials you just created

## Step 9: Add Employee Data

Since you're starting with a fresh database:

1. Log in as the superuser
2. Navigate to the admin dashboard
3. Create employee records as needed

> [!TIP]
> **Migrating Data from SQLite (Optional)**
>
> If you want to migrate existing data from your local SQLite database:
> 1. Export data: `python manage.py dumpdata --exclude auth.permission --exclude contenttypes > data.json`
> 2. Upload `data.json` to your repository
> 3. In Render Shell: `python manage.py loaddata data.json`

## Troubleshooting

### Application Error / 500 Error

1. Check the **Logs** tab in Render Dashboard
2. Common issues:
   - Missing environment variables
   - Database connection failed
   - Static files not collected

### Static Files Not Loading

1. Verify `build.sh` ran successfully (check logs)
2. Ensure `STATIC_ROOT` is set correctly in settings.py
3. Check that WhiteNoise middleware is properly configured

### Database Connection Error

1. Verify `DATABASE_URL` is set correctly in environment variables
2. Make sure you copied the **Internal Database URL** (not External)
3. Check that your PostgreSQL database is running

### CSRF Verification Failed

1. Check that `RENDER_EXTERNAL_URL` is set correctly
2. Ensure it matches your actual Render app URL
3. Verify `CSRF_TRUSTED_ORIGINS` includes your Render URL

## Updating Your Application

When you make changes to your code:

```powershell
git add .
git commit -m "Description of changes"
git push origin main
```

Render will automatically detect the push and redeploy your application.

## Free Tier Limitations

> [!CAUTION]
> **Render Free Tier Limitations:**
> - Service spins down after 15 minutes of inactivity
> - First request after spin-down may take 30-60 seconds
> - 750 hours/month of runtime
> - PostgreSQL database has 1GB storage limit
> - Best for development/testing, not production

## Next Steps

✅ Your application is now live on Render!

Consider:
- Setting up automatic backups for your PostgreSQL database
- Upgrading to a paid tier for production use (no spin-down, better performance)
- Setting up a custom domain
- Configuring monitoring and alerts

## Support

If you encounter issues:
1. Check Render's logs (Logs tab in dashboard)
2. Review Render documentation: https://render.com/docs
3. Check Django deployment checklist: `python manage.py check --deploy`
