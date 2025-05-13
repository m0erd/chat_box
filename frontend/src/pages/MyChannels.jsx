import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const backendUrl = process.env.REACT_APP_BACKEND_URL;

const MyChannels = () => {
  const accessToken = localStorage.getItem("access_token");
  const [channels, setChannels] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchChannels = async () => {
      try {
        const res = await fetch(`${backendUrl}/api/channels/my/`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        if (!res.ok) {
          throw new Error("Failed to fetch channels");
        }

        const data = await res.json();
        console.log("Fetched channels:", data);

        setChannels(data);
      } catch (err) {
        console.error(err);
      }
    };

    if (accessToken) {
      fetchChannels();
    }
  }, [accessToken]);

  if (!accessToken) return <div>User not authenticated.</div>;

  return (
    <div style={{ padding: "20px", maxWidth: "600px", margin: "0 auto" }}>
      <h2 style={{ marginBottom: "20px" }}>My Channels</h2>
      {channels.length > 0 ? (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {channels.map((channel) => (
            <li
              key={channel.id}
              onClick={() => navigate(`/chat/${channel.id}`)}
              style={{
                padding: "16px",
                marginBottom: "12px",
                border: "1px solid #ccc",
                borderRadius: "8px",
                backgroundColor: "#f0f4f8",
                cursor: "pointer",
                boxShadow: "0 2px 4px rgba(0, 0, 0, 0.05)",
                transition: "background-color 0.2s ease",
              }}
              onMouseEnter={(e) =>
                (e.currentTarget.style.backgroundColor = "#e6ecf1")
              }
              onMouseLeave={(e) =>
                (e.currentTarget.style.backgroundColor = "#f0f4f8")
              }
            >
              <strong>{channel.name}</strong>
            </li>
          ))}
        </ul>
      ) : (
        <p>No channels found</p>
      )}
    </div>
  );
};

export default MyChannels;
