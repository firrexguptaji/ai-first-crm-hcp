interface TextAreaProps {
    label: string;
    value?: string;
    placeholder?: string;
    rows?: number;
}

export default function TextArea({
    label,
    value = "",
    placeholder,
    rows = 3,
}: TextAreaProps) {
    return (
        <div className="textarea-group">

            <label className="input-label">
                {label}
            </label>

            <textarea
                className="crm-textarea"
                value={value}
                placeholder={placeholder}
                rows={rows}
                readOnly
            />

        </div>
    );
}