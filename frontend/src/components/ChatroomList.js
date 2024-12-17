// frontend/src/components/ChatroomList.js

import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api";
import "./ChatroomList.css";

function ChatroomList({ onLogout }) {
    const [chatrooms, setChatrooms] = useState([]);
    const [username, setUsername] = useState(localStorage.getItem("username") || "");
    const [newChatroomName, setNewChatroomName] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const fetchChatrooms = async () => {
        try {
            const response = await api.get("/chatrooms/");
            setChatrooms(response.data);
        } catch (error) {
            console.error("Error fetching chatrooms:", error);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem("token");
        localStorage.removeItem("username");
        onLogout();
        navigate("/auth");
    };

    const handleCreateChatroom = async (e) => {
        e.preventDefault();
        setError("");
        if (!newChatroomName.trim()) {
            setError("Chatroom name cannot be empty.");
            return;
        }
        try {
            const response = await api.post("/chatrooms/", { name: newChatroomName });
            setChatrooms([...chatrooms, response.data]);
            setNewChatroomName("");
        } catch (err) {
            console.error("Error creating chatroom:", err.response);
            setError(err.response.data.detail || "Failed to create chatroom.");
        }
    };

    useEffect(() => {
        fetchChatrooms();
    }, []);

    return (
        <div className="chatroom-list-container">
            <h2>Welcome, {username}!</h2>
            <button onClick={handleLogout} className="logout-button">Logout</button>
            <h2>Chatrooms</h2>
            <ul>
                {chatrooms.map((room) => (
                    <li key={room.id}>
                        <Link to={`/chatroom/${room.id}`}>{room.name}</Link>
                    </li>
                ))}
            </ul>
            <form onSubmit={handleCreateChatroom} className="create-chatroom-form">
                <input
                    type="text"
                    value={newChatroomName}
                    onChange={(e) => setNewChatroomName(e.target.value)}
                    placeholder="New Chatroom Name"
                    required
                />
                <button type="submit">Create Chatroom</button>
            </form>
            {error && <p className="error">{error}</p>}
            <Link to="/invitations" className="invitation-link">View Invitations</Link>
        </div>
    );
}

export default ChatroomList;
