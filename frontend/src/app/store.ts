import { configureStore } from "@reduxjs/toolkit";

import chatReducer from "../features/chat/chatSlice";
import interactionReducer from "../features/interaction/interactionSlice";
import appReducer from "../features/app/appSlice";

export const store = configureStore({
    reducer: {
        app: appReducer,
        chat: chatReducer,
        interaction: interactionReducer,
    },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;