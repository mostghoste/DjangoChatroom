// frontend/src/components/AuthForm.js

import React, { useState } from "react";
import api from "../api";
import "./AuthForm.css"; // We'll create this CSS file for styling

function AuthForm({ onAuthSuccess }) {
    const [isSignup, setIsSignup] = useState(false);
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [password2, setPassword2] = useState("");
    const [error, setError] = useState("");

    const handleToggle = () => {
        setIsSignup(!isSignup);
        setError("");
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(""); // Reset error message

        if (isSignup) {
            // Signup Logic
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
                onAuthSuccess(user.username);
            } catch (err) {
                console.error("Signup failed:", err.response);
                // Extract and display error messages
                const errorMessages = Object.values(err.response.data).flat();
                setError(errorMessages.join(" "));
            }
        } else {
            // Login Logic
            try {
                const response = await api.post("/token/", {
                    username,
                    password,
                });
                const { token } = response.data;
                // Store token and username
                localStorage.setItem("token", token);
                localStorage.setItem("username", username);
                onAuthSuccess(username);
            } catch (err) {
                console.error("Login failed:", err.response);
                setError("Invalid credentials. Please try again.");
            }
        }
    };

    return (
        <div className="auth-form-container">
            <h2>{isSignup ? "Sign Up" : "Login"}</h2>
            {error && <p className="error">{error}</p>}
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Username"
                    required
                />
                {isSignup && (
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Email"
                        required
                    />
                )}
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                    required
                />
                {isSignup && (
                    <input
                        type="password"
                        value={password2}
                        onChange={(e) => setPassword2(e.target.value)}
                        placeholder="Confirm Password"
                        required
                    />
                )}
                <button type="submit">{isSignup ? "Sign Up" : "Login"}</button>
            </form>
            <p>
                {isSignup ? "Already have an account?" : "Don't have an account?"}{" "}
                <button onClick={handleToggle} className="toggle-button">
                    {isSignup ? "Login" : "Sign Up"}
                </button>
            </p>
        </div>
    );
}

export default AuthForm;
