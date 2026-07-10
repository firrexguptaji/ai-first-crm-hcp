import { createSlice } from "@reduxjs/toolkit";

import type { AppState } from "../../types/redux";

const initialState: AppState = {
    loading: false,
};

const appSlice = createSlice({
    name: "app",
    initialState,
    reducers: {},
});

export default appSlice.reducer;