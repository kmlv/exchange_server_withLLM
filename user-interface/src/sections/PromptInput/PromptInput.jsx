import React, { useState } from "react";
import "./index.css";
import axios from "axios";

// Sets the client address to the API URL if it is defined, otherwise sets it to the local host 5001
// Will only be defined when ran through docker
var client_addr = import.meta.env.VITE_API_URL;
if (import.meta.env.VITE_API_URL === undefined) {
  client_addr = "http://127.0.0.1:5001";
}

/**
 * The PromptInput section allows the user to enter a prompt and then sends it to the server
 * to be translated into python code. Then in the message container, the user can confirm or reject a generated 
 * description of the code that was generated. 
 * 
 * @returns {JSX.Element} - The PromptInput section
 */
export default function PromptInput() {
  const [prompt, setPrompt] = useState("");
  const [confirmationMessage, setConfirmationMessage] = useState("");
  const [showConfirmation, setShowConfirmation] = useState(false);

  // Sends the prompt our model to be translated into code
  const sendRequest = async () => {
    console.log(prompt);
    try {
      const response = await axios.post(client_addr + "/prompt", {
        prompt: prompt,
      });
      const message = response.data.confirmation;
      setConfirmationMessage(message);
      setShowConfirmation(true);
    } catch (error) {
      console.error(error);
    }
    setPrompt("");
  };


  /**
   * Sends the confirmation to the server whether to execute or don't execute the code
   * 
   * @param {boolean} isConfirmed - A boolean value that determines if the user confirmed the generated code
   * @returns {Promise<void>} - A promise that resolves when the confirmation is sent
  */
  
  const sendConfirmation = async (isConfirmed) => {
    if (isConfirmed === false) {
      setConfirmationMessage("Cancelled Confirmation");
      setShowConfirmation(false);
      return;
    }
    try {
      const response = await axios.post(client_addr + "/execute");
      console.log(response.data.confirmation);
      setConfirmationMessage(response.data.confirmation);
    } catch (error) {
      console.error(error);
    }
    setShowConfirmation(false);
  };

  return (
    <>
      <div className="chat-container">
        {/* Input for the user to enter a prompt */}
        <div className="inputDiv">
          <input
            value={prompt}
            placeholder="Enter a Prompt"
            onChange={(e) => setPrompt(e.target.value)}
          />
          <button className="enter-button" onClick={sendRequest}>
            Enter
          </button>
        </div>

        {/* Message container to display the message that explains what the generated code does*/}
        <div className="message-container">
          <div>{confirmationMessage}</div>
          {/* Buttons to confirm or reject the generated code */}
          <div className = "button-container1">
            {showConfirmation && (
              <button onClick={() => sendConfirmation(true)}>Confirm</button>
            )}
            {showConfirmation && (
              <button onClick={() => sendConfirmation(false)}>Reject</button>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
