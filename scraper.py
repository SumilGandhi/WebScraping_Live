import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coinmarketcap.db'
db = SQLAlchemy(app)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    detail = db.Column(db.String(1000))
    published = db.Column(db.DateTime, default=datetime.utcnow)

def fetch_latest_data():
    url = "https://coinmarketcap.com/currencies/ethereum/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Scrape price
    price_tag = soup.find('div', class_="priceValue")
    price = price_tag.text if price_tag else "N/A"

    # Scrape Market Cap
    mc_tag = soup.find('div', string="Market cap")
    mc_value = mc_tag.find_next('div').text if mc_tag else "N/A"

    # Scrape Volume and Supply
    volume_tag = soup.find('div', string="Volume (24h)")
    volume_value = volume_tag.find_next('div').text if volume_tag else "N/A"
    
    supply_tag = soup.find('div', string="Circulating supply")
    supply_value = supply_tag.find_next('div').text if supply_tag else "N/A"

    # Scrape About section summary
    about_tag = soup.find('div', class_="sc-16r8icm-0")
    about = about_tag.text.strip() if about_tag else "N/A"

    info_list = [
        f"Price: {price}",
        f"Market Cap: {mc_value}",
        f"Volume (24h): {volume_value}",
        f"Circulating Supply: {supply_value}",
        f"About: {about[:250]}...",  # First 250 chars for preview
    ]
    for entry_text in info_list:
        # Save individual data items as News entries
        entry = News(title="Ethereum Info", detail=entry_text)
        db.session.add(entry)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        fetch_latest_data()
