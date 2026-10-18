import type {
    InteractionChannel,
    Sentiment,
} from "../../types/interaction";

/**
 * Display labels for backend enum values.
 */
export const CHANNEL_LABELS: Record<InteractionChannel, string> = {
    IN_PERSON: "In Person",
    PHONE: "Phone",
    EMAIL: "Email",
    VIDEO: "Video",
    OTHER: "Other",
};

export const SENTIMENT_LABELS: Record<Sentiment, string> = {
    POSITIVE: "Positive",
    NEUTRAL: "Neutral",
    NEGATIVE: "Negative",
};

export const CHANNEL_OPTIONS = Object.values(CHANNEL_LABELS);

export const SENTIMENT_OPTIONS = Object.values(SENTIMENT_LABELS);

export function channelLabel(channel: InteractionChannel | ""): string {
    return channel ? CHANNEL_LABELS[channel] : "";
}

export function sentimentLabel(sentiment: Sentiment | ""): string {
    return sentiment ? SENTIMENT_LABELS[sentiment] : "";
}

/*
 * Dates are read from the ISO string directly (not through
 * `new Date`) so the browser time zone cannot shift the day.
 */

/** "2026-10-18T10:30:00" or "2026-10-18" → "18-10-2026" */
export function formatDate(iso: string): string {
    const match = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso);

    if (!match) {
        return "";
    }

    const [, year, month, day] = match;

    return `${day}-${month}-${year}`;
}

/** "2026-10-18T10:30:00" → "10:30" */
export function formatTime(iso: string): string {
    const match = /T(\d{2}):(\d{2})/.exec(iso);

    return match ? `${match[1]}:${match[2]}` : "";
}

export function formatFollowUp(
    required: boolean,
    date: string,
): string {
    if (date) {
        return `Follow up on ${formatDate(date)}`;
    }

    return required ? "Follow-up required (no date set)" : "";
}
