import React from 'react';

function App() {
  let [productName, setProductName] = React.useState<string>('');

  chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
      let url = tabs[0].url;
      console.log(url);
      // use `url` here inside the callback because it's asynchronous!
      setProductName((url?.split('?')[1].split('&')[0].split('=')[1].split('+'))?.join(' ') ?? 'No product name found')
  });
  return (
    <div className="App">
      <h1 className="display-1 text-center">RegionSell</h1>
      <h2 className="display-4 text-center">Product: {productName}</h2>
    </div>
  );
}

export default App;
