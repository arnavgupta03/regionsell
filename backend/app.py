"""Server for application to classify text and clean data."""
import csv
import cohere
import os
from dotenv import load_dotenv
from flask import Flask

app = Flask(__name__)

load_dotenv()

co = cohere.Client(os.environ.get("COHERE_API_KEY"))

app.config['SECRET_KEY'] = 'P+A4EHVAH'

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
    examples = read_data_file()
    response = co.classify(
        inputs=["DOORMAT FANCY FONT HOME SWEET HOME 2/11/2023 2:55"],
        examples=examples,
        model="large",
        truncate="END"
    )
    return {"response": response}

if __name__ == '__main__':
    app.run(debug = True)
