"""Server for application to classify text and clean data."""
import os
import csv
from datetime import datetime
import cohere
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from cohere.classify import Example

app = Flask(__name__)
CORS(app, resources={
        r"/?*": {"origins": "*"},
        r"/add_to_cart?*": {"origins": "*"}
    })

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
    new_examples = []
    # read lines from new_examples.csv
    with open("new_examples.csv", newline='', encoding="utf-8") as csvfile:
        fieldnames = ["Name", "Country"]
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for row in reader:
            new_examples.append(Example(row["Name"] + " " + current_date, row["Country"]))

    just_labels = [x.label for x in new_examples]
    if all(just_labels.count(x) > 2 for x in just_labels):
        response = co.classify(
            inputs=[item + " " + current_date],
            model="a6da86a1-2683-4abe-8c2c-454b0aa4385d-ft",
            examples=new_examples,
            truncate="END"
        )
    else:
        response = co.classify(
            inputs=[item + " " + current_date],
            model="a6da86a1-2683-4abe-8c2c-454b0aa4385d-ft",
            truncate="END"
        )
    response = jsonify([
        {
            "label": item[0],
            "value": item[1][0]
        }
        for item in sorted(
            response.classifications[0].labels.items(),
            key=lambda x: x[1],
            reverse=True)
        ])
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/add_to_cart')
def add_to_cart():
    """Add item to new examples to train on."""
    # append item name and country to csv file
    item = request.args.get('item_name')
    country = request.args.get('location')
    with open("new_examples.csv", 'a', newline='', encoding="utf-8") as csvfile:
        fieldnames = ["Name", "Country"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({
            "Name": item,
            "Country": country
        })
    return {"Success": True}

if __name__ == '__main__':
    app.run()
