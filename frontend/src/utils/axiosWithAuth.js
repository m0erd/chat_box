import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: `${backendUrl}/api`,
});

const axiosWithAuth = () => {
  const token = localStorage.getItem("token");
  return axios.create({
    baseURL: `${backendUrl}/api`,
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};

export { axiosInstance, axiosWithAuth };

