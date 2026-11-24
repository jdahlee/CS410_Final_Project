import { useState } from "react";
import "./App.css";
import { health } from "./requests";

function App() {
  return (
    <>
      <div className="w-full p-10 bg-blue-200">
        <button onClick={health} className="w-20 h-20 bg-white">
          Health check
        </button>
      </div>
    </>
  );
}

export default App;
