// frontend/src/App.js

import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import ChatroomList from "./components/ChatroomList";
import Chatroom from "./components/Chatroom";
import Login from "./components/Login";
import Signup from "./components/Signup";

function App() {
    const [username, setUsername] = useState(localStorage.getItem("username") || "");

    const handleLoginSuccess = (username) => {
        setUsername(username);
    };

    const handleSignupSuccess = (username) => {
        setUsername(username);
    };

    const handleLogout = () => {
        localStorage.removeItem("token");
        localStorage.removeItem("username");
        setUsername("");
    };

    return (
        <Router>
            <div className="App">
                <Routes>
                    <Route
                        path="/"
                        element={
                            username ? (
                                <ChatroomList onLogout={handleLogout} />
                            ) : (
                                <Navigate to="/login" />
                            )
                        }
                    />
                    <Route
                        path="/login"
                        element={
                            username ? (
                                <Navigate to="/" />
                            ) : (
                                <Login onLoginSuccess={handleLoginSuccess} />
                            )
                        }
                    />
                    <Route
                        path="/signup"
                        element={
                            username ? (
                                <Navigate to="/" />
                            ) : (
                                <Signup onSignupSuccess={handleSignupSuccess} />
                            )
                        }
                    />
                    <Route
                        path="/chatroom/:id"
                        element={
                            username ? <Chatroom /> : <Navigate to="/login" />
                        }
                    />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
