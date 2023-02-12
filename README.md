# RegionSell

<p>
  <a href="https://regionsell.azurewebsites.net/?item=something"><img src="https://betteruptime.com/status-badges/v1/monitor/a9kf.svg" alt="Uptime"></a>
  <a href="https://github.com/arnavgupta03/regionsell/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-purple" alt="License"></a>
</p>

With RegionSell, all sorts of businesses can begin to predict where and when sales of certain items might increase, all through an easy to use Chrome extension! This can help e-commerce developers move certain items to the top of recommendations on a storefront based on a user's location and can assist e-commerce brands as a whole to get a better idea of what sells better where. Further, couriers can keep commonly bought items on their route, allowing for even faster delivery for certain lucky customers.

## How to use it

The API is hosted [https://regionsell.azurewebsites.net/](here). These are the endpoints you can use with it:
| Endpoint | Description |
| -------- | ----------- |
| ```/?item={item}``` | Uses the custom Cohere classification model to classify the given item into different countries and returns the list. |
| ```/add_to_cart?item_name={item_name}&location={country}``` | Adds the new purchase data to the training set for the custom Cohere model. |


To run the Chrome extension, you will need:
- Yarn
- Node.js
- Google Chrome
The Chrome extension can be built with ```yarn run build``` when inside the frontend folder, which creates the build folder, and then choosing the 'Load Unpacked' option in Chrome extensions and choosing the build folder.

### Built with
- [https://reactjs.org/](React)
- [https://flask.palletsprojects.com/en/2.2.x/](Flask)
- [https://cohere.ai/](Cohere)
- [https://azure.microsoft.com/en-us/products/app-service/](Azure App Service)
- [https://getbootstrap.com/](Bootstrap 5)
