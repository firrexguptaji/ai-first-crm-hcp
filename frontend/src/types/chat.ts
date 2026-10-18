/**
 * AI Chat API types.
 *
 * Mirrors backend/app/schemas/chat.py and the
 * tool_output returned by each LangGraph tool.
 */

import type { HCPSearchResult } from "./hcp";
import type { InteractionRecord } from "./interaction";

export interface ChatRequest {
    message: string;
}

export type ToolName =
    | "log_interaction"
    | "edit_interaction"
    | "search_hcp"
    | "interaction_history"
    | "suggest_followup"
    | "unsupported";

/* ---------- Tool outputs ---------- */

export interface ToolErrorOutput {
    success: false;
    error_type?: "validation" | "internal" | "unsupported";
    error?: string;
    reason?: string;
}

/** log_interaction and edit_interaction */
export interface InteractionToolOutput {
    success: true;
    interaction_id: string;
    hcp_name: string;
    interaction: InteractionRecord;
}

/** interaction_history */
export interface HistoryToolOutput {
    success: true;
    count: number;
    hcp_name: string;
    results: InteractionRecord[];
}

/** search_hcp */
export interface SearchToolOutput {
    success: true;
    count: number;
    results: HCPSearchResult[];
}

/** suggest_followup */
export interface FollowUpToolOutput {
    success: true;
    recommendation: {
        recommendation: string;
        rationale: string;
    };
}

export type ToolOutput =
    | ToolErrorOutput
    | InteractionToolOutput
    | HistoryToolOutput
    | SearchToolOutput
    | FollowUpToolOutput;

/* ---------- Response ---------- */

export interface ChatResponse {
    response: string;
    /** Empty string when the workflow failed before routing. */
    tool_name: ToolName | "";
    tool_output: ToolOutput;
}

/* ---------- Type guards ---------- */

export function isToolError(
    output: ToolOutput,
): output is ToolErrorOutput {
    return output.success === false;
}

export function isInteractionOutput(
    response: ChatResponse,
): response is ChatResponse & { tool_output: InteractionToolOutput } {
    return (
        (response.tool_name === "log_interaction"
            || response.tool_name === "edit_interaction")
        && response.tool_output.success
        && "interaction" in response.tool_output
    );
}

export function isHistoryOutput(
    response: ChatResponse,
): response is ChatResponse & { tool_output: HistoryToolOutput } {
    return (
        response.tool_name === "interaction_history"
        && response.tool_output.success
        && "results" in response.tool_output
    );
}

export function isFollowUpOutput(
    response: ChatResponse,
): response is ChatResponse & { tool_output: FollowUpToolOutput } {
    return (
        response.tool_name === "suggest_followup"
        && response.tool_output.success
        && "recommendation" in response.tool_output
    );
}
