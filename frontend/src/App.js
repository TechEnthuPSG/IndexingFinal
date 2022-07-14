import Header from "./components/Header";
import Line from "./components/Line";
import Search from "./components/Search";
import "./index.css";
import "./main.css";

function App() {
  return (
    <div className="bg-[#1a202c] h-[100vh] overflow-y-auto overflow-x-hidden">
      <Line />
      <Header />
      <Search />
    </div>
  );
}

export default App;
