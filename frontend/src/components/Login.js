// frontend/src/components/Login.js

import React, { useState } from "react";
import api from "../api";
import "./Login.css"; // Create and style this CSS file as needed

function Login({ onLoginSuccess }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post("/token/", {
                username,
                password,
            });
            const { token } = response.data;
            // Fetch user details if necessary or assume username from input
            localStorage.setItem("token", token);
            localStorage.setItem("username", username);
            onLoginSuccess(username);
        } catch (err) {
            console.error("Login failed:", err.response);
            setError("Invalid credentials. Please try again.");
        }
    };

    return (
        <div className="login-container">
            <h2>Login</h2>
            {error && <p className="error">{error}</p>}
            <form onSubmit={handleLogin}>
                <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Username"
                    required
                />
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                    required
                />
                <button type="submit">Login</button>
            </form>
        </div>
    );
}

export default Login;
