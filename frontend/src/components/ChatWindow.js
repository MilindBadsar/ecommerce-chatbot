import React, { useState, useEffect, useRef } from "react";
import { v4 as uuidv4 } from "uuid"; // For generating unique session IDs
import Message from "./Message";
import ChatInput from "./ChatInput";
import { sendMessageToChatbot } from "../services/api";
import "../index.css";

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null); // For auto-scrolling

  // a new session ID when the component mounts or resets
  useEffect(() => {
    const currentSessionId = localStorage.getItem("chatbotSessionId");
    if (currentSessionId) {
      setSessionId(currentSessionId);
    } else {
      const newId = uuidv4();
      setSessionId(newId);
      localStorage.setItem("chatbotSessionId", newId);
    }
    // initial welcome message from bot
    setMessages([
      {
        type: "bot",
        text: "Hello! I am your AI sales assistant. How can I help you today?",
      },
    ]);
  }, []);

  // Scroll to the bottom of the chat window on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = async (userMessage) => {
    const newUserMessage = { type: "user", text: userMessage };
    setMessages((prevMessages) => [...prevMessages, newUserMessage]);
    setIsLoading(true);

    try {
      const botResponse = await sendMessageToChatbot(userMessage, sessionId);
      const newBotMessage = { type: "bot", text: botResponse };
      setMessages((prevMessages) => [...prevMessages, newBotMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { type: "bot", text: "Oops! Something went wrong. Please try again." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleResetChat = () => {
    const newId = uuidv4();
    setSessionId(newId);
    localStorage.setItem("chatbotSessionId", newId);
    setMessages([
      {
        type: "bot",
        text: "Hello! I am your AI sales assistant. How can I help you today?",
      },
    ]);
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>AI Sales Chatbot</h2>
        <button onClick={handleResetChat} className="reset-button">
          Reset Chat
        </button>
      </div>
      <div className="messages-display">
        {messages.map((msg, index) => (
          <Message key={index} type={msg.type} text={msg.text} />
        ))}
        <div ref={messagesEndRef} /> {/* Scroll target */}
      </div>
      <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  );
};

export default ChatWindow;
