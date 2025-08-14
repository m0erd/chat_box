import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  useNavigate,
} from "react-router-dom";
import { useEffect, useState } from "react";
import Layout from "./components/layouts/BaseLayout";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Chat from "./pages/ChatApp";
import Logout from "./pages/Logout";
import Profile from "./pages/Profile";
import MyChannels from "./pages/MyChannels";
import CreateChannel from "./pages/CreateChannel";
import { useAuth } from "./context/AuthContext";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import "./styles/styles.css";

const backendUrl = process.env.REACT_APP_BACKEND_URL;


function AppHeader() {
  const { user, setUser, logoutUser } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    const refreshToken = localStorage.getItem("refresh_token");

    if (refreshToken) {
      await fetch(`${backendUrl}/api/logout/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });
    }

    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUser(null);
    navigate("/");
};

  return (
    <nav className="navbar navbar-expand-lg navbar-custom">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/">ChatApp</Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto">
            {user ? (
              <>
                <li className="nav-item">
                  <span className="nav-link">Hello, {user?.username || "Guest"}</span>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/my-channels">My Channels</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/create-channel">Create Channel</Link>
                </li>
                <li className="nav-item">
                  <button className="btn btn-outline-danger btn-sm" onClick={handleLogout}>Logout</button>
                </li>
              </>
            ) : (
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/login">Login</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/register">Register</Link>
                </li>
              </>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
}

function AppLayoutWrapper() {
  const { user } = useAuth();
  const [channels, setChannels] = useState([]);
  const [projectInfo, setProjectInfo] = useState("");
  const backendUrl = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    fetch(`${backendUrl}/api/channels/`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: token ? `Bearer ${token}` : "",
      },
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch channels");
        }
        return res.json();
      })
      .then((data) => {
        setChannels(data);
      })
      .catch((err) => {
        console.error("Channel fetch error:", err);
      });

    fetch("/project_description.txt")
      .then((res) => res.text())
      .then((text) => setProjectInfo(text))
      .catch((err) => console.error("Failed to load project description:", err));
  }, []);

  const navigate = useNavigate();

  const handleChannelClick = (channelId) => {
    if (!user) {
      localStorage.setItem("redirectChannel", channelId);
      navigate("/login");
    } else {
      navigate(`/chat/${channelId}`);
    }
  };

  return (
  <div className="chat-container row">
    <aside className="col-md-3 sidebar">
      <h4>Channels</h4>
      <ul className="list-group">
        {channels.map((channel) => (
          <li key={channel.id} className="list-group-item">
            <button
              className="btn btn-link p-0 text-start"
              onClick={() => handleChannelClick(channel.id)}
              aria-label={`Join ${channel.name} channel`}
            >
              {channel.name}
            </button>
          </li>
        ))}
      </ul>
    </aside>

    <main
      className="col-md-9 chat-panel"
      style={{
        padding: "2rem",
        backgroundColor: "#fff",
        fontFamily: "Arial, sans-serif",
        lineHeight: 1.6,
      }}
    >
      <h2 style={{ marginBottom: "1rem", color: "#2c3e50" }}>🛠 Explore the Project</h2>
      <p>
        Check out the real-time chat functionality by logging in with these demo accounts (or you can crate):
        <br />
        <strong>username:</strong> user, <strong>password:</strong> pass
        <br />
        <strong>username:</strong> user2, <strong>password:</strong> pass
      </p>
      <p>
        Use separate browsers (e.g., Chrome and Opera) to log in with different accounts and see messages update live in the same channel.
      </p>
      <p>
        Developers can explore the codebase and architecture here:{" "}
        <a href="https://github.com/m0erd/chat_box/" target="_blank" rel="noopener noreferrer">
          GitHub Repository
        </a>
      </p>

      <h1 style={{ fontSize: "2rem", marginBottom: "1rem" }}>
        🚀 Real-Time Chat Application with Django
      </h1>
      <p>
        This project showcases a highly engineered real-time chat system built using Django, Django Channels, and PostgreSQL,
        emphasizing modern backend architecture, asynchronous communication, and robust security practices.
      </p>

      <p>
        At its core, the application delivers a production-ready WebSocket infrastructure that allows users to create and join
        custom chat channels, exchange messages instantly, and securely authenticate via a JWT-based token system.
      </p>

      <h2 style={{ marginTop: "2rem", color: "#2c3e50" }}>🧠 Core Engineering Highlights</h2>
      <ul style={{ paddingLeft: "1.2rem" }}>
        <li><span style={{ fontSize: "1.2rem", marginRight: "0.4rem" }}>⚙️</span><strong>Scalable Architecture:</strong> Modular Django design, layered service structure, and reusable components ensure clean separation of concerns and future-proofing.</li>
        <li><span style={{ fontSize: "1.2rem", marginRight: "0.4rem" }}>🔄</span><strong>Asynchronous Real-Time Messaging:</strong> Django Channels enable full-duplex WebSocket communication for high-performance messaging.</li>
        <li><span style={{ fontSize: "1.2rem", marginRight: "0.4rem" }}>🔐</span><strong>JWT-Based Authentication:</strong> Secure token-based login with access and refresh tokens.</li>
        <li><span style={{ fontSize: "1.2rem", marginRight: "0.4rem" }}>🛡️</span><strong>Centralized Error Handling:</strong> Consistent and meaningful HTTP responses for all exception cases.</li>
        <li><span style={{ fontSize: "1.2rem", marginRight: "0.4rem" }}>🧾</span><strong>Persistent Chat Storage:</strong> PostgreSQL database for structured message history and metadata.</li>
        <li><span style={{ fontSize: "1.2rem", marginRight: "0.4rem" }}>📡</span><strong>WebSocket Security Layer:</strong> Token-based connection validation for all real-time interactions.</li>
        <li><span style={{ fontSize: "1.2rem", marginRight: "0.4rem" }}>📊</span><strong>Comprehensive Logging System:</strong> Includes log levels and error tracing for production debugging.</li>
        <li><span style={{ fontSize: "1.2rem", marginRight: "0.4rem" }}>🐳</span><strong>Deployment Ready:</strong> Docker-based local and cloud deployment.</li>
      </ul>

      <h2 style={{ marginTop: "2rem", color: "#2c3e50" }}>🔧 Tech Stack</h2>
      <p><strong>Django, Django Rest Framework(RESTful API), PostgreSQL, Channels, Redis, Docker & React</strong></p>

      <h2 style={{ marginTop: "2rem", color: "#2c3e50" }}>🚀 Deployment</h2>
      <p><strong>Railway</strong> (previously AWS — switched due to cost).</p>

      <h2 style={{ marginTop: "2rem", color: "#2c3e50" }}>⚠️ Note</h2>
      <p>Message persistence was partially disabled to accommodate free-tier database limitations during deployment.</p>
    </main>
  </div>
);

}

function App() {
  const { user, setUser } = useAuth();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token && !user) {
      fetch(`${backendUrl}/api/users/detail/`, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      })
        .then((res) => {
          if (!res.ok) throw new Error("Failed to fetch user");
          return res.json();
        })
        .then((data) => {
          setUser(data);
        })
        .catch((err) => console.error("User fetch error:", err));
    }
  }, [user, setUser]);

  return (
    <Router>
      <AppHeader />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/register" element={<Register setUser={setUser} />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/" element={<Layout />}>
          <Route index element={<AppLayoutWrapper />} />
          <Route path="chat/:channelId" element={<Chat />} />
        </Route>
        <Route path="/my-channels" element={<MyChannels />} />
        <Route path="/create-channel" element={<CreateChannel />} />
      </Routes>
    </Router>
  );
}

export default App;
