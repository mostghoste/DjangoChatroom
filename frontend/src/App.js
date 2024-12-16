import React, { useEffect, useState } from "react";
import api from "./api";

function App() {
    const [chatrooms, setChatrooms] = useState([]);
    const [token, setToken] = useState(localStorage.getItem("token") || "");

    // Fetch Chatrooms
    const fetchChatrooms = async () => {
        try {
            const response = await api.get("/chatrooms/");
            setChatrooms(response.data);
        } catch (error) {
            console.error("Error fetching chatrooms:", error);
        }
    };

    // Login Function
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

    // Fetch chatrooms on load if token exists
    useEffect(() => {
        if (token) fetchChatrooms();
    }, [token]);

    return (
        <div>
            <h1>Chatroom App</h1>
            {!token ? (
                <div>
                    <button onClick={login}>Login</button>
                </div>
            ) : (
                <div>
                    <h2>Chatrooms</h2>
                    <ul>
                        {chatrooms.map((room) => (
                            <li key={room.id}>{room.name}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default App;
