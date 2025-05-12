import React, { createContext, useContext, useEffect, useState } from 'react';
import { jwtDecode } from 'jwt-decode';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  const login = (userData, access, refresh) => {
    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
    setUser(userData);
  };

  const refreshAccessToken = async () => {
    const refreshToken = localStorage.getItem("refresh_token");
    if (!refreshToken) return null;
  
    try {
      const res = await fetch("http://localhost:8001/api/token/refresh/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh: refreshToken }),
      });
  
      if (!res.ok) throw new Error("Failed to refresh token");
  
      const data = await res.json();
      localStorage.setItem("access_token", data.access);
      return data.access;
    } catch (err) {
      console.error("Token refresh error:", err);
      logoutUser();
      return null;
    }
  };

  useEffect(() => {
    const fetchUser = async () => {
      let accessToken = localStorage.getItem("access_token");
      if (!accessToken) return;
  
      let res = await fetch("http://localhost:8001/api/users/detail/", {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
  
      if (res.status === 401) {
        accessToken = await refreshAccessToken();
        if (!accessToken) return;
  
        res = await fetch("http://localhost:8001/api/users/detail/", {
          headers: { Authorization: `Bearer ${accessToken}` },
        });
      }
  
      if (res.ok) {
        const data = await res.json();
        setUser(data);
      } else {
        console.error("Failed to fetch user even after refresh.");
        setUser(null);
      }
    };
  
    fetchUser();
  }, []);
  
  const loginUser = (token) => {
    if (typeof token !== 'string') {
      console.error('Invalid token passed to loginUser:', token);
      return;
    }

    try {
      const decoded = jwtDecode(token);
      localStorage.setItem('access_token', token);
      setUser({ user_id: decoded.user_id });

      fetch("http://localhost:8001/api/users/detail/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((res) => {
          if (!res.ok) throw new Error("Failed to fetch user");
          return res.json();
        })
        .then((data) => {
          console.log("Fetched user details after login:", data);
          setUser(data);
        })
        .catch((err) => {
          console.error("Could not load user info:", err);
        });

    } catch (error) {
      console.error('Failed to decode token:', error);
    }
  };

  const logoutUser = async () => {
    const refreshToken = localStorage.getItem("refresh_token");

    try {
      if (refreshToken) {
        await fetch("http://localhost:8001/api/users/logout/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ refresh_token: refreshToken }),
        });
      }
    } catch (error) {
      console.error("Logout failed:", error);
    } finally {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider value={{ user, setUser, loginUser, logoutUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
