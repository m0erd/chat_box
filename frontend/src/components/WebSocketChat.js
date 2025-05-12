import React, { useState, useEffect, useRef } from 'react';

const WebSocketChat = () => {
  const [message, setMessage] = useState('');
  const [chatLog, setChatLog] = useState('');
  const socketRef = useRef(null);
  const messageInputRef = useRef(null);

  useEffect(() => {
    // Initialize WebSocket connection
    const roomName = '1';
    const socket = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${roomName}/`);

    // Assign WebSocket reference
    socketRef.current = socket;

    socket.onopen = () => {
      console.log('WebSocket connection established.');
    };

    socket.onmessage = (e) => {
      const data = JSON.parse(e.data);
      console.log('Message received:', data.message); // Debugging log
      setChatLog((prevChatLog) => prevChatLog + data.message + '\n');
    };

    socket.onclose = () => {
      console.error('Chat socket closed unexpectedly');
    };

    socket.onerror = (e) => {
      console.error('WebSocket error:', e);
    };

    // Cleanup WebSocket connection on component unmount
    return () => {
      socket.close();
    };
  }, []);

  const handleMessageSubmit = () => {
    if (message.trim()) {
      console.log('Sending message:', message); // Debugging log
      socketRef.current.send(JSON.stringify({ message }));
      setMessage('');
    }
  };

  const handleInputChange = (e) => {
    setMessage(e.target.value);
  };

  const handleKeyUp = (e) => {
    if (e.keyCode === 13) {  // Enter key
      handleMessageSubmit();
    }
  };

  return (
    <div>
      <h1>WebSocket Chat Test</h1>
      <textarea
        id="chat-log"
        cols="100"
        rows="20"
        readOnly
        value={chatLog}
        style={{ width: '100%' }}
      ></textarea>
      <br />
      <input
        id="chat-message-input"
        type="text"
        size="100"
        value={message}
        onChange={handleInputChange}
        onKeyUp={handleKeyUp}
        ref={messageInputRef}
        style={{ width: '80%' }}
      />
      <input
        id="chat-message-submit"
        type="button"
        value="Send"
        onClick={handleMessageSubmit}
        style={{ width: '15%' }}
      />
    </div>
  );
};

export default WebSocketChat;
