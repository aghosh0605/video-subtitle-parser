import "./App.css";
import { FileUpload } from "./components/form";
import ProgressBar from "./components/progressbar";
import { useState, useEffect } from "react";
import Search from "./components/searchbar";

const App = () => {
  const [completed, setCompleted] = useState(0);
  const [fileName, setFileName] = useState();

  useEffect(() => {
    setInterval(() => setCompleted(Math.floor(Math.random() * 100) + 1), 2000);
  }, []);
  return (
    <div className="App">
      <FileUpload setFileName={setFileName} />

      <ProgressBar
        bgcolor={"#6a1b9a"}
        completed={completed}
        fileName={fileName}
      />

      <Search />
    </div>
  );
};

export default App;
