"""This is the basic test application to test the Chrome extension."""
# Path: testapp\app.py
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    """Returns the index.html file with all shopping data."""
    items = [
        {
            "itemname": "WHITE HANGING HEART T-LIGHT HOLDER",
            "quantity": 6,
            "price": 2.55,
            "date": "2010-12-01 08:26:00"
        },
        {
            "itemname": "WHITE METAL LANTERN",
            "quantity": 6,
            "price": 3.39,
            "date": "2010-12-01 08:26:00"
        },
        {
            "itemname": "CREAM CUPID HEARTS COAT HANGER",
            "quantity": 8,
            "price": 2.75,
            "date": "2010-12-01 08:26:00"
        },
        {
            "itemname": "ALARM CLOCK BAKELIKE PINK",
            "quantity": 24,
            "price": 3.75,
            "date": "2010-12-01 08:45:00"
        },
        {
            "itemname": "ALARM CLOCK BAKELIKE RED",
            "quantity": 24,
            "price": 3.75,
            "date": "2010-12-01 08:45:00"
        },
        {
            "itemname": "ALARM CLOCK BAKELIKE GREEN",
            "quantity": 12,
            "price": 3.75,
            "date": "2010-12-01 08:45:00"
        },
        {
            "itemname": "CHRISTMAS LIGHTS 10 REINDEER",
            "quantity": 6,
            "price": 8.50,
            "date": "2010-12-01 10:03:00"
        },
        {
            "itemname": "VINTAGE UNION JACK CUSHION COVER",
            "quantity": 8,
            "price": 4.95,
            "date": "2010-12-01 10:03:00"
        },
        {
            "itemname": "VINTAGE HEADS AND TAILS CARD GAME",
            "quantity": 12,
            "price": 1.25,
            "date": "2010-12-01 10:03:00"
        },
        {
            "itemname": "SET OF 6 T-LIGHTS SANTA",
            "quantity": 6,
            "price": 2.95,
            "date": "2010-12-01 13:04:00"
        },
        {
            "itemname": "ROTATING SILVER ANGELS T-LIGHT HLDR",
            "quantity": 6,
            "price": 2.55,
            "date": "2010-12-01 13:04:00"
        },
        {
            "itemname": "MULTI COLOUR SILVER T-LIGHT HOLDER",
            "quantity": 12,
            "price": 0.85,
            "date": "2010-12-01 13:04:00"
        },
    ]
    return render_template('index.html', items=items)

@app.route('/item')
def item():
    """Returns the item.html file with all shopping data for that item."""
    # get item name from url query params
    item_id = request.args.get('item_id')
    item_price = request.args.get('item_price')
    return render_template('item.html', item_name=item_id, item_price=item_price)

if __name__ == '__main__':
    app.run(debug = True, port=5001)