"""Server for application to classify text and clean data."""
import os
import csv
from datetime import datetime
import cohere
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

load_dotenv()

co = cohere.Client(os.environ.get("COHERE_API_KEY"))

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

def read_data_file():
    """Reads data from csv file and returns a list of dictionaries after writing to csv file."""
    rows = []
    with open("data.csv", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append({
                "example": row["Description"] + " " + row["InvoiceDate"],
                "label": row["Country"]
            })

    ukrows = list(filter(lambda x: (x["label"] == 'United Kingdom'), rows))
    rows = list(filter(lambda x: (x["label"] != 'United Kingdom'), rows))
    rows.extend(ukrows[:9500])

    with open("examples.csv", 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = ["example", "label"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writerows(rows)
    return rows

@app.route('/')
def home():
    """Classifies text and returns a response."""
    # get the item query parameter from the url
    item = request.args.get('item')
    # get the current date and time
    current_date = datetime.now().strftime("%m/%d/%Y %H:%M")
    response = co.classify(
        inputs=[item + " " + current_date],
        model="a6da86a1-2683-4abe-8c2c-454b0aa4385d-ft",
        truncate="END"
    )
    return [
        {
            "label": item[0],
            "value": item[1][0]
        }
        for item in sorted(
            response.classifications[0].labels.items(),
            key=lambda x: x[1],
            reverse=True)
        ]

if __name__ == '__main__':
    app.run(debug = True)
