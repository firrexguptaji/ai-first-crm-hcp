export interface ChatRequest {
    message: string;
}

export interface ChatResponse {
    response: string;
    tool_name: string;
    tool_output: unknown;
}