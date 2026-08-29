from sqlalchemy import Column, Integer, String, Text, ForeignKey
from .database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)


class KeywordIndex(Base):
    __tablename__ = "keyword_index"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=False
    )

    keyword_hash = Column(String(64), nullable=False, index=True)

    frequency = Column(Integer, nullable=False, default=1)