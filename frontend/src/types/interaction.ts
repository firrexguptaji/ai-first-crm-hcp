/**
 * Interaction types.
 *
 * Mirrors backend/app/schemas/interaction.py and
 * backend/app/models/enums.py
 */

export type InteractionChannel =
    | "IN_PERSON"
    | "PHONE"
    | "EMAIL"
    | "VIDEO"
    | "OTHER";

export type Sentiment =
    | "POSITIVE"
    | "NEUTRAL"
    | "NEGATIVE";

/**
 * Interaction as returned by the AI tools
 * (backend/app/graph/tools/serializers.py).
 */
export interface InteractionRecord {
    id: string;
    hcp_id: string;
    interaction_date: string;
    channel: InteractionChannel;
    raw_notes: string;
    summary: string;
    sentiment: Sentiment;
    products_discussed: string[];
    follow_up_required: boolean;
    follow_up_date: string | null;
}

/**
 * Interaction as returned by the REST API.
 */
export interface Interaction
    extends Omit<InteractionRecord, "products_discussed"> {
    products_discussed: string[] | null;
    created_at: string;
    updated_at: string;
}

export interface CreateInteraction {
    hcp_id: string;
    interaction_date: string;
    channel: InteractionChannel;
    raw_notes: string;
    summary: string;
    sentiment: Sentiment;
    products_discussed?: string[] | null;
    follow_up_required?: boolean;
    follow_up_date?: string | null;
}

export type UpdateInteraction =
    Partial<Omit<CreateInteraction, "hcp_id">>;
