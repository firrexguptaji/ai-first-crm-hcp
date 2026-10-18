import type { InteractionRecord } from "../../types/interaction";
import type {
    InteractionSource,
    InteractionState,
} from "../../types/redux";

/**
 * Convert an interaction returned by an AI tool into
 * Redux interaction state.
 */
export function toInteractionState(
    record: InteractionRecord,
    hcpName: string,
    source: InteractionSource,
): Omit<InteractionState, "suggestions"> {
    return {
        interactionId: record.id,
        hcpName,
        interactionDate: record.interaction_date,
        channel: record.channel,
        rawNotes: record.raw_notes,
        summary: record.summary,
        sentiment: record.sentiment,
        productsDiscussed: record.products_discussed ?? [],
        followUpRequired: record.follow_up_required,
        followUpDate: record.follow_up_date ?? "",
        source,
    };
}
