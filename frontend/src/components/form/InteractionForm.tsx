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

export default function InteractionForm() {
    return (
        <div className="interaction-form">
            
            <h2 className="interaction-section-title">
                Interaction Details
            </h2>

            <div className="interaction-grid">

                <Input 
                    label="HCP Name" 
                    placeholder="Search or select HCP..."
                    icon={<Search size={16} />}
                />

                <Dropdown
                     label="Interaction Type"
                    value="Meeting"
                    options={[
                        "Meeting",
                        "Call",
                        "Email",
                        "Conference",
                    ]}
                />

                <Input
                    label="Date"
                    value="19-04-2025"
                    icon={<Calendar size={16} />}
                />

                <Input
                    label="Time"
                    value="19:36"
                    icon={<Clock size={16} />}
                />

                <div className="full-width">
                        <TextArea
                        label="Attendees"
                        rows={1}
                        placeholder="Enter names or search..."
                    />
                </div>

                <div className="full-width">

                    <TextAreaWithAction
                        label="Topics Discussed"
                        rows={3}
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
                        buttonText="Search/Add"
                    />

                </div>

                <div className="full-width">

                    <InfoCard
                        title="Samples Distributed"
                        emptyText="No samples added."
                        buttonText="Add Sample"
                    />

                </div>

                <div className="full-width">

                    <RadioGroup
                        label="Observed / Inferred HCP Sentiment"
                        options={[
                                "Positive",
                                "Neutral",
                                "Negative",
                            ]}
                        selected="Neutral"
                    />

                </div>

                <div className="full-width">
                    <TextArea
                        label="Outcomes"
                        rows={2}
                        placeholder="Key outcomes or agreements..."
                    />
                </div>

                <div className="full-width">
                    <TextArea
                        label="Follow-up Actions"
                        rows={2}
                        placeholder="Enter next steps or tasks..."
                    />
                </div>

                <div className="full-width">

                    <SuggestionList
                        suggestions={[
                            "Schedule follow-up meeting",
                            "Share Product A clinical trial",
                            "Invite to educational webinar",
                    ]}
                />

                </div>

            </div>

        </div>
    );
}   

