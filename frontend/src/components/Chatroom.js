// frontend/src/components/Chatroom.js

import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api";
import "./Chatroom.css"; // Ensure this CSS file includes styles for members-container

function Chatroom() {
    const { id } = useParams(); // Chatroom ID from URL
    const [messages, setMessages] = useState([]);
    const [members, setMembers] = useState([]); // State for chatroom members
    const [content, setContent] = useState("");
    const [socket, setSocket] = useState(null);
    const [chatroomName, setChatroomName] = useState("");
    const [inviteUsername, setInviteUsername] = useState("");
    const [inviteError, setInviteError] = useState("");
    const [inviteSuccess, setInviteSuccess] = useState("");

    // Fetch chatroom details, messages, and members
    const fetchChatroomDetails = async () => {
        try {
            const response = await api.get(`/chatrooms/${id}/`);
            setChatroomName(response.data.name);
        } catch (error) {
            console.error("Error fetching chatroom details:", error);
        }
    };

    const fetchMessages = async () => {
        try {
            const response = await api.get(`/chatrooms/${id}/messages/`);
            setMessages(response.data);
        } catch (error) {
            console.error("Error fetching messages:", error);
        }
    };

    const fetchMembers = async () => {
        try {
            const response = await api.get(`/chatrooms/${id}/members/`);
            setMembers(response.data);
        } catch (error) {
            console.error("Error fetching members:", error);
        }
    };

    // Initialize WebSocket connection
    useEffect(() => {
        const token = localStorage.getItem("token");
        const ws = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${id}/?token=${token}`);
        setSocket(ws);

        // Handle incoming messages
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.message && data.user) {
                setMessages((prevMessages) => [
                    ...prevMessages,
                    { content: data.message, user: data.user, timestamp: data.timestamp },
                ]);
            }
        };

        ws.onopen = () => console.log("WebSocket connection opened");
        ws.onclose = () => console.log("WebSocket connection closed");

        return () => ws.close(); // Cleanup on unmount
    }, [id]);

    // Fetch chatroom details, messages, and members on mount
    useEffect(() => {
        fetchChatroomDetails();
        fetchMessages();
        fetchMembers();
    }, [id]);

    // Send a message via WebSocket
    const sendMessage = () => {
        if (socket && content.trim()) {
            socket.send(JSON.stringify({ message: content })); // Send message to WebSocket
            setContent(""); // Clear input
        }
    };

    // Invite a user to the chatroom
    const handleInvite = async (e) => {
        e.preventDefault();
        setInviteError("");
        setInviteSuccess("");
        if (!inviteUsername.trim()) {
            setInviteError("Username cannot be empty.");
            return;
        }
        try {
            const response = await api.post("/invitations/", {
                recipient: inviteUsername,
                chatroom: chatroomName,
            });
            setInviteSuccess(`Invitation sent to ${inviteUsername}.`);
            setInviteUsername("");
            fetchMembers(); // Refresh members list after sending invitation
        } catch (err) {
            console.error("Error sending invitation:", err.response);
            setInviteError(err.response.data.detail || "Failed to send invitation.");
        }
    };

    return (
        <div className="chatroom-container">
            <h2>Chatroom: {chatroomName}</h2>

            {/* Members List */}
            <div className="members-container">
                <h3>Members</h3>
                <ul>
                    {members.map((member) => (
                        <li key={member.id}>{member.username}</li>
                    ))}
                </ul>
            </div>

            {/* Messages */}
            <div className="messages-container">
                {messages.map((msg, index) => (
                    <p key={index}>
                        <strong>{msg.user || "User"}:</strong> {msg.content}{" "}
                        <em>({new Date(msg.timestamp).toLocaleTimeString()})</em>
                    </p>
                ))}
            </div>

            {/* Message Input */}
            <div className="message-input-container">
                <input
                    type="text"
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    placeholder="Type your message..."
                />
                <button onClick={sendMessage}>Send</button>
            </div>

            {/* Invite User */}
            <div className="invite-container">
                <h3>Invite User</h3>
                <form onSubmit={handleInvite}>
                    <input
                        type="text"
                        value={inviteUsername}
                        onChange={(e) => setInviteUsername(e.target.value)}
                        placeholder="Username to invite"
                        required
                    />
                    <button type="submit">Invite</button>
                </form>
                {inviteError && <p className="error">{inviteError}</p>}
                {inviteSuccess && <p className="success">{inviteSuccess}</p>}
            </div>
        </div>
    );
}

export default Chatroom;
