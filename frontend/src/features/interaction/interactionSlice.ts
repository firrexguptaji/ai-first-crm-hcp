import { createSlice } from "@reduxjs/toolkit";

import { sendChatMessage } from "../chat/chatSlice";
import { toInteractionState } from "./mappers";

import {
    isFollowUpOutput,
    isHistoryOutput,
    isInteractionOutput,
} from "../../types/chat";

import type { InteractionState } from "../../types/redux";

const initialState: InteractionState = {
    interactionId: null,
    hcpName: "",
    interactionDate: "",
    channel: "",
    rawNotes: "",
    summary: "",
    sentiment: "",
    productsDiscussed: [],
    followUpRequired: false,
    followUpDate: "",
    attendees: [],
    samplesDistributed: [],
    outcomes: "",
    followUpActions: "",
    suggestions: [],
    source: null,
};

/**
 * Holds the interaction shown in the read-only
 * Interaction Details form.
 *
 * The form is populated only by AI responses:
 * - log_interaction / edit_interaction → the saved interaction
 * - interaction_history                → the latest interaction
 * - suggest_followup                   → AI suggested follow-ups
 *
 * Failed tool responses leave the form unchanged.
 */
const interactionSlice = createSlice({
    name: "interaction",

    initialState,

    reducers: {
        clearInteraction: () => initialState,
    },

    extraReducers: (builder) => {

        builder.addCase(sendChatMessage.fulfilled, (state, action) => {
            const response = action.payload;

            if (isInteractionOutput(response)) {
                const { interaction, hcp_name } = response.tool_output;
                const sameInteraction = state.interactionId === interaction.id;

                return {
                    ...toInteractionState(
                        interaction,
                        hcp_name,
                        response.tool_name as "log_interaction" | "edit_interaction",
                    ),
                    // Keep suggestions only while the same interaction is shown.
                    suggestions: sameInteraction ? state.suggestions : [],
                };
            }

            if (isHistoryOutput(response)) {
                const { results, hcp_name } = response.tool_output;

                if (results.length === 0) {
                    return state;
                }

                return {
                    ...toInteractionState(
                        results[0],
                        hcp_name,
                        "interaction_history",
                    ),
                    suggestions: [],
                };
            }

            if (isFollowUpOutput(response)) {
                state.suggestions = [
                    response.tool_output.recommendation.recommendation,
                ];
            }

            return state;
        });

    },
});

export const { clearInteraction } = interactionSlice.actions;

export default interactionSlice.reducer;
