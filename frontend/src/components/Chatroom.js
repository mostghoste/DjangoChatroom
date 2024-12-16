import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api";

function Chatroom() {
    const { id } = useParams(); // Chatroom ID from URL
    const [messages, setMessages] = useState([]);
    const [content, setContent] = useState("");
    const [socket, setSocket] = useState(null);

    // Fetch initial messages from the REST API
    const fetchMessages = async () => {
        try {
            const response = await api.get(`/chatrooms/${id}/messages/`);
            setMessages(response.data);
        } catch (error) {
            console.error("Error fetching messages:", error);
        }
    };

    // Initialize WebSocket connection
    useEffect(() => {
        const ws = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${id}/`); // Connect to the WebSocket endpoint
        setSocket(ws);

        // Handle incoming messages
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.message) {
                setMessages((prevMessages) => [...prevMessages, { content: data.message, user: "WebSocket" }]);
            }
        };

        ws.onopen = () => console.log("WebSocket connection opened");
        ws.onclose = () => console.log("WebSocket connection closed");

        return () => ws.close(); // Cleanup on unmount
    }, [id]);

    // Send a message via WebSocket
    const sendMessage = () => {
        if (socket && content.trim()) {
            socket.send(JSON.stringify({ message: content })); // Send message to WebSocket
            setContent(""); // Clear input
        }
    };

    useEffect(() => {
        fetchMessages(); // Load initial messages when component mounts
    }, []);

    return (
        <div>
            <h2>Chatroom {id}</h2>
            <div>
                {messages.map((msg, index) => (
                    <p key={index}>
                        <strong>{msg.user || "User"}:</strong> {msg.content}
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
