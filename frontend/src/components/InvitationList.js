import React, { useEffect, useState } from "react";
import api from "../api";
import "./InvitationList.css"; // Create and style this CSS file as needed

function InvitationList() {
    const [invitations, setInvitations] = useState([]);
    const [error, setError] = useState("");

    const fetchInvitations = async () => {
        try {
            const response = await api.get("/invitations/incoming/");
            setInvitations(response.data);
        } catch (error) {
            console.error("Error fetching invitations:", error);
            setError("Failed to load invitations.");
        }
    };

    const handleAccept = async (invitationId) => {
        try {
            await api.put(`/invitations/${invitationId}/accept/`);
            // Remove the accepted invitation from the list
            setInvitations(invitations.filter(inv => inv.id !== invitationId));
        } catch (err) {
            console.error("Error accepting invitation:", err.response);
            setError(err.response.data.detail || "Failed to accept invitation.");
        }
    };

    const handleDecline = async (invitationId) => {
        try {
            await api.put(`/invitations/${invitationId}/decline/`);
            // Remove the declined invitation from the list
            setInvitations(invitations.filter(inv => inv.id !== invitationId));
        } catch (err) {
            console.error("Error declining invitation:", err.response);
            setError(err.response.data.detail || "Failed to decline invitation.");
        }
    };

    useEffect(() => {
        fetchInvitations();
    }, []);

    return (
        <div className="invitation-list-container">
            <h2>Incoming Invitations</h2>
            {error && <p className="error">{error}</p>}
            {invitations.length === 0 ? (
                <p>No incoming invitations.</p>
            ) : (
                <ul>
                    {invitations.map((inv) => (
                        <li key={inv.id}>
                            <p>
                                <strong>{inv.sender}</strong> has invited you to join <strong>{inv.chatroom}</strong>.
                            </p>
                            <button onClick={() => handleAccept(inv.id)}>Accept</button>
                            <button onClick={() => handleDecline(inv.id)}>Decline</button>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default InvitationList;
