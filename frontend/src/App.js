import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ChatroomList from "./components/ChatroomList";
import Chatroom from "./components/Chatroom";

function App() {
    return (
        <Router>
            <div>
                <h1>Chatroom App</h1>
                <Routes>
                    <Route path="/" element={<ChatroomList />} />
                    <Route path="/chatroom/:id" element={<Chatroom />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
