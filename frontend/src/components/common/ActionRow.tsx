interface ActionRowProps {
    text: string;
}

export default function ActionRow({
    text,
}: ActionRowProps) {
    return (
        <div className="action-row">

            <span className="action-icon">
                ✨
            </span>

            <span className="action-text">
                {text}
            </span>

        </div>
    );
}