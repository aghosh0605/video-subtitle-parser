import "./App.css";
import { FileUpload } from "./components/form";
import ProgressBar from "./components/progressbar";
import { useState, useEffect } from "react";
import Search from "./components/searchbar";

const App = () => {
  const [completed, setCompleted] = useState(0);

  useEffect(() => {
    setInterval(() => setCompleted(Math.floor(Math.random() * 100) + 1), 2000);
  }, []);
  return (
    <div className="App">
      <FileUpload />

      <ProgressBar bgcolor={"#6a1b9a"} completed={completed} />

      <Search />
    </div>
  );
};

export default App;
