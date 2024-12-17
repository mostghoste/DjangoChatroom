// frontend/src/components/ChatroomList.js

import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api";
import "./ChatroomList.css"; // Create and style this CSS file as needed

function ChatroomList({ onLogout }) {
    const [chatrooms, setChatrooms] = useState([]);
    const [username, setUsername] = useState(localStorage.getItem("username") || "");
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
        navigate("/login");
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
            <Link to="/signup" className="signup-link">Sign Up</Link>
        </div>
    );
}

export default ChatroomList;
