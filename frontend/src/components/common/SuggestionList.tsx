interface SuggestionListProps {
    suggestions: string[];
}

export default function SuggestionList({
    suggestions,
}: SuggestionListProps) {
    return (

        <div className="suggestion-list">

            <label className="input-label">
                AI Suggested Follow-ups
            </label>

            <ul>

                {suggestions.map((item) => (

                    <li key={item}>
                        {item}
                    </li>

                ))}

            </ul>

        </div>

    );
}