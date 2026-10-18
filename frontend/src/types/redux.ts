import type { InteractionChannel, Sentiment } from "./interaction";

export interface AppState {
    loading: boolean;
}

/**
 * How an assistant message should be displayed.
 *
 * - ok:      normal reply
 * - notice:  expected problem the user can fix (missing HCP name,
 *            HCP not found, nothing to update)
 * - info:    unsupported request, reply lists capabilities
 * - error:   request failed; can be retried
 */
export type ChatMessageStatus = "ok" | "notice" | "info" | "error";

export interface ChatMessage {
    id: string;
    role: "user" | "assistant";
    content: string;
    status?: ChatMessageStatus;
    /** Original user message, set on failed replies so they can be retried. */
    retryMessage?: string;
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
    attendees: string[];
    samplesDistributed: string[];
    outcomes: string;
    followUpActions: string;
    /** AI follow-up recommendations for the current HCP. */
    suggestions: string[];
    /** Which AI tool last updated the form. */
    source: InteractionSource | null;
}
