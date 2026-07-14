import {
    Search,
    Plus,
} from "lucide-react";

interface InfoCardProps {
    title: string;
    emptyText: string;
    buttonText: string;
}

export default function InfoCard({
    title,
    emptyText,
    buttonText,
}: InfoCardProps) {
    return (

        <div className="info-card">

            <div className="info-header">

                <span>{title}</span>

                <button
                    type="button"
                    className="card-button"
>

                    {buttonText === "Search/Add" ? (
                        <Search size={14} />
                        ) : (
                        <Plus size={14} />
                    )}

                    <span>{buttonText}</span>

                </button>

            </div>

            <p className="empty-text">
                {emptyText}
            </p>

        </div>

    );
}