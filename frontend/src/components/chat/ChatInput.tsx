import { SendHorizontal } from "lucide-react";

export default function ChatInput() {
    return (
        <div className="chat-input-container">

            <textarea
                className="chat-input"
                placeholder="Describe your interaction with the HCP..."
                rows={3}
            />

            <div className="chat-actions">

                <button
                    type="button"
                    className="send-button"
                >
                    <SendHorizontal size={16} />

                    <span>Send</span>
                </button>

            </div>

        </div>
    );
}