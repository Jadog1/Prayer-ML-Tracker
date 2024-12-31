import datetime
from typing import List
from sqlalchemy import create_engine, String, ForeignKey, func, DateTime
from sqlalchemy.orm import relationship, scoped_session, sessionmaker, Mapped, mapped_column, DeclarativeBase, Session
from pgvector.sqlalchemy import Vector

class Base(DeclarativeBase):
    pass

prayerColumnsExceptEmbeddings = [
    "id",
    "account_id",
    "request",
    "created_at",
    "updated_at",
    "contact_id",
    "archived_at",
    "link_id",
    "prayer_type",
    "sentiment_analysis",
    "emotion_roberta"
]
class PrayerRequestORM(Base):
    __tablename__ = 'prayer_request'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)
    request: Mapped[str] = mapped_column(String(), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.current_timestamp())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.current_timestamp())
    archived_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    link_id: Mapped[int] = mapped_column(ForeignKey("link.id"), nullable=True)
    gte_base_embedding: Mapped[Vector] = mapped_column(Vector(768), nullable=True)
    msmarco_base_embedding: Mapped[Vector] = mapped_column(Vector(768), nullable=True)
    prayer_type: Mapped[str] = mapped_column(String(),nullable=True)
    sentiment_analysis: Mapped[str] = mapped_column(String(),nullable=True)
    emotion_roberta: Mapped[str] = mapped_column(String(),nullable=True)
    contact_group_id: Mapped[int] = mapped_column(ForeignKey("contact_prayer_groups.id"), nullable=False)

    # Foreign key relationships
    account: Mapped["AccountORM"] = relationship(back_populates="prayer_requests")
    contact_group: Mapped["ContactGroupORM"] = relationship(back_populates="prayer_requests")
    link: Mapped["LinkORM"] = relationship(back_populates="prayer_requests")
    prayer_topics: Mapped[List["PrayerTopicsORM"]] = relationship(back_populates="prayer_request")

class ContactORM(Base):
    __tablename__ = 'contact'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    description: Mapped[str] = mapped_column(String(), nullable=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.current_timestamp())

    # Relationships
    account: Mapped["AccountORM"] = relationship(back_populates="contacts")
    contact_group: Mapped[List["ContactGroupORM"]] = relationship(back_populates="contact")

class ContactGroupORM(Base):
    __tablename__ = 'contact_prayer_groups'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    contact_id: Mapped[int] = mapped_column(ForeignKey("contact.id"), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("prayer_group.id"), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.current_timestamp())

    # Relationships
    contact: Mapped["ContactORM"] = relationship(back_populates="contact_group")
    group: Mapped["GroupORM"] = relationship(back_populates="contacts")
    prayer_requests: Mapped["PrayerRequestORM"] = relationship(back_populates="contact_group")

class AccountORM(Base):
    __tablename__ = 'account'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)

    # Relationships
    prayer_requests: Mapped[List["PrayerRequestORM"]] = relationship(back_populates="account")
    contacts: Mapped[List["ContactORM"]] = relationship(back_populates="account")
    groups: Mapped[List["GroupORM"]] = relationship(back_populates="account")

class GroupORM(Base):
    __tablename__ = 'prayer_group'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)

    # Relationships
    account: Mapped["AccountORM"] = relationship(back_populates="groups")
    contacts: Mapped[List["ContactGroupORM"]] = relationship(back_populates="group")

class LinkORM(Base):
    __tablename__ = 'link'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Relationships
    prayer_requests: Mapped[List["PrayerRequestORM"]] = relationship(back_populates="link")

class BibleTopicORM(Base):
    __tablename__ = 'bible_topic'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    book: Mapped[str] = mapped_column(String(), nullable=False)
    chapter: Mapped[int] = mapped_column(nullable=False)
    verse_start: Mapped[int] = mapped_column(nullable=False)
    verse_end: Mapped[int] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(String(), nullable=False)
    gte_base_embedding: Mapped[Vector] = mapped_column(Vector(768), nullable=False)

    # Relationships
    bible_topics: Mapped[List["BibleTopicsORM"]] = relationship(back_populates="bible_topic")

class TopicORM(Base):
    __tablename__ = 'topic'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(), nullable=False, unique=True)
    gte_base_embedding: Mapped[Vector] = mapped_column(Vector(768), nullable=False)

    # Relationships
    bible_topics: Mapped[List["BibleTopicsORM"]] = relationship(back_populates="topic")
    prayer_topics: Mapped[List["PrayerTopicsORM"]] = relationship(back_populates="topic")

class BibleTopicsORM(Base):
    __tablename__ = 'bible_topics'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topic.id"), nullable=False)
    bible_topic_id: Mapped[int] = mapped_column(ForeignKey("bible_topic.id"), nullable=False)

    # Relationships
    topic: Mapped["TopicORM"] = relationship(back_populates="bible_topics")
    bible_topic: Mapped["BibleTopicORM"] = relationship(back_populates="bible_topics")

class PrayerTopicsORM(Base):
    __tablename__ = 'prayer_topics'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topic.id"), nullable=False)
    prayer_request_id: Mapped[int] = mapped_column(ForeignKey("prayer_request.id"), nullable=False)
    score: Mapped[float] = mapped_column(nullable=False)

    # Relationships
    topic: Mapped["TopicORM"] = relationship(back_populates="prayer_topics")
    prayer_request: Mapped["PrayerRequestORM"] = relationship(back_populates="prayer_topics")

def OpenPool(pg_uri: str)->scoped_session[Session]:
    engine = create_engine(pg_uri)
    Base.metadata.create_all(engine)

    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)