import { SendHorizontal } from "lucide-react";
import Button from "../common/Button";

export default function ChatInput() {
    return (
        <div className="chat-input-container">

            <textarea
                className="chat-input"
                placeholder="Describe your interaction with the HCP..."
                rows={3}
            />

            <div className="chat-actions">

                <Button type="button">

                    <SendHorizontal size={16} />

                    <span>Send</span>

                </Button>

            </div>

        </div>
    );
}