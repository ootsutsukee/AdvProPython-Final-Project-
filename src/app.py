import os
import dotenv

from flask import Flask, request, render_template

from utils.scraper import CryptoScraper
from utils.database import db
from utils.summarizer import Summarizer

from models.news import News

dotenv.load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisismyflasksecretkey'
#app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Akbota@127.0.0.1:5432/pythonFinal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

async def scrap(query):
    scraper = CryptoScraper()
    results = await scraper.scrap(query)

    for result in results:
        news = News(
            url=result['url'],
            heading=result['heading'],
            paragraph=result['paragraph']
        )
        
        news.sync()
    
    return results

@app.route('/coin', methods=['GET'])
async def search():
    query = request.args.get('q')
    
    if not query:
        return render_template('search.html')
    
    return render_template('search.html', query=query, data=await scrap(query))

if __name__ == "__main__":
    app.run(debug=True)