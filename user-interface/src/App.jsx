import "./App.css";
import Header from "./sections/header/Header";
import PromptInput from "./sections/PromptInput/PromptInput";
import Client_orders from "./sections/client_orders/Client_orders";

function App() {
  console.log(process.env.REACT_APP_API_URL);
  //Fetch clients from client_0 at 10.10.0.1:8083
  //endpoint: /get_clients
  //receive something like clients = [ 10.10.0.1:8083,  10.10.0.2:8084,  10.10.0.3:8085..]

  //Build pool/list/array of client receive from fetch

  //client that exists per user session
  // var client = client.pop()
  //client 10.10.0.2:8084


  //When sending API calls to allocated client
  //fetch client.addr
  //fetch to client_2 10.10.0.3:8085
  // if fetched_client_id == my_client_id:
    //update page
  

  return (
    <>
      <Header/>
      <PromptInput/>
      <Client_orders/>
    </>
  );
}

export default App;
