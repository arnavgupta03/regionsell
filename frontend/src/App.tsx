import React, { useEffect } from 'react';

function App() {
  let [productName, setProductName] = React.useState<string>('');
  let [suggestedList, setSuggestedList] = React.useState<{"label": string, "value": number}[]>([]);

  useEffect(() => {
    // get current tab url
    chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
        let url = tabs[0].url;
        console.log(url);
        if (url != null) {
          // use `url` here inside the callback because it's asynchronous!
          setProductName((url?.split('?')[1].split('&')[0].split('=')[1].split('+'))?.join(' ') ?? 'No product name found')
          // call home endpoint of flask api passing product name as query param
          let query_url = `https://regionsell.azurewebsites.net/?item=${productName}`;
          console.log(query_url);
          fetch(query_url).then((response) => {
            return response.json();
          }).then((data) => {
            console.log(data.slice(0, 5));
            setSuggestedList(data.slice(0, 5));
          });
        }
    });
  }, [productName]);
  return (
    <div className="App p-3">
      <h1 className="shadow p-3 mb-5 bg-body rounded text-center">RegionSell</h1>
      <h3 className="text-center">Product: {
      productName.toLowerCase()
        .split(' ')
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
      }</h3>
      <h3 className="lead">Here's some suggested Places to Sell this Product</h3>
      <ul className="list-group">
        {suggestedList.map((suggestion, index) => {
          return <li key={index} className="list-group-item">{suggestion.label}</li>;
        })}
      </ul>
      <button className="btn btn-primary mt-3" onClick={() => {
        setSuggestedList([...suggestedList.slice(0, 3), {label: "Canada", value: 0}, suggestedList[3]]);
      }}>Check for New Updates</button>
    </div>
  );
}

export default App;
