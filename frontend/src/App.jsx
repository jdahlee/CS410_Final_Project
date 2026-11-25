import { useState } from "react";
import "./App.css";
import { health } from "./requests";

function App() {
  const [query, setQuery] = useState("");

  const borderStyles = "border-2 rounded border-slate-500";
  const buttonStyles =
    "px-6 py-3 justify-self-center text-black bg-sky-100 hover:bg-sky-200 hover:cursor-pointer " +
    borderStyles;

  return (
    <>
      <div className="w-full h-full p-5">
        <div className="w-full my-10">
          <h1>CS 410 Song Title Finder</h1>
        </div>
        <div className="w-full my-10 grid justify-center space-y-4">
          <textarea
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter your song query here"
            className={`w-lg h-20 p-4 text-center text-black ${borderStyles}`}
          ></textarea>
          <button className={buttonStyles}>Search</button>
        </div>
        <button
          onClick={health}
          className="w-20 h-20 bg-white hover:bg-blue-100 hover:cursor-pointer"
        >
          Health check
        </button>
      </div>
    </>
  );
}

export default App;
