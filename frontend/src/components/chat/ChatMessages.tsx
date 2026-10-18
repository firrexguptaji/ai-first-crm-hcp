import ChatMessage from "./ChatMessage";

import { useAppSelector } from "../../app/hooks";

const WELCOME_MESSAGE =
    "Hello! I'm your AI CRM Assistant. Tell me about your interaction with an HCP.";

export default function ChatMessages() {

    // Failed requests are added to `messages` with status "error",
    // so they appear in order with the rest of the conversation.
    const { messages } = useAppSelector(
        (state) => state.chat
    );

    return (
        <div className="chat-messages">

            {messages.length === 0 && (
                <ChatMessage
                    sender="assistant"
                    message={WELCOME_MESSAGE}
                />
            )}

            {messages.map((message) => (

                <ChatMessage
                    key={message.id}
                    sender={message.role}
                    message={message.content}
                />

            ))}

        </div>
    );
}
