import { Bot, User } from "lucide-react";

interface ChatMessageProps {
    sender: "user" | "assistant";
    message: string;
    time?: string;
}

export default function ChatMessage({
    sender,
    message,
    time,
}: ChatMessageProps) {

    const isUser = sender === "user";

    return (

        <div
            className={`chat-message ${
                isUser
                ? "user-message"
                : "assistant-message"
            }`}
            data-role={sender}
        >

            <div className="message-avatar">
                {isUser ? <User size={18}/> : <Bot size={18}/>}
            </div>

            <div className="message-content">

                <div className="message-header">

                    <span className="sender-name">
                        {isUser ? "You" : "AI Assistant"}
                    </span>

                    <span className="message-time">
                        {time}
                    </span>

                </div>

                <div className="message-bubble">
                    {message}
                </div>

            </div>

        </div>

    );
}