import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api";

function Chatroom() {
    const { id } = useParams();
    const [messages, setMessages] = useState([]);
    const [content, setContent] = useState("");

    const fetchMessages = async () => {
        try {
            const response = await api.get(`/chatrooms/${id}/messages/`);
            setMessages(response.data);
        } catch (error) {
            console.error("Error fetching messages:", error);
        }
    };

    const sendMessage = async () => {
        try {
            await api.post(`/chatrooms/${id}/messages/`, { content });
            setContent(""); // Clear input
            fetchMessages(); // Refresh messages
        } catch (error) {
            console.error("Error sending message:", error);
        }
    };

    useEffect(() => {
        fetchMessages();
    }, []);

    return (
        <div>
            <h2>Chatroom {id}</h2>
            <div>
                {messages.map((msg) => (
                    <p key={msg.id}>
                        <strong>{msg.user}</strong>: {msg.content}
                    </p>
                ))}
            </div>
            <input
                type="text"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Type your message..."
            />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
}

export default Chatroom;
