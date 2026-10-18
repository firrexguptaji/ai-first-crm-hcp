import { useId } from "react";

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
    const id = useId();

    return (
        <div className="textarea-group">

            <label className="input-label" htmlFor={id}>
                {label}
            </label>

            <textarea
                id={id}
                className="crm-textarea"
                value={value}
                placeholder={placeholder}
                rows={rows}
                readOnly
                aria-readonly="true"
            />

        </div>
    );
}