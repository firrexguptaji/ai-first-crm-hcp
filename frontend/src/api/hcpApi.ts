import apiClient from "./client";

import type {
    HealthcareProfessional,
    CreateHealthcareProfessional,
} from "../types/hcp";

export async function getHCPs(): Promise<HealthcareProfessional[]> {

    const response =
        await apiClient.get<HealthcareProfessional[]>("/hcps");

    return response.data;
}

export async function getHCP(
    id: string,
): Promise<HealthcareProfessional> {

    const response =
        await apiClient.get<HealthcareProfessional>(
            `/hcps/${id}`,
        );

    return response.data;
}

export async function createHCP(
    data: CreateHealthcareProfessional,
): Promise<HealthcareProfessional> {

    const response =
        await apiClient.post<HealthcareProfessional>(
            "/hcps",
            data,
        );

    return response.data;
}