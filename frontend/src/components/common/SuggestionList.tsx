interface SuggestionListProps {
    suggestions: string[];
    emptyText?: string;
}

export default function SuggestionList({
    suggestions,
    emptyText = "No suggestions yet.",
}: SuggestionListProps) {
    return (

        <div className="suggestion-list">

            <label className="input-label">
                AI Suggested Follow-ups
            </label>

            {suggestions.length > 0 ? (

                <ul>

                    {suggestions.map((item) => (

                        <li key={item}>
                            {item}
                        </li>

                    ))}

                </ul>

            ) : (

                <p className="empty-text">
                    {emptyText}
                </p>

            )}

        </div>

    );
}
