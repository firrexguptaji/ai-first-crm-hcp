import { Bot } from "lucide-react";

export default function EmptyChat() {
    return (
        <div className="empty-chat">

            <Bot size={48} />

            <h3>Start a Conversation</h3>

            <p>
                Describe your interaction with a Healthcare Professional.
            </p>

            <p className="chat-example">
                Example:
            </p>

            <code>
                "Met Dr. Alice Brown today to discuss Product A..."
            </code>

        </div>
    );
}