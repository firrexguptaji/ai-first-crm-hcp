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
    return (
        <div className="input-group">

            <label className="input-label">
                {label}
            </label>

            <div className="input-wrapper">

                <input
                    type={type}
                    value={value}
                    placeholder={placeholder}
                    readOnly
                    className="crm-input"
                />

                {icon && (
                    <span className="input-icon">
                        {icon}
                    </span>
                )}

            </div>

        </div>
    );
}