interface ActionRowProps {
    text: string;
    /** Shown as a small badge; marks the action as not available yet. */
    badge?: string;
}

export default function ActionRow({
    text,
    badge,
}: ActionRowProps) {
    return (
        <div
            className="action-row"
            aria-disabled={badge ? "true" : undefined}
            title={badge ? `${text}: ${badge}` : undefined}
        >

            <span className="action-icon" aria-hidden="true">
                ✨
            </span>

            <span className="action-text">
                {text}
            </span>

            {badge && (
                <span className="action-badge">
                    {badge}
                </span>
            )}

        </div>
    );
}