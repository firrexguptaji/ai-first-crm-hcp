import type { ReactNode } from "react";

interface TextAreaWithActionProps {
    label: string;
    placeholder?: string;
    rows?: number;
    value?: string;
    actionIcon?: ReactNode;
}

export default function TextAreaWithAction({
    label,
    placeholder,
    rows = 3,
    value = "",
    actionIcon,
}: TextAreaWithActionProps) {
    return (
        <div className="textarea-group">

            <label className="input-label">
                {label}
            </label>

            <div className="textarea-wrapper">

                <textarea
                    className="crm-textarea"
                    rows={rows}
                    value={value}
                    placeholder={placeholder}
                    readOnly
                />

                {actionIcon && (
                    <button
                        type="button"
                        className="textarea-action"
                        disabled
                    >
                        {actionIcon}
                    </button>
                )}

            </div>

        </div>
    );
}