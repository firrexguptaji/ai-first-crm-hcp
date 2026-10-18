import { useId, type ReactNode } from "react";

interface TextAreaWithActionProps {
    label: string;
    placeholder?: string;
    rows?: number;
    value?: string;
    actionIcon?: ReactNode;
    /** Accessible name for the icon-only action button. */
    actionLabel?: string;
}

export default function TextAreaWithAction({
    label,
    placeholder,
    rows = 3,
    value = "",
    actionIcon,
    actionLabel = "Voice input (not available)",
}: TextAreaWithActionProps) {
    const id = useId();

    return (
        <div className="textarea-group">

            <label className="input-label" htmlFor={id}>
                {label}
            </label>

            <div className="textarea-wrapper">

                <textarea
                    id={id}
                    className="crm-textarea"
                    rows={rows}
                    value={value}
                    placeholder={placeholder}
                    readOnly
                    aria-readonly="true"
                />

                {actionIcon && (
                    <button
                        type="button"
                        className="textarea-action"
                        disabled
                        aria-label={actionLabel}
                        title={actionLabel}
                    >
                        {actionIcon}
                    </button>
                )}

            </div>

        </div>
    );
}