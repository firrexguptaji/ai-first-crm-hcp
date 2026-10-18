import axios from "axios";

/**
 * Convert a failed API request into a message for the user.
 *
 * Errors returned by the AI tools arrive as normal responses
 * (HTTP 200 with success: false). This handles requests that
 * failed before a response was received, or with an HTTP error.
 */
export function getErrorMessage(error: unknown): string {

    if (axios.isAxiosError(error)) {

        if (error.code === "ECONNABORTED" || error.code === "ETIMEDOUT") {
            return "The AI is taking too long to respond. Please try again.";
        }

        if (!error.response) {
            return "Can't reach the server. Check that the backend is running, then try again.";
        }

        const status = error.response.status;

        if (status >= 500) {
            return "The server ran into a problem. Please try again in a moment.";
        }

        if (status === 422) {
            return "The request was not valid. Please rephrase your message.";
        }

        return `Request failed (HTTP ${status}). Please try again.`;
    }

    if (error instanceof Error && error.message) {
        return error.message;
    }

    return "Something went wrong. Please try again.";
}
