import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api";

function ChatroomList() {
    const [chatrooms, setChatrooms] = useState([]);
    const [token, setToken] = useState(localStorage.getItem("token") || "");

    const fetchChatrooms = async () => {
        try {
            const response = await api.get("/chatrooms/");
            setChatrooms(response.data);
        } catch (error) {
            console.error("Error fetching chatrooms:", error);
        }
    };

    const login = async () => {
        try {
            const response = await api.post("/token/", {
                username: "mostghoste",
                password: "demo",
            });
            const token = response.data.token;
            localStorage.setItem("token", token);
            setToken(token);
            fetchChatrooms();
        } catch (error) {
            console.error("Login failed:", error);
        }
    };

    useEffect(() => {
        if (token) fetchChatrooms();
    }, [token]);

    return (
        <div>
            {!token ? (
                <button onClick={login}>Login</button>
            ) : (
                <div>
                    <h2>Chatrooms</h2>
                    <ul>
                        {chatrooms.map((room) => (
                            <li key={room.id}>
                                <Link to={`/chatroom/${room.id}`}>{room.name}</Link>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default ChatroomList;