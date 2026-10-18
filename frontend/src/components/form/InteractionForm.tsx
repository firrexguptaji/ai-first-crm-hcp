import "./InteractionForm.css";
import Input from "../common/Input";
import TextArea from "../common/TextArea";
import ActionRow from "../common/ActionRow";
import InfoCard from "../common/InfoCard";
import RadioGroup from "../common/RadioGroup";
import SuggestionList from "../common/SuggestionList";
import Dropdown from "../common/Dropdown";
import {
    Calendar,
    Clock,
    Search,
    Mic,
} from "lucide-react";

import TextAreaWithAction from "../common/TextAreaWithAction";

import { useAppSelector } from "../../app/hooks";
import {
    CHANNEL_OPTIONS,
    SENTIMENT_OPTIONS,
    channelLabel,
    formatDate,
    formatFollowUp,
    formatList,
    formatTime,
    sentimentLabel,
} from "../../features/interaction/formatters";

import type { InteractionSource } from "../../types/redux";

const SOURCE_LABELS: Record<InteractionSource, string> = {
    log_interaction: "Logged by AI",
    edit_interaction: "Updated by AI",
    interaction_history: "Latest from history",
};

/**
 * Read-only Interaction Details form.
 *
 * All values come from the interaction slice, which is
 * populated by AI chat responses (see interactionSlice.ts).
 */
export default function InteractionForm() {
    const interaction = useAppSelector(
        (state) => state.interaction
    );

    return (
        <div className="interaction-form">
            
            <h2 className="interaction-section-title">
                Interaction Details

                {interaction.source && (
                    <span className="interaction-source">
                        {SOURCE_LABELS[interaction.source]}
                    </span>
                )}
            </h2>

            <div className="interaction-grid">

                <Input 
                    label="HCP Name" 
                    value={interaction.hcpName}
                    placeholder="Search or select HCP..."
                    icon={<Search size={16} />}
                />

                <Dropdown
                     label="Interaction Type"
                    value={channelLabel(interaction.channel)}
                    options={CHANNEL_OPTIONS}
                />

                <Input
                    label="Date"
                    value={formatDate(interaction.interactionDate)}
                    placeholder="DD-MM-YYYY"
                    icon={<Calendar size={16} />}
                />

                <Input
                    label="Time"
                    value={formatTime(interaction.interactionDate)}
                    placeholder="HH:MM"
                    icon={<Clock size={16} />}
                />

                <div className="full-width">
                        <TextArea
                        label="Attendees"
                        rows={1}
                        value={formatList(interaction.attendees)}
                        placeholder="Enter names or search..."
                    />
                </div>

                <div className="full-width">

                    <TextAreaWithAction
                        label="Topics Discussed"
                        rows={3}
                        value={interaction.summary}
                        placeholder="Enter key discussion points..."
                        actionIcon={<Mic size={16} />}
                    />

                </div>

                <div className="full-width">

                    <ActionRow
                        text="Summarize from Voice Note (Requires Consent)"
                    />

                </div>

                <div className="full-width">

                    <label className="input-label">

                        Materials Shared / Samples Distributed

                    </label>

                    <InfoCard
                        title="Materials Shared"
                        emptyText="No materials added."
                        items={interaction.productsDiscussed}
                        buttonText="Search/Add"
                    />

                </div>

                <div className="full-width">

                    <InfoCard
                        title="Samples Distributed"
                        emptyText="No samples added."
                        items={interaction.samplesDistributed}
                        buttonText="Add Sample"
                    />

                </div>

                <div className="full-width">

                    <RadioGroup
                        label="Observed / Inferred HCP Sentiment"
                        options={SENTIMENT_OPTIONS}
                        selected={sentimentLabel(interaction.sentiment)}
                    />

                </div>

                <div className="full-width">
                    <TextArea
                        label="Outcomes"
                        rows={2}
                        value={interaction.outcomes}
                        placeholder="Key outcomes or agreements..."
                    />
                </div>

                <div className="full-width">
                    <TextArea
                        label="Follow-up Actions"
                        rows={2}
                        value={formatFollowUp(
                            interaction.followUpRequired,
                            interaction.followUpDate,
                            interaction.followUpActions,
                        )}
                        placeholder="Enter next steps or tasks..."
                    />
                </div>

                <div className="full-width">

                    <SuggestionList
                        suggestions={interaction.suggestions}
                        emptyText='Ask the AI, e.g. "Suggest a follow-up for Alice Brown".'
                    />

                </div>

            </div>

        </div>
    );
}   

