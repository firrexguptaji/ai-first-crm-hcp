import {
    createAsyncThunk,
    createSlice,
    type PayloadAction,
} from "@reduxjs/toolkit";

import { sendMessage } from "../../api/chatApi";
import { getErrorMessage } from "../../api/errors";

import type {
    ChatRequest,
    ChatResponse,
    ToolOutput,
} from "../../types/chat";

import type {
    ChatMessage,
    ChatMessageStatus,
    ChatState,
} from "../../types/redux";

const initialState: ChatState = {
    messages: [],
    loading: false,
    error: null,
};

export const sendChatMessage = createAsyncThunk<
    ChatResponse,
    ChatRequest,
    { rejectValue: string }
>(
    "chat/sendMessage",
    async (data, thunkAPI) => {
        try {
            return await sendMessage(data);
        } catch (error: unknown) {
            return thunkAPI.rejectWithValue(getErrorMessage(error));
        }
    }
);

/**
 * Display status for a reply returned by the backend.
 */
export function replyStatus(output: ToolOutput): ChatMessageStatus {

    if (output.success) {
        return "ok";
    }

    switch (output.error_type) {
        case "unsupported":
            return "info";
        case "internal":
            return "error";
        default:
            return "notice";
    }
}

const chatSlice = createSlice({
    name: "chat",

    initialState,

    reducers: {

        addUserMessage: (state, action: PayloadAction<ChatMessage>) => {
            state.messages.push(action.payload);
        },

        /** Remove a message, e.g. a failed reply before retrying. */
        removeMessage: (state, action: PayloadAction<string>) => {
            state.messages = state.messages.filter(
                (message) => message.id !== action.payload
            );
        },

    },

    extraReducers: (builder) => {

        builder

            .addCase(sendChatMessage.pending, (state) => {
                state.loading = true;
                state.error = null;
            })

            .addCase(sendChatMessage.fulfilled, (state, action) => {
                state.loading = false;

                const status = replyStatus(action.payload.tool_output);

                state.messages.push({
                    id: crypto.randomUUID(),
                    role: "assistant",
                    content: action.payload.response,
                    status,
                    // Internal errors can be retried with the same message.
                    retryMessage:
                        status === "error"
                            ? action.meta.arg.message
                            : undefined,
                });
            })

            .addCase(sendChatMessage.rejected, (state, action) => {
                state.loading = false;

                const message =
                    action.payload ??
                    "Something went wrong. Please try again.";

                state.error = message;

                state.messages.push({
                    id: crypto.randomUUID(),
                    role: "assistant",
                    content: message,
                    status: "error",
                    retryMessage: action.meta.arg.message,
                });
            });

    },

});

export const {
    addUserMessage,
    removeMessage,
} = chatSlice.actions;

export default chatSlice.reducer;
