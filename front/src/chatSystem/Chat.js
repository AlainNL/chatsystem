import React, { useState } from 'react';
import './Chat.css';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: 'user', message: input };
    setMessages([...messages, userMessage]);

    const history = [...messages, userMessage];

  try {
    const response = await fetch('http://127.0.0.1:5000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json'},
      body: JSON.stringify({history}) //send complete history
    });

    if(!response) {
      throw new Error('An error occured');
    }

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
