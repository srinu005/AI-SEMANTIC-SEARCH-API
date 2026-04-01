from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from datetime import datetime

class DocumentMetadata(Base):
    __tablename__ = "document_metadata"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[str] = mapped_column(index=True)
    content_hash: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)