import axios from 'axios';

// Base instance without auth, can be used for public requests
const axiosInstance = axios.create({
  baseURL: 'http://localhost:8001/api',
});

// Function to create an Axios instance with Authorization header
const axiosWithAuth = () => {
  const token = localStorage.getItem("token");
  return axios.create({
    baseURL: "http://localhost:8001/api",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};

export { axiosInstance, axiosWithAuth };

