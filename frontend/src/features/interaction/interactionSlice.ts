import { createSlice } from "@reduxjs/toolkit";

import type { InteractionState } from "../../types/redux";

const initialState: InteractionState = {
    hcpName: "",
    interactionDate: "",
    channel: "",
    rawNotes: "",
    summary: "",
    sentiment: "",
    productsDiscussed: [],
    followUpRequired: false,
    followUpDate: "",
};

const interactionSlice = createSlice({
    name: "interaction",
    initialState,
    reducers: {},
});

export default interactionSlice.reducer;