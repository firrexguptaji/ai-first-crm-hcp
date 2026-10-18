import {
    AlertCircle,
    AlertTriangle,
    Bot,
    Info,
    RotateCcw,
    User,
} from "lucide-react";

import type { ChatMessageStatus } from "../../types/redux";

interface ChatMessageProps {
    sender: "user" | "assistant";
    message: string;
    time?: string;
    status?: ChatMessageStatus;
    /** Shown as a Retry button on failed replies. */
    onRetry?: () => void;
    retryDisabled?: boolean;
}

const STATUS_ICONS = {
    notice: <AlertCircle size={14} />,
    info: <Info size={14} />,
    error: <AlertTriangle size={14} />,
};

export default function ChatMessage({
    sender,
    message,
    time,
    status = "ok",
    onRetry,
    retryDisabled = false,
}: ChatMessageProps) {

    const isUser = sender === "user";
    const icon = status === "ok" ? null : STATUS_ICONS[status];

    return (

        <div
            className={`chat-message ${
                isUser
                ? "user-message"
                : "assistant-message"
            } message-${status}`}
            data-role={sender}
            role={status === "error" ? "alert" : undefined}
        >

            <div className="message-avatar">
                {isUser ? <User size={18}/> : <Bot size={18}/>}
            </div>

            <div className="message-content">

                <div className="message-header">

                    <span className="sender-name">
                        {isUser ? "You" : "AI Assistant"}
                    </span>

                    {time && (
                        <time className="message-time">
                            {time}
                        </time>
                    )}

                </div>

                <div className="message-bubble">

                    {icon && (
                        <span className="message-status-icon">
                            {icon}
                        </span>
                    )}

                    {message}

                </div>

                {onRetry && (
                    <button
                        type="button"
                        className="message-retry"
                        onClick={onRetry}
                        disabled={retryDisabled}
                    >
                        <RotateCcw size={14} />
                        Retry
                    </button>
                )}

            </div>

        </div>

    );
}
