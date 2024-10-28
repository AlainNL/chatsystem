import React, { useState } from 'react';
import './Chat.css';

const API_URL = 'http://127.0.0.1:5000/chat'

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

 //Function for send a message
  const sendMessage = async () => {
    if (!input.trim()) return;

    //Create a user message
    const userMessage = { sender: 'user', message: input };
    setMessages([...messages, userMessage]);

    //Create a history
    const history = [...messages, userMessage];

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json'},
      body: JSON.stringify({history}) //send complete history
    });

    if(!response) {
      throw new Error('An error occured');
    }

    //Collect server response
    const data = await response.json();
    const agentMessage = { sender: 'agent', message: data.agent_reply};

    setMessages(prev => [...prev, agentMessage]);
  } catch (error) {
    console.error('Error, error');
    setMessages(prev => [...prev, { sender: 'agent', message: 'An error occurend.'}])
  }

  setInput('');
}

  return (
    <div className="chat-container">
      <div className="chat-box">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`}>
                {msg.message}
            </div>
          ))}
      </div>
      <div className="input-container">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter your message here"
          />
          <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  )
};

export default Chat
