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
    return (
        <div className="input-group">
            <label className="input-label">
                {label}
            </label>

            <select
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
            <span className="input-icon">
                <ChevronDown size={16} />
            </span>
        </div>
    );
}
