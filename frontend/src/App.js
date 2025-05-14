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
  const { user, logoutUser } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logoutUser();
    navigate("/");
    window.location.reload();
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
      <div className="col-md-3 sidebar">
        <h4>Channels</h4>
        <ul className="list-group">
          {channels.map((channel) => (
            <li key={channel.id} className="list-group-item">
              <button
                className="btn btn-link"
                onClick={() => handleChannelClick(channel.id)}
              >
                {channel.name}
              </button>
            </li>
          ))}
        </ul>
      </div>
      <div className="col-md-9 chat-panel">
        <iframe
          src="/app_info.html"
          title="About Chat App"
          style={{ width: "100%", height: "500px", border: "none" }}
        ></iframe>
      </div>
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


