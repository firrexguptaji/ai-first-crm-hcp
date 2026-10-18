/**
 * Healthcare Professional types.
 *
 * Mirrors backend/app/schemas/healthcare_professional.py
 */

export interface HealthcareProfessional {
    id: string;
    first_name: string;
    last_name: string;
    specialization: string;
    organization: string;
    email: string | null;
    phone: string | null;
    created_at: string;
    updated_at: string;
}

export interface CreateHealthcareProfessional {
    first_name: string;
    last_name: string;
    specialization: string;
    organization: string;
    email?: string | null;
    phone?: string | null;
}

export type UpdateHealthcareProfessional =
    Partial<CreateHealthcareProfessional>;

/**
 * HCP summary returned by the search_hcp AI tool.
 */
export interface HCPSearchResult {
    id: string;
    first_name: string;
    last_name: string;
    specialization: string;
    organization: string;
}
