import { useId } from 'react';
import { ChevronDown } from 'lucide-react';

interface DropdownProps {
    label: string;
    value: string;
    options: string[];
    placeholder?: string;
}

export default function Dropdown({
    label,
    value,
    options,
    placeholder = "Select...",
}: DropdownProps) {
    const id = useId();

    return (
        <div className="input-group">
            <label className="input-label" htmlFor={id}>
                {label}
            </label>

            <select
                id={id}
                className="crm-input"
                value={value}
                disabled
            >
                {!value && (
                    <option value="">
                        {placeholder}
                    </option>
                )}

                {options.map((option) => (
                    <option
                        key={option}
                        value={option}
                    >
                        {option}
                    </option>
                ))}
            </select>
            <span className="input-icon" aria-hidden="true">
                <ChevronDown size={16} />
            </span>
        </div>
    );
}
