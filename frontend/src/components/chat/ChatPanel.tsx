import ChatHeader from "./ChatHeader";
import ChatMessages from "./ChatMessages";
import ChatInput from "./ChatInput";

import "./chat.css";

export default function ChatPanel() {
    return (
        <div className="chat-panel">
            <ChatHeader />

            <ChatMessages />

            <ChatInput />
        </div>
    );
}