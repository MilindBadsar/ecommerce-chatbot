import React from "react";
import "../index.css";

const Message = ({ type, text }) => {
  const messageClass = type === "user" ? "user-message" : "bot-message";
  const sender = type === "user" ? "You" : "Bot";

  return (
    <div className={`message-container ${messageClass}`}>
      <div className="sender-label">{sender}:</div>
      <div className="message-bubble">
        <p>{text}</p>
      </div>
    </div>
  );
};

export default Message;
