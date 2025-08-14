import React, { useState } from "react";

const backendUrl = process.env.REACT_APP_BACKEND_URL;

const Logout = ({ setUserAuthenticated }) => {
  const [logoutMessage, setLogoutMessage] = useState("");

  const handleLogout = async () => {
    const refresh_token = localStorage.getItem("refresh_token");

    if (!refresh_token) {
      setLogoutMessage("You are not logged in.");
      return;
    }

    try {
      const response = await fetch(`${backendUrl}/api/users/logout/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ refresh_token }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");

        setUserAuthenticated(false);
        setLogoutMessage("Logout successful.");
      } else {
        setLogoutMessage(data.error || "An error occurred during logout.");
      }
    } catch (error) {
      setLogoutMessage("Network error during logout.");
    }
  };

  return (
    <div className="logout-container">
      <h2>Logout</h2>
      <button onClick={handleLogout}>Logout</button>
      {logoutMessage && <p className="message">{logoutMessage}</p>}
    </div>
  );
};

export default Logout;
