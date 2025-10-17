from flask import Flask, render_template, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import atexit
import json
import pytz
import os

app = Flask(__name__)

# Use environment variables for production, fallback to defaults for local dev
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///crypto_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'crypto-scraper-2025-secret-key')

# Fix Postgres URL for SQLAlchemy (Render uses 'postgres://' but SQLAlchemy needs 'postgresql://')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)

db = SQLAlchemy(app)

class CryptoPrice(db.Model):
    """Model to store cryptocurrency prices"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    change_24h = db.Column(db.String(20))
    market_cap = db.Column(db.String(50))
    volume_24h = db.Column(db.String(50))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'symbol': self.symbol,
            'price': self.price,
            'change_24h': self.change_24h,
            'market_cap': self.market_cap,
            'volume_24h': self.volume_24h,
            'last_updated': self.last_updated.strftime('%Y-%m-%d %H:%M:%S')
        }

class News(db.Model):
    """Model to store crypto news"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    link = db.Column(db.String(500), nullable=False, unique=True)
    source = db.Column(db.String(100))
    published = db.Column(db.DateTime, default=datetime.utcnow)

class Weather(db.Model):
    """Model to store weather data"""
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.String(20))
    description = db.Column(db.String(100))
    humidity = db.Column(db.String(20))
    wind_speed = db.Column(db.String(20))
    icon = db.Column(db.String(10))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

def fetch_crypto_prices():
    """Scrape cryptocurrency prices from CoinGecko API"""
    with app.app_context():
        try:
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 20,
                'page': 1,
                'sparkline': False
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            count = 0
            for coin in data:
                try:
                    name = coin.get('name', 'N/A')
                    symbol = coin.get('symbol', 'N/A').upper()
                    price = f"${coin.get('current_price', 0):,.2f}"
                    change_24h = f"{coin.get('price_change_percentage_24h', 0):.2f}%"
                    market_cap = f"${coin.get('market_cap', 0):,.0f}"
                    volume_24h = f"${coin.get('total_volume', 0):,.0f}"
                    
                    existing = CryptoPrice.query.filter_by(symbol=symbol).first()
                    if existing:
                        existing.price = price
                        existing.change_24h = change_24h
                        existing.market_cap = market_cap
                        existing.volume_24h = volume_24h
                        existing.last_updated = datetime.utcnow()
                    else:
                        new_crypto = CryptoPrice(
                            name=name,
                            symbol=symbol,
                            price=price,
                            change_24h=change_24h,
                            market_cap=market_cap,
                            volume_24h=volume_24h
                        )
                        db.session.add(new_crypto)
                    count += 1
                    
                except Exception as e:
                    print(f"Error processing {coin.get('name', 'unknown')}: {e}")
                    continue
            
            db.session.commit()
            print(f"✅ Successfully updated {count} cryptocurrencies")
            
        except Exception as e:
            print(f"❌ Error fetching crypto prices: {e}")

def fetch_crypto_news():
    """Scrape crypto news from CoinDesk"""
    with app.app_context():
        try:
            url = "https://www.coindesk.com/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            count = 0
            articles = soup.find_all('a', class_='card-title')
            
            if not articles:
                articles = soup.find_all('h4', class_='heading')
            
            for article in articles[:15]:
                try:
                    if article.name == 'a':
                        title = article.get_text(strip=True)
                        link = article.get('href')
                    else:
                        link_tag = article.find('a')
                        if link_tag:
                            title = article.get_text(strip=True)
                            link = link_tag.get('href')
                        else:
                            continue
                    
                    if not title or not link or len(title) < 10:
                        continue
                    
                    if not link.startswith('http'):
                        link = f"https://www.coindesk.com{link}"
                    
                    if not News.query.filter_by(link=link).first():
                        news_entry = News(
                            title=title[:500],
                            link=link,
                            source='CoinDesk'
                        )
                        db.session.add(news_entry)
                        count += 1
                        
                except Exception as e:
                    print(f"Error processing news: {e}")
                    continue
            
            db.session.commit()
            print(f"✅ Successfully added {count} news articles")
            
        except Exception as e:
            print(f"❌ Error fetching crypto news: {e}")

