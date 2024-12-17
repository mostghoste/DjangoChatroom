// frontend/src/components/Signup.js

import React, { useState } from "react";
import api from "../api";
import "./Signup.css"; // Create and style this CSS file as needed

function Signup({ onSignupSuccess }) {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [password2, setPassword2] = useState("");
    const [error, setError] = useState("");

    const handleSignup = async (e) => {
        e.preventDefault();
        if (password !== password2) {
            setError("Passwords do not match.");
            return;
        }
        try {
            const response = await api.post("/register/", {
                username,
                email,
                password,
                password2,
            });
            const { token, user } = response.data;
            // Store token and username
            localStorage.setItem("token", token);
            localStorage.setItem("username", user.username);
            onSignupSuccess(user.username);
        } catch (err) {
            console.error("Signup failed:", err.response);
            setError(err.response.data);
        }
    };

    return (
        <div className="signup-container">
            <h2>Sign Up</h2>
            {error && <p className="error">{JSON.stringify(error)}</p>}
            <form onSubmit={handleSignup}>
                <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Username"
                    required
                />
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Email"
                />
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                    required
                />
                <input
                    type="password"
                    value={password2}
                    onChange={(e) => setPassword2(e.target.value)}
                    placeholder="Confirm Password"
                    required
                />
                <button type="submit">Sign Up</button>
            </form>
        </div>
    );
}

export default Signup;
