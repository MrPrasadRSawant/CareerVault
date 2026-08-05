import enum


class OpportunityStatus(str, enum.Enum):
    DRAFT = "draft"
    SAVED = "saved"
    APPLIED = "applied"
    # Retained for records created before the candidate-focused lifecycle.
    INTERVIEWING = "interviewing"
    OFFERED = "offered"
    FOLLOW_UP = "follow_up"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEW_COMPLETED = "interview_completed"
    OFFER = "offer"
    REJECTED = "rejected"
    NOT_REPLIED = "not_replied"
    ON_HOLD = "on_hold"
    ARCHIVED = "archived"


class ApplicationStatus(str, enum.Enum):
    APPLIED = "applied"
    SCREENING = "screening"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEW_COMPLETED = "interview_completed"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class InterviewType(str, enum.Enum):
    PHONE = "phone"
    VIDEO = "video"
    TECHNICAL = "technical"
    PANEL = "panel"
    ONSITE = "onsite"
    OTHER = "other"


class InterviewStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class FollowUpStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    DONE = "done"
    SKIPPED = "skipped"
