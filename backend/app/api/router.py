from fastapi import APIRouter

from app.api import ai_actions, api_keys, applications, auth, cover_letters, email_agent, email_follow_ups, follow_ups, interviews, opportunities, resumes

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(api_keys.router)
api_router.include_router(ai_actions.router)
api_router.include_router(email_agent.router)
api_router.include_router(opportunities.router)
api_router.include_router(applications.router)
api_router.include_router(resumes.router)
api_router.include_router(cover_letters.router)
api_router.include_router(interviews.router)
api_router.include_router(follow_ups.router)
api_router.include_router(email_follow_ups.router)
