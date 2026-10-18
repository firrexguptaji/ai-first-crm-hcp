import axios from "axios";

const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    // AI requests can take several LLM calls (e.g. suggest_followup
    // makes two), so allow more time than a plain REST call.
    timeout: 60000,
    headers: {
        "Content-Type": "application/json",
    },
});

export default apiClient;