import { Inbox } from "lucide-react";

interface EmptyStateProps {
    title?: string;
    description?: string;
}

export default function EmptyState({
    title = "No Data Available",
    description = "There is currently nothing to display.",
}: EmptyStateProps) {
    return (
        <div className="empty-state">

            <Inbox
                size={48}
                className="empty-state-icon"
            />

            <h3 className="empty-state-title">
                {title}
            </h3>

            <p className="empty-state-description">
                {description}
            </p>

        </div>
    );
}