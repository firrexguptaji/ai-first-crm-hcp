export interface HealthcareProfessional {
    id: string;
    first_name: string;
    last_name: string;
    specialty: string;
    organization: string;
    email: string;
}

export interface CreateHealthcareProfessional {
    first_name: string;
    last_name: string;
    specialty: string;
    organization: string;
    email: string;
}