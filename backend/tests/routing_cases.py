"""
Routing evaluation set.

Realistic messages and the tool that should handle each one.
Used by:
- tests/test_routing_eval.py (live LLM evaluation, opt-in)
- the keyword baseline report in the same file

Add a case whenever a message is routed incorrectly in testing.
"""

ROUTING_CASES: list[tuple[str, str]] = [
    # ---------------- Log Interaction ----------------
    ("Met Dr. Smith yesterday.", "log_interaction"),
    ("Called Dr. Smith this morning about Product B", "log_interaction"),
    ("Had lunch with Alice Brown, talked about Product A", "log_interaction"),
    ("Emailed Dr. Smith the brochure", "log_interaction"),
    ("Video call with Alice Brown, she was happy", "log_interaction"),
    ("Dr. Smith rang me about side effects", "log_interaction"),
    ("Saw Alice Brown at the conference, she asked about pricing", "log_interaction"),
    ("Today I visited Dr. Smith and we reviewed the trial data", "log_interaction"),
    ("Alice Brown wants to change her prescribing to Product A, met her today", "log_interaction"),
    ("Met Alice Brown, she asked me to update her on trial results", "log_interaction"),
    ("Quick catch-up with Alice Brown today", "log_interaction"),
    ("Met Alice Brown today. Schedule a follow-up next week.", "log_interaction"),
    ("Dr. Smith asked about metformin dosing", "log_interaction"),
    ("Met Alice Brown, she wants to add Product B to her formulary", "log_interaction"),

    # ---------------- Edit Interaction ----------------
    ("Update my meeting with Dr. Smith, sentiment was positive", "edit_interaction"),
    ("Change the sentiment of my last meeting with Alice Brown to negative", "edit_interaction"),
    ("The meeting with Alice Brown was actually a phone call", "edit_interaction"),
    ("Correct the date of my last visit with Alice Brown to yesterday", "edit_interaction"),
    ("Mark follow-up as not required for Alice Brown", "edit_interaction"),
    ("Alice Brown's sentiment should be neutral", "edit_interaction"),
    ("Also note that Nurse Kelly attended my meeting with Alice Brown", "edit_interaction"),
    ("Add Dr. Patel as an attendee to my meeting with Alice Brown", "edit_interaction"),
    ("Remove Nurse Kelly from the attendees for Alice Brown", "edit_interaction"),
    ("Delete Product A from the products in my last meeting with Alice Brown", "edit_interaction"),
    ("Append 'send brochure' to follow-up actions for Alice Brown", "edit_interaction"),
    ("Edit the outcome for Alice Brown", "edit_interaction"),
    ("Actually she was negative, not positive", "edit_interaction"),

    # ---------------- Interaction History ----------------
    ("Show interaction history for Dr. Alice Brown", "interaction_history"),
    ("What did I discuss with Alice Brown last time?", "interaction_history"),
    ("When did I last meet Alice Brown?", "interaction_history"),
    ("Show my interactions with Alice Brown", "interaction_history"),
    ("List all meetings with Alice Brown", "interaction_history"),
    ("Give me a summary of my visits to Alice Brown", "interaction_history"),

    # ---------------- Search HCP ----------------
    ("Find Alice Brown", "search_hcp"),
    ("Who is Alice Brown?", "search_hcp"),
    ("Find cardiologists in City Hospital", "search_hcp"),
    ("Show me all doctors", "search_hcp"),
    ("Do we have an oncologist named Smith?", "search_hcp"),

    # ---------------- Suggest Follow-up ----------------
    ("Suggest a follow-up for Alice Brown", "suggest_followup"),
    ("What should I do next with Alice Brown?", "suggest_followup"),
    ("Recommend a next step for Alice Brown", "suggest_followup"),
    ("How should I follow up with Alice Brown?", "suggest_followup"),
    ("Any advice for my next visit to Alice Brown?", "suggest_followup"),

    # ---------------- Unsupported ----------------
    ("Hi", "unsupported"),
    ("What can you do?", "unsupported"),
    ("Delete my last interaction with Alice Brown", "unsupported"),
    ("What's the weather today?", "unsupported"),
]
