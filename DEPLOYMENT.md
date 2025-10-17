# 🚀 Deployment Guide

## Quick Deploy Options

### 1️⃣ Heroku (Easiest)

```bash
# Login to Heroku
heroku login

# Create new app
heroku create crypto-tracker-app

# Deploy
git push heroku main

# Open app
heroku open

# View logs
heroku logs --tail
```

**Required Files**: ✅ Procfile, ✅ requirements.txt, ✅ runtime.txt

### 2️⃣ Railway.app

1. Visit [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Railway auto-detects Flask and deploys
5. Get your URL from dashboard

**Pros**: Free tier, auto-deploys on push, no config needed

### 3️⃣ Render

1. Visit [render.com](https://render.com)
2. New → Web Service
3. Connect GitHub repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn app:app`

### 4️⃣ PythonAnywhere

```bash
# 1. Upload code via Files tab
# 2. Open Bash console
cd flask_web_scraper
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Web tab → Add new web app
# 4. Choose Flask, Python 3.11
# 5. Set source code directory
# 6. Edit WSGI file:

import sys
path = '/home/yourusername/flask_web_scraper'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

### 5️⃣ Docker

```bash
# Build
docker build -t crypto-tracker .

# Run locally
docker run -p 5000:5000 crypto-tracker

# Push to Docker Hub
docker tag crypto-tracker yourusername/crypto-tracker
docker push yourusername/crypto-tracker

# Deploy on any cloud with Docker support
```

### 6️⃣ Google Cloud Run

```bash
# Install gcloud CLI
gcloud init

# Build and deploy
gcloud run deploy crypto-tracker \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### 7️⃣ AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 crypto-tracker

# Create environment and deploy
eb create crypto-env
eb open
```

### 8️⃣ DigitalOcean App Platform

1. Create account at [digitalocean.com](https://digitalocean.com)
2. App Platform → Create App
3. Connect GitHub repo
4. Auto-detects Python/Flask
5. Deploy!

## Environment Variables

For production, set these:
```bash
SECRET_KEY=your-production-secret-key-here
FLASK_ENV=production
DATABASE_URL=sqlite:///crypto_data.db
```

## Post-Deployment Checklist

- [ ] App loads without errors
- [ ] Database is created
- [ ] Crypto prices are fetching
- [ ] News is loading
- [ ] Refresh button works
- [ ] API endpoint responds
- [ ] Auto-refresh is working
- [ ] Mobile responsive
- [ ] SSL/HTTPS enabled
- [ ] Custom domain (optional)

## Monitoring

### Check if app is running:
```bash
curl https://your-app-url.com/api/crypto
```

### View logs:
- **Heroku**: `heroku logs --tail`
- **Railway**: Dashboard → Deployments → Logs
- **Render**: Dashboard → Logs tab

## Troubleshooting

**Issue**: Database not persisting
- Solution: Use PostgreSQL for production or mount volume for SQLite

**Issue**: Scheduler not running
- Solution: Ensure worker dyno is running (Heroku) or use external cron

**Issue**: API rate limiting
- Solution: Add delays between requests or use paid API tiers

## Free Hosting Summary

| Platform | Free Tier | Auto-deploy | Database | Best For |
|----------|-----------|-------------|----------|----------|
| Heroku | 550 hrs/mo | ✅ | ✅ Postgres | Quick deploys |
| Railway | $5 credit | ✅ | ✅ Any | Modern apps |
| Render | 750 hrs/mo | ✅ | ✅ Postgres | Full features |
| PythonAnywhere | Limited | ❌ | ✅ SQLite | Python projects |
| Vercel | Unlimited | ✅ | ❌ External | Static/JAMstack |

## Production Optimizations

1. **Use Production Database**
   ```python
   # PostgreSQL instead of SQLite
   app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
   ```

2. **Enable Caching**
   ```python
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'simple'})
   ```

3. **Add Rate Limiting**
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, default_limits=["200 per day"])
   ```

4. **Compress Responses**
   ```python
   from flask_compress import Compress
   Compress(app)
   ```

---

🎉 **Your app is now live!** Share the URL and impress everyone!
