import React, { useState } from "react";

const Logout = ({ setUserAuthenticated }) => {
  const [logoutMessage, setLogoutMessage] = useState("");

  const handleLogout = async () => {
    const refresh_token = localStorage.getItem("refresh_token");

    if (!refresh_token) {
      setLogoutMessage("You are not logged in.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8001/api/users/logout/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ refresh_token }),
      });

      const data = await response.json();

      if (response.ok) {
        // Clear tokens from localStorage
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
