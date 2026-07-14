interface RadioGroupProps {
    label: string;
    options: string[];
    selected?: string;
}

export default function RadioGroup({
    label,
    options,
    selected,
}: RadioGroupProps) {
    return (
        <div className="radio-group">

            <label className="input-label">
                {label}
            </label>

            <div className="radio-options">

                {options.map((option) => (
                    <label
                        key={option}
                        className="radio-option"
                    >
                        <input
                            type="radio"
                            checked={selected === option}
                            readOnly
                        />

                        <span>{option}</span>

                    </label>
                ))}

            </div>

        </div>
    );
}