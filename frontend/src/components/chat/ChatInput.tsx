import { useState } from "react";
import { SendHorizontal } from "lucide-react";

import Button from "../common/Button";

import {
    addUserMessage,
    sendChatMessage,
} from "../../features/chat/chatSlice";

import {
    useAppDispatch,
    useAppSelector,
} from "../../app/hooks";


export default function ChatInput() {

    const dispatch = useAppDispatch();

    const { loading } = useAppSelector(
        (state) => state.chat
    );
    const [message, setMessage] = useState("");

    

    const handleSend = () => {
        const trimmedMessage = message.trim();

        if (!trimmedMessage) {
            return;
        }

        dispatch(
            addUserMessage({
                id: crypto.randomUUID(),
                role: "user",
                content: trimmedMessage,
            })
        );

        dispatch(
            sendChatMessage({
                message: trimmedMessage,
            })
        );

        setMessage("");

    };

    return (
        <div className="chat-input-container">

            <textarea
                className="chat-input"
                placeholder="Describe your interaction with the HCP..."
                rows={3}
                value={message}
                disabled={loading}
                onChange={(event) =>
                    setMessage(event.target.value)
                }
            />

            <div className="chat-actions">

                <Button
                    type="button"
                    onClick={handleSend}
                    disabled={loading || !message.trim()}
                >
                    <SendHorizontal size={16} />
                    <span>
                        {loading ? "Sending..." : "Send"}
                    </span>
                </Button>

            </div>

        </div>
    );
}