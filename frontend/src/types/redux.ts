import type { InteractionChannel, Sentiment } from "./interaction";

export interface AppState {
    loading: boolean;
}

export interface ChatMessage {
    id: string;
    role: "user" | "assistant";
    content: string;
}

export interface ChatState {
    messages: ChatMessage[];
    loading: boolean;
    error: string | null;
}

export type InteractionSource =
    | "log_interaction"
    | "edit_interaction"
    | "interaction_history";

export interface InteractionState {
    /** Null until the AI has logged, edited or retrieved an interaction. */
    interactionId: string | null;
    hcpName: string;
    /** ISO datetime, e.g. 2026-10-18T10:30:00 */
    interactionDate: string;
    channel: InteractionChannel | "";
    rawNotes: string;
    summary: string;
    sentiment: Sentiment | "";
    productsDiscussed: string[];
    followUpRequired: boolean;
    /** ISO date, e.g. 2026-10-25 */
    followUpDate: string;
    /** AI follow-up recommendations for the current HCP. */
    suggestions: string[];
    /** Which AI tool last updated the form. */
    source: InteractionSource | null;
}
