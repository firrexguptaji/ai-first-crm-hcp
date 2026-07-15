import apiClient from "./client";

import type {
    Interaction,
    CreateInteraction,
} from "../types/interaction";

export async function getInteractions(): Promise<Interaction[]> {

    const response =
        await apiClient.get<Interaction[]>(
            "/interactions",
        );

    return response.data;
}

export async function createInteraction(
    data: CreateInteraction,
): Promise<Interaction> {

    const response =
        await apiClient.post<Interaction>(
            "/interactions",
            data,
        );

    return response.data;
}

export async function updateInteraction(
    id: string,
    data: Partial<CreateInteraction>,
): Promise<Interaction> {

    const response =
        await apiClient.put<Interaction>(
            `/interactions/${id}`,
            data,
        );

    return response.data;
}