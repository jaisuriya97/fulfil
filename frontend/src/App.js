import React from "react";
import FileUpload from "./components/FileUpload";
import ProductList from "./components/ProductList";
import WebhookManager from "./components/WebhookManager";
import "./App.css";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Acme Inc. Product Importer</h1>
      </header>
      <main>
        <FileUpload />
        <ProductList />
        <WebhookManager />
      </main>
    </div>
  );
}

export default App;
