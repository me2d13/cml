import React from "react";
import "./App.css";
import Keypad from "./keypad/keypad";
import { PAGES } from './config';
import Setup from './setup/setup';


function App() {
  const [page, setPage] = React.useState(PAGES.keypad);
  return (
    <div className="App">
      { page === PAGES.keypad && <Keypad setPage={setPage} />}
      { page === PAGES.setup && <Setup setPage={setPage} />}
    </div>
  );
}

export default App;
