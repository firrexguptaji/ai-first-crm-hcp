import { useId } from "react";

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
    const id = useId();

    return (
        <div
            className="radio-group"
            role="radiogroup"
            aria-labelledby={id}
            aria-readonly="true"
        >

            <span className="input-label" id={id}>
                {label}
            </span>

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
                            tabIndex={-1}
                        />

                        <span>{option}</span>

                    </label>
                ))}

            </div>

        </div>
    );
}