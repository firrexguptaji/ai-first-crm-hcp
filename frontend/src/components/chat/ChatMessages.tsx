import { useEffect, useRef } from "react";

import ChatMessage from "./ChatMessage";
import ThinkingIndicator from "./ThinkingIndicator";

import {
    useAppDispatch,
    useAppSelector,
} from "../../app/hooks";

import {
    removeMessage,
    sendChatMessage,
} from "../../features/chat/chatSlice";

const WELCOME_MESSAGE =
    "Hello! I'm your AI CRM Assistant. Tell me about your interaction with an HCP.";

export default function ChatMessages() {

    const dispatch = useAppDispatch();

    // Failed requests are added to `messages` with status "error",
    // so they appear in order with the rest of the conversation.
    const { messages, loading } = useAppSelector(
        (state) => state.chat
    );

    const endRef = useRef<HTMLDivElement>(null);

    // Keep the newest message (or the thinking indicator) in view.
    useEffect(() => {
        endRef.current?.scrollIntoView({
            behavior: "smooth",
            block: "end",
        });
    }, [messages.length, loading]);

    const retry = (id: string, message: string) => {
        dispatch(removeMessage(id));
        dispatch(sendChatMessage({ message }));
    };

    return (
        <div className="chat-messages">

            {messages.length === 0 && (
                <ChatMessage
                    sender="assistant"
                    message={WELCOME_MESSAGE}
                />
            )}

            {messages.map((message) => {

                const retryMessage = message.retryMessage;

                return (
                    <ChatMessage
                        key={message.id}
                        sender={message.role}
                        message={message.content}
                        status={message.status}
                        onRetry={
                            retryMessage
                                ? () => retry(message.id, retryMessage)
                                : undefined
                        }
                        retryDisabled={loading}
                    />
                );
            })}

            {loading && <ThinkingIndicator />}

            <div ref={endRef} />

        </div>
    );
}
