import os
import  datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    client = MongoClient(os.environ.get("MONGODB_URI"))
    app.db = client.microblog


    @app.route('/', methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            app.db.entries.insert({"content": entry_content, "date": formatted_date})
            
        entries_with_date = [
            (entry["content"],
            entry["date"],
            datetime.datetime.strptime(entry["date"], "%d-%m-%Y %H:%M:%S").strftime("%b %d %H:%M")
            )
            for entry in app.db.entries.find({}).sort("date", -1)
        ]        
            
        return render_template("home.html", entries=entries_with_date)
    return app