import {
    Search,
    Plus,
} from "lucide-react";

import Button from "./Button";

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

                <Button
                    type="button"
                    variant="secondary"
                    disabled
>

                    {buttonText === "Search/Add" ? (
                        <Search size={14}/>
                        ) : (
                        <Plus size={14}/>
                    )}

                    {buttonText}

                </Button>

            </div>

            <p className="empty-text">
                {emptyText}
            </p>

        </div>

    );
}