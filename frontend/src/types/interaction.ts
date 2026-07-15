export interface Interaction {
    id: string;
    hcp_id: string;
    interaction_type: string;
    summary: string;
    interaction_date: string;
}

export interface CreateInteraction {
    hcp_id: string;
    interaction_type: string;
    summary: string;
}