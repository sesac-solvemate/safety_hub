import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import MainPage from "./components/pages/MainPage";
import FirstPage from "./components/pages/FirstPage";
import SecondPage from "./components/pages/SecondPage";
import ThirdPage from "./components/pages/ThirdPage";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<MainPage />} />
          <Route path="/tenMin" element={<FirstPage />} />
          <Route path="/firstForm" element={<SecondPage />} />
          <Route path="/secondForm" element={<ThirdPage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
