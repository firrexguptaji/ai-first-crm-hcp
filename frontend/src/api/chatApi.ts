import apiClient from "./client";

import type {
    ChatRequest,
    ChatResponse,
} from "../types/chat";

export async function sendMessage(
    data: ChatRequest,
): Promise<ChatResponse> {

    try {

        const response =
            await apiClient.post<ChatResponse>(
                "/chat",
                data,
            );

        return response.data;

    } catch (error) {

        console.error(
            "Failed to send chat message:",
            error,
        );

        throw error;

    }

}