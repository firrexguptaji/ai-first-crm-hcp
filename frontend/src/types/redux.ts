export interface AppState {
    loading: boolean;
}

export interface ChatMessage {
    id: string;
    role: "user" | "assistant";
    content: string;
}

export interface ChatState {
    messages: ChatMessage[];
    loading: boolean;
    error: string | null;
}

export interface InteractionState {
    hcpName: string;
    interactionDate: string;
    channel: string;
    rawNotes: string;
    summary: string;
    sentiment: string;
    productsDiscussed: string[];
    followUpRequired: boolean;
    followUpDate: string;
}