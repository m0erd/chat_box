import React, { useEffect, useState, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";

const backendUrl = process.env.REACT_APP_BACKEND_URL;

const apiLogin = async (username, password) => {
  return {
    data: { token: "access_token" },
  };
};

const isTokenExpired = (token) => {
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.exp < Date.now() / 1000;
  } catch (err) {
    console.error("Invalid token format:", err);
    return true;
  }
};

function ChatApp() {
  const { channelId } = useParams();
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [channelName, setChannelName] = useState("");
  const websocketRef = useRef(null);
  const navigate = useNavigate();
  const messagesEndRef = useRef(null);

  const hasConnectedRef = useRef(false);

  const refreshAccessToken = async () => {
    const refresh = localStorage.getItem("refresh_token");
    if (!refresh) return null;

    try {
      const response = await fetch(`${backendUrl}/api/token/refresh/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh }),
      });

      if (!response.ok) throw new Error("Token refresh failed");

      const data = await response.json();
      localStorage.setItem("access_token", data.access);
      return data.access;
    } catch (err) {
      console.error("Token refresh error:", err);
      return null;
    }
  };

  useEffect(() => {
    const fetchChannelName = async () => {
      try {
        const response = await fetch(`${backendUrl}/api/channels/${channelId}/`, {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("access_token")}`
          }
        });

        if (response.ok) {
          const data = await response.json();
          setChannelName(data.channel_name);
        } else {
          console.error("Failed to fetch channel name");
        }
      } catch (err) {
        console.error("Error fetching channel name:", err);
      }
    };

    fetchChannelName();

    const buildWebSocketURL = (httpUrl, path) => {
      const wsScheme = httpUrl.startsWith("https") ? "wss" : "ws";
      const cleanBackendUrl = httpUrl.replace(/^https?:\/\//, "");
      return `${wsScheme}://${cleanBackendUrl}${path}`;
    };

    const setupWebSocket = async () => {
      const isPublic = ["general", "tech-talk", "random"].includes(channelId);
      let token = localStorage.getItem("access_token");

      if (!isPublic) {
        if (!token || isTokenExpired(token)) {
          token = await refreshAccessToken();
          if (!token) {
            navigate("/login");
            return;
          }
        }
      }

      const wsPath = isPublic
        ? `/ws/chat/${channelId}/`
        : `/ws/chat/${channelId}/?token=${token}`;

      const url = buildWebSocketURL(backendUrl, wsPath);

      console.log("Connecting to WebSocket at:", url);
      const wss = new WebSocket(url);
      websocketRef.current = wss;

      wss.onopen = () => console.log("✅ WebSocket connected");
      wss.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          const { message, username } = data;
          setMessages((prev) => [...prev, { username, message }]);
        } catch (err) {
          console.error("Parse error:", err);
        }
      };
      
      wss.onerror = (err) => console.error("❌ WebSocket error:", err);
      wss.onclose = () => console.log("🔌 WebSocket closed");
    };

    setupWebSocket();

    return () => {
      if (websocketRef.current) {
        websocketRef.current.close();
        websocketRef.current = null;
        console.log("🔁 Cleaned up previous WebSocket");
      }
    };
  }, [channelId, navigate]);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const sendMessage = () => {
    if (!message.trim()) return;

    if (websocketRef.current && websocketRef.current.readyState === WebSocket.OPEN) {
      websocketRef.current.send(JSON.stringify({ message }));
      setMessage("");
    } else {
      console.error("WebSocket is not open.");
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  return (
    <div className="chat-panel p-3">
      <h3 className="channel-name">{channelName || channelId}</h3>

      <div className="chat-messages border p-2 mb-3" style={{ height: "400px", overflowY: "scroll" }}>
        {messages.map((msg, index) => (
          <div key={index} className="message">
            <strong>{msg.username || "Anonymous"}:</strong> {msg.message}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-group">
        <input
          type="text"
          className="form-control"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message..."
        />
        <button className="btn btn-primary" onClick={sendMessage}>
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatApp;
