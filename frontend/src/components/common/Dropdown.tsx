import { ChevronDown } from 'lucide-react';

interface DropdownProps {
    label: string;
    value: string;
    options: string[];
}

export default function Dropdown({
    label,
    value,
    options,
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