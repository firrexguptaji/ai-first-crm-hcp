import { createSlice } from "@reduxjs/toolkit";

import type { ChatState } from "../../types/redux";

const initialState: ChatState = {
    messages: [],
    loading: false,
};

const chatSlice = createSlice({
    name: "chat",
    initialState,
    reducers: {},
});

export default chatSlice.reducer;