def fetch_weather(city="London"):
    """Fetch weather data from OpenWeatherMap API"""
    with app.app_context():
        try:
            # Using OpenWeatherMap API (free tier - get API key from openweathermap.org)
            # For demo, using wttr.in which doesn't require API key
            url = f"https://wttr.in/{city}?format=j1"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            current = data['current_condition'][0]
            
            # Delete old weather data
            Weather.query.delete()
            
            # Add new weather data
            weather = Weather(
                city=city,
                temperature=f"{current['temp_C']}°C",
                description=current['weatherDesc'][0]['value'],
                humidity=f"{current['humidity']}%",
                wind_speed=f"{current['windspeedKmph']} km/h",
                icon=current['weatherCode'],
                last_updated=datetime.utcnow()
            )
            db.session.add(weather)
            db.session.commit()
            print(f"✅ Successfully updated weather for {city}")
            
        except Exception as e:
            print(f"❌ Error fetching weather: {e}")

def fetch_all_data():
    """Fetch crypto prices, news, and weather"""
    print(f"\n🔄 Starting data fetch at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    fetch_crypto_prices()
    fetch_crypto_news()
    fetch_weather("London")  # Change to your city
    print(f"✅ Data fetch complete\n")

# Setup scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=fetch_all_data, trigger="interval", minutes=5)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

@app.route('/')
def index():
    """Main page showing crypto prices, news, weather and time"""
    crypto_data = CryptoPrice.query.order_by(CryptoPrice.id).limit(20).all()
    news_data = News.query.order_by(News.published.desc()).limit(10).all()
    weather_data = Weather.query.first()
    
    last_update = CryptoPrice.query.first()
    last_update_time = last_update.last_updated.strftime('%Y-%m-%d %H:%M:%S') if last_update else 'Never'
    
    # Get current time in different timezones
    utc_time = datetime.now(pytz.utc)
    ist_time = utc_time.astimezone(pytz.timezone('Asia/Kolkata'))
    
    return render_template("index.html", 
                         crypto_list=crypto_data, 
                         news_list=news_data,
                         weather=weather_data,
                         last_update=last_update_time,
                         current_time=ist_time.strftime('%I:%M:%S %p'),
                         current_date=ist_time.strftime('%A, %B %d, %Y'))

@app.route('/refresh')
def refresh():
    """Manual refresh endpoint"""
    fetch_all_data()
    flash('Data refreshed successfully!')
    return redirect(url_for('index'))

@app.route('/api/crypto')
def api_crypto():
    """API endpoint to get crypto data as JSON"""
    crypto_data = CryptoPrice.query.order_by(CryptoPrice.id).limit(20).all()
    return jsonify([crypto.to_dict() for crypto in crypto_data])

@app.route('/api/weather')
def api_weather():
    """API endpoint to get weather data as JSON"""
    weather = Weather.query.first()
    if weather:
        return jsonify({
            'city': weather.city,
            'temperature': weather.temperature,
            'description': weather.description,
            'humidity': weather.humidity,
            'wind_speed': weather.wind_speed,
            'last_updated': weather.last_updated.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify({'error': 'No weather data available'}), 404

@app.route('/debug')
def debug():
    """Debug route to check database contents"""
    crypto_count = CryptoPrice.query.count()
    news_count = News.query.count()
    weather = Weather.query.first()
    
    debug_info = f"<h2>Database Status</h2>"
    debug_info += f"<p>Total Cryptocurrencies: {crypto_count}</p>"
    debug_info += f"<p>Total News Articles: {news_count}</p>"
    if weather:
        debug_info += f"<p>Weather: {weather.city} - {weather.temperature} - {weather.description}</p>"
    debug_info += "<hr>"
    
    debug_info += "<h3>Latest Crypto Prices:</h3>"
    cryptos = CryptoPrice.query.limit(10).all()
    for crypto in cryptos:
        debug_info += f"<b>{crypto.name} ({crypto.symbol})</b>: {crypto.price} | Change: {crypto.change_24h}<br>"
    
    debug_info += "<hr><h3>Latest News:</h3>"
    news = News.query.order_by(News.published.desc()).limit(10).all()
    for item in news:
        debug_info += f"<a href='{item.link}' target='_blank'>{item.title}</a><br><br>"
    
    return debug_info

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("🚀 Starting Crypto Price Tracker...")
        print("📊 Fetching initial data...")
        fetch_all_data()
        print("✅ App ready!")
        print("🌐 Visit: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)