import ChatMessage from "./ChatMessage";

import { useAppSelector } from "../../app/hooks";

export default function ChatMessages() {

    const { messages, error } = useAppSelector(
        (state) => state.chat
    );

    if (messages.length === 0) {
        return (
            <div className="chat-messages">

                <ChatMessage
                    sender="assistant"
                    message="Hello! I'm your AI CRM Assistant. Tell me about your interaction with an HCP."
                />

                {error && (
                    <ChatMessage
                        sender="assistant"
                        message={error}
                    />
                )}

            </div>
        );
    }

    return (
        <div className="chat-messages">

            {messages.map((message) => (

                <ChatMessage
                    key={message.id}
                    sender={message.role}
                    message={message.content}
                />

            ))}

            {error && (

                <ChatMessage
                    sender="assistant"
                    message={error}
                />

            )}

        </div>
    );
}