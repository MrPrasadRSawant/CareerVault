import enum


class UserRole(str, enum.Enum):
    JOB_APPLICANT = "job_applicant"
    SYSTEM_ADMIN = "system_admin"


class AuthEventType(str, enum.Enum):
    LOGIN = "login"
    REGISTRATION = "registration"


class AuthOutcome(str, enum.Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class AuthFailureReason(str, enum.Enum):
    INVALID_CREDENTIALS = "invalid_credentials"
    ACCOUNT_BLOCKED = "account_blocked"
    TEMPORARILY_LOCKED = "temporarily_locked"
    ROLE_NOT_ALLOWED = "role_not_allowed"


class AuthSessionEndReason(str, enum.Enum):
    LOGOUT = "logout"
    ACCOUNT_BLOCKED = "account_blocked"


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
    NOT_SATISFYING_EXPECTATIONS = "not_satisfying_expectations"


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


class EmailFollowUpOutcome(str, enum.Enum):
    PENDING = "pending"
    WON = "won"
    LOST = "lost"


class NotificationType(str, enum.Enum):
    OPPORTUNITY = "opportunity"
    EMAIL_FOLLOW_UP = "email_follow_up"
