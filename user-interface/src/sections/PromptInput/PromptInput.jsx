import React, { useState } from "react";
import "./index.css";

import axios from "axios";

var client_addr = import.meta.env.VITE_API_URL;
if (import.meta.env.VITE_API_URL === undefined) {
  client_addr = "http://127.0.0.1:5001";
}

export default function PromptInput() {
  const [prompt, setPrompt] = useState("");
  const [message, setMessage] = useState("");
  const [confirm, setConfirm] = useState(false);

  const sendRequest = async () => {
    console.log(prompt);
    try {
      const response = await axios.post(client_addr + "/prompt", {
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
    if (confirmation === false) {
      setMessage("Cancelled Confirmation");
      setConfirm(false);
      return;
    }
    try {
      const response = await axios.post(client_addr + "/execute");
      console.log(response.data.confirmation);
      setMessage(response.data.confirmation);
    } catch (error) {
      console.error(error);
    }
    setConfirm(false);
  };

  return (
    <>
      <div className="chat-container">
        <div className="inputDiv">
          <input
            value={prompt}
            placeholder="Enter a Prompt"
            onChange={(e) => setPrompt(e.target.value)}
          />
          <button class="enter-button" onClick={sendRequest}>
            Enter
          </button>
        </div>

        <div className="message-container">
          <div>{message}</div>
          <div className = "button-container1">
            {confirm && (
              <button onClick={() => sendConfirmation(true)}>Confirm</button>
            )}
            {confirm && (
              <button onClick={() => sendConfirmation(false)}>Reject</button>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
