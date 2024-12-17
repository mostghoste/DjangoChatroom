// frontend/src/api.js

import axios from "axios";

// Create an Axios instance with the backend URL
const api = axios.create({
    baseURL: "http://127.0.0.1:8000/api", // Django API endpoint
    headers: {
        "Content-Type": "application/json",
    },
});

// Automatically add the token to requests if it exists
api.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) {
        config.headers.Authorization = `Token ${token}`;
    }
    return config;
});

axios.defaults.withCredentials = true;

export default api;
