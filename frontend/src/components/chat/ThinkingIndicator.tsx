import { Bot } from "lucide-react";

/**
 * Shown as an assistant bubble while a request is in progress.
 */
export default function ThinkingIndicator() {
    return (
        <div
            className="chat-message assistant-message thinking-message"
            aria-live="polite"
        >

            <div className="message-avatar">
                <Bot size={18} />
            </div>

            <div className="message-content">

                <div className="message-header">
                    <span className="sender-name">
                        AI Assistant
                    </span>
                </div>

                <div className="message-bubble thinking-bubble">

                    <span className="thinking-dots" aria-hidden="true">
                        <span />
                        <span />
                        <span />
                    </span>

                    <span className="thinking-text">
                        Thinking…
                    </span>

                </div>

            </div>

        </div>
    );
}
