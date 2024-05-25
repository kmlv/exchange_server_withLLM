import React, {useState} from "react";
import "./index.css";

import axios from "axios";


export default function PromptInput() {
  const [prompt, setPrompt] = useState("");
  const [message, setMessage] = useState("");
  const [confirm, setConfirm] = useState(false);

  const sendRequest = async () => {
    console.log(prompt);
    try {
      const response = await axios.post(import.meta.env.VITE_API_URL +"/prompt", {
        prompt: prompt,
      });
      console.log(response.data.confirmation);
      const confirmation_message = response.data.confirmation;
      setMessage(confirmation_message);
      setConfirm(true);
      
    } catch (error) {
      console.error(error);
    }
    setPrompt("");
  };
  const sendConfirmation = async (confirmation) => {
    if (confirmation === false){
      setMessage("Cancelled Confirmation");
      return;
    }
    try{
      const response = await axios.post(import.meta.env.VITE_API_URL + "/execute");
      console.log(response.data.confirmation);
      setMessage(response.data.confirmation);
    }catch (error) {
      console.error(error);
    }
    setConfirm(false);
    

  }

  return (
    <>
      <div className="chat-container">
        <div className = "inputDiv">
          <input
            value={prompt}
            placeholder="Enter a Prompt"
            onChange={(e) => setPrompt(e.target.value)}
          />
          <button onClick={sendRequest}>Enter</button>
        </div>
        <div>
          <div className="message-container">
            {message}
            {confirm && <button onClick={() => sendConfirmation(true)}>Confirm</button>}
            {confirm && <button onClick={() => sendConfirmation(false)}>Reject</button>}
          </div>
        </div>
      </div>
    </>
  );
}
