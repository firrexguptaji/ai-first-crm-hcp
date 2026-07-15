interface LoadingProps {
    text?: string;
}

export default function Loading({
    text = "Loading...",
}: LoadingProps) {
    return (
        <div className="loading-container">

            <div className="loading-spinner" />

            <p className="loading-text">
                {text}
            </p>

        </div>
    );
}