import "./App.css";
import Header from "./Sections/Header/Header";
import PromptInput from "./Sections/PromptInput/PromptInput";
import ClientOrders from "./Sections/ClientOrders/ClientOrders";

// The App component is the root component of the application
function App() {
  console.log(import.meta.env.VITE_API_URL);
 
  // All the sections of the application are rendered here
  return (
    <>
      <Header/>
      <PromptInput/>
      <ClientOrders/>
    </>
  );
}

export default App;
