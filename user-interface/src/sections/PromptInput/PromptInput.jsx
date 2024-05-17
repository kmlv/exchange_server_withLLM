import React, {useState} from "react";
import "./index.css";

import axios from "axios";


export default function PromptInput() {
  const [prompt, setPrompt] = useState("");

  const sendRequest = async () => {
    console.log(prompt);
    try {
      const response = await axios.post("http://localhost:8083/prompt", {
        prompt: prompt,
      });
      console.log(response);
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
    setPrompt("");
  };

  return (
    <div className = "inputDiv">
      <input
        value={prompt}
        placeholder="Enter a Prompt"
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button onClick={sendRequest}>Enter</button>
    </div>
  );
}
