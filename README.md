# 🚀 Live Crypto Price Tracker - Web Scraping Project

A dynamic Flask web application that scrapes live cryptocurrency prices and news from multiple sources, stores data in a SQLite database, and displays it with an elegant UI. Features automated updates using APScheduler (cron job alternative).

## 📋 Features

✅ **Live Data Scraping**: Fetches real-time crypto prices from CoinGecko API  
✅ **News Aggregation**: Scrapes latest crypto news from CoinDesk  
✅ **Database Storage**: SQLite database with SQLAlchemy ORM  
✅ **Auto-Updates**: Background scheduler updates data every 5 minutes  
✅ **REST API**: JSON endpoint for crypto data (`/api/crypto`)  
✅ **Responsive UI**: Modern, mobile-friendly design  
✅ **Manual Refresh**: On-demand data refresh button  
✅ **Debug Mode**: `/debug` endpoint for troubleshooting  

## 🛠️ Tech Stack

- **Backend**: Flask 3.0
- **Database**: SQLite + SQLAlchemy
- **Scraping**: BeautifulSoup4, Requests
- **Scheduler**: APScheduler (Cron alternative)
- **Frontend**: HTML5, CSS3, Font Awesome
- **Deployment**: Gunicorn ready

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/flask_web_scraper.git
cd flask_web_scraper
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## 🔧 Configuration

### Scheduler Settings
Edit `app.py` to change update frequency:
```python
scheduler.add_job(func=fetch_all_data, trigger="interval", minutes=5)  # Change minutes
```

### Database Location
Change database path in `app.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crypto_data.db'
```

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main page with crypto prices and news |
| `/refresh` | GET | Manual data refresh |
| `/api/crypto` | GET | JSON API for crypto data |
| `/debug` | GET | Database statistics and debug info |

## 🤖 Automated Updates (Cron Job)

### Using Built-in Scheduler (Recommended)
The app uses APScheduler which runs automatically when the Flask app is running.

### Using System Cron (Linux/Mac)
```bash
chmod +x cron_job.sh
crontab -e
```
Add this line:
```
*/5 * * * * /path/to/flask_web_scraper/cron_job.sh
```

### Using Task Scheduler (Windows)
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Every 5 minutes
4. Action: Start Program
5. Program: `python`
6. Arguments: `c:\path\to\flask_web_scraper\app.py`

## 🚀 Deployment

### Deploy to Heroku
```bash
# Install Heroku CLI
heroku login
heroku create your-app-name
git push heroku main
heroku open
```

### Deploy to Railway
1. Connect GitHub repository
2. Auto-deploy on push
3. Add environment variables if needed

### Deploy to PythonAnywhere
1. Upload files via dashboard
2. Create web app with Flask
3. Configure WSGI file
4. Set working directory

### Deploy with Docker
```bash
# Build image
docker build -t crypto-tracker .

# Run container
docker run -p 5000:5000 crypto-tracker
```

## 📁 Project Structure

```
flask_web_scraper/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── cron_job.sh            # Cron job script
├── README.md              # Documentation
├── instance/              # SQLite database (auto-created)
│   └── crypto_data.db
├── static/
│   └── style.css          # CSS styling
└── templates/
    └── index.html         # Main template
```

## 🎨 Screenshots

### Main Dashboard
![Dashboard](screenshots/dashboard.png)

### Crypto Prices
![Prices](screenshots/prices.png)

### News Section
![News](screenshots/news.png)

## 📊 Database Schema

### CryptoPrice Table
- `id`: Primary key
- `name`: Cryptocurrency name
- `symbol`: Ticker symbol (BTC, ETH, etc.)
- `price`: Current USD price
- `change_24h`: 24-hour price change percentage
- `market_cap`: Total market capitalization
- `volume_24h`: 24-hour trading volume
- `last_updated`: Timestamp of last update

### News Table
- `id`: Primary key
- `title`: News article title
- `link`: URL to full article
- `source`: News source (e.g., CoinDesk)
- `published`: Timestamp

## 🔍 Troubleshooting

### No Data Showing
1. Check terminal for error messages
2. Visit `/debug` to see database contents
3. Click "Refresh Now" to manually fetch data
4. Ensure internet connection is active

### Scraper Not Working
- Update BeautifulSoup selectors if website structure changes
- Check if source website is accessible
- Review rate limiting policies

### Database Errors
```bash
# Delete and recreate database
rm instance/crypto_data.db
python app.py
```

## 📝 Git Commit Best Practices

```bash
# Initial commit
git add .
git commit -m "Initial commit: Flask crypto scraper setup"

# Feature commits
git commit -m "feat: Add CoinGecko API integration"
git commit -m "feat: Implement news scraping from CoinDesk"
git commit -m "style: Update UI with modern design"
git commit -m "fix: Resolve database connection issues"
git commit -m "docs: Add comprehensive README"

# Push to GitHub
git push origin main
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- CoinGecko API for crypto price data
- CoinDesk for news content
- Flask community for excellent documentation
- Font Awesome for icons

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Email: your.email@example.com

---

⭐ **Star this repo if you find it helpful!** ⭐
