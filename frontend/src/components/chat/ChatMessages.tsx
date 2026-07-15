import ChatMessage from "./ChatMessage";

const messages = [
    {
        id: 1,
        sender: "assistant",
        message:
            "Hello! I'm your AI CRM Assistant. Tell me about your interaction with an HCP.",
        time: "10:00 AM",
    },
    {
        id: 2,
        sender: "user",
        message:
            "I met Dr. Alice Brown today regarding Product A.",
        time: "10:01 AM",
    },
] as const;

export default function ChatMessages() {
    return (
        <div className="chat-messages">

            {messages.map((message) => (
                <ChatMessage
                    key={message.id}
                    sender={message.sender}
                    message={message.message}
                    time={message.time}
                />
            ))}

        </div>
    );
}