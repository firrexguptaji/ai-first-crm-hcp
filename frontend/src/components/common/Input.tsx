import { useId } from "react";

interface InputProps {
    label: string;
    value?: string;
    placeholder?: string;
    type?: string;
    icon?: React.ReactNode;
}

export default function Input({
    label,
    value = "",
    placeholder,
    type = "text",
    icon,
}: InputProps) {
    const id = useId();

    return (
        <div className="input-group">

            <label className="input-label" htmlFor={id}>
                {label}
            </label>

            <div className="input-wrapper">

                <input
                    id={id}
                    type={type}
                    value={value}
                    placeholder={placeholder}
                    readOnly
                    aria-readonly="true"
                    className="crm-input"
                />

                {icon && (
                    <span className="input-icon" aria-hidden="true">
                        {icon}
                    </span>
                )}

            </div>

        </div>
    );
}