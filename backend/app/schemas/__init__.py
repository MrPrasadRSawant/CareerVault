from app.schemas.application import (
    ApplicationCreate,
    ApplicationRead,
    ApplicationStatusHistoryRead,
    ApplicationStatusUpdate,
    ApplicationUpdate,
)
from app.schemas.ai_actions import AiOpportunityBatchCreate, AiOpportunityCreate, AiOpportunityUpdate
from app.schemas.api_key import ApiKeyCreate, ApiKeyCreated, ApiKeyRead, ApiKeyUpdate
from app.schemas.auth import LoginRequest, Token, TokenWithUser
from app.schemas.common import Message, ORMModel
from app.schemas.cover_letter import CoverLetterCreate, CoverLetterRead, CoverLetterUpdate
from app.schemas.email_follow_up import (
    EmailAgentApplication,
    EmailFollowUpCreate,
    EmailFollowUpGroup,
    EmailFollowUpRead,
    EmailFollowUpUpdate,
)
from app.schemas.follow_up import FollowUpCreate, FollowUpRead, FollowUpUpdate
from app.schemas.interview import InterviewCreate, InterviewRead, InterviewUpdate
from app.schemas.notification import (
    NotificationCountRead,
    NotificationRead,
    NotificationSeenUpdate,
)
from app.schemas.opportunity import (
    OpportunityBulkDelete,
    OpportunityBulkDeleteRead,
    OpportunityCreate,
    OpportunityRead,
    OpportunityUpdate,
)
from app.schemas.resume import ResumeCreate, ResumeRead, ResumeUpdate
from app.schemas.user import UserCreate, UserRead, UserUpdate

__all__ = [
    "ApplicationCreate",
    "ApplicationRead",
    "ApplicationStatusHistoryRead",
    "ApplicationStatusUpdate",
    "ApplicationUpdate",
    "AiOpportunityBatchCreate",
    "AiOpportunityCreate",
    "AiOpportunityUpdate",
    "ApiKeyCreate",
    "ApiKeyCreated",
    "ApiKeyRead",
    "ApiKeyUpdate",
    "CoverLetterCreate",
    "CoverLetterRead",
    "CoverLetterUpdate",
    "EmailAgentApplication",
    "EmailFollowUpCreate",
    "EmailFollowUpGroup",
    "EmailFollowUpRead",
    "EmailFollowUpUpdate",
    "FollowUpCreate",
    "FollowUpRead",
    "FollowUpUpdate",
    "InterviewCreate",
    "InterviewRead",
    "InterviewUpdate",
    "LoginRequest",
    "Message",
    "NotificationCountRead",
    "NotificationRead",
    "NotificationSeenUpdate",
    "OpportunityBulkDelete",
    "OpportunityBulkDeleteRead",
    "OpportunityCreate",
    "OpportunityRead",
    "OpportunityUpdate",
    "ORMModel",
    "ResumeCreate",
    "ResumeRead",
    "ResumeUpdate",
    "Token",
    "TokenWithUser",
    "UserCreate",
    "UserRead",
    "UserUpdate",
]
