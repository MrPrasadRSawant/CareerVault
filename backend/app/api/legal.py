from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.system_setting import TermsOfServiceRead
from app.services.system_setting_service import SystemSettingService

router = APIRouter(prefix="/legal", tags=["legal"])


@router.get("/terms-of-service", response_model=TermsOfServiceRead)
def terms_of_service(db: Session = Depends(get_db)) -> TermsOfServiceRead:
    return SystemSettingService(db).terms_of_service()
