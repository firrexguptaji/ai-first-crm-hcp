import {
    createAsyncThunk,
    createSlice,
} from "@reduxjs/toolkit";

import { sendMessage } from "../../api/chatApi";

import type {
    ChatRequest,
    ChatResponse,
} from "../../types/chat";

import type { ChatState } from "../../types/redux";

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
        } catch (error: any) {
            return thunkAPI.rejectWithValue(
                error.message ?? "Failed to send chat message"
            );
        }
    }
);

const chatSlice = createSlice({
    name: "chat",

    initialState,

    reducers: {

            addUserMessage: (state, action) => {

            state.messages.push(action.payload);
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

                state.messages.push({
                    id: crypto.randomUUID(),
                    role: "assistant",
                    content: action.payload.response,
                });
            })

            .addCase(sendChatMessage.rejected, (state, action) => {
                state.loading = false;
                state.error =
                    action.payload ??
                    "Failed to send chat message";
            });

    },

});

export const {
    addUserMessage,
} = chatSlice.actions;

export default chatSlice.reducer;