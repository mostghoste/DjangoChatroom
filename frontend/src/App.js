import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import ChatroomList from "./components/ChatroomList";
import Chatroom from "./components/Chatroom";
import AuthForm from "./components/AuthForm";
import InvitationList from "./components/InvitationList"; // Import the new InvitationList component

function App() {
    const [username, setUsername] = useState(localStorage.getItem("username") || "");

    const handleAuthSuccess = (username) => {
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
                                <Navigate to="/auth" />
                            )
                        }
                    />
                    <Route
                        path="/auth"
                        element={
                            username ? (
                                <Navigate to="/" />
                            ) : (
                                <AuthForm onAuthSuccess={handleAuthSuccess} />
                            )
                        }
                    />
                    <Route
                        path="/chatroom/:id"
                        element={
                            username ? <Chatroom /> : <Navigate to="/auth" />
                        }
                    />
                    <Route
                        path="/invitations"
                        element={
                            username ? <InvitationList /> : <Navigate to="/auth" />
                        }
                    />
                    <Route
                        path="*"
                        element={<Navigate to={username ? "/" : "/auth"} />}
                    />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
