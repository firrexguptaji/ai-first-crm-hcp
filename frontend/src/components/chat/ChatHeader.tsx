import { Bot } from "lucide-react";

export default function ChatHeader() {
    return (
        <div className="chat-header">

            <div className="chat-header-title">

                <Bot
                    size={18}
                    className="chat-header-icon"
                />

                <h3>AI Assistant</h3>

            </div>

            <p className="chat-header-subtitle">
                Log interaction via chat
            </p>

        </div>
    );
}