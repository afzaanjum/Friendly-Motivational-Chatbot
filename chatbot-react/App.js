import React, { useState } from "react";
import "./App.css";
import background from "./background.jpg";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  // Format current date
  const todayDate = new Date().toLocaleDateString(undefined, {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  const getTime = () =>
  new Date().toLocaleTimeString([], {
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  });

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = {
      sender: "user",
      text: input,
      time: getTime(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsTyping(true);

    try {
      const response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();

      const botMessage = {
        sender: "bot",
        text: data.reply,
        time: getTime(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const botMessage = {
        sender: "bot",
        text: "Oops! Something went wrong.",
        time: getTime(),
      };
      setMessages((prev) => [...prev, botMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <div
      className="app"
      style={{
        backgroundImage: `url(${background})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
      }}
    >
      <div className="chat-container">
        <h2 className="chat-header">Friendly ChatBot 🤖</h2>

        {/* Date */}
        <div className="chat-date">{todayDate}</div>

        <div className="chat-box">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`chat-message ${
                msg.sender === "user" ? "user" : "bot"
              }`}
            >
              <div className="message-text">{msg.text}</div>
              <div className="message-time">{msg.time}</div>
            </div>
          ))}

          {/* Typing Indicator */}
          {isTyping && (
            <div className="chat-message bot typing">
              <span></span>
              <span></span>
              <span></span>
            </div>
          )}
        </div>

        <div className="input-container">
          <input
            type="text"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>

      {/* Footer */}
      <div className="footer-credit">Made with ❤️ by Afza</div>
    </div>
  );
}

export default App;
