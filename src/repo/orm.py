import datetime
from typing import List
from sqlalchemy import create_engine, String, ForeignKey, func, DateTime
from sqlalchemy.orm import relationship, scoped_session, sessionmaker, Mapped, mapped_column, DeclarativeBase, Session
from pgvector.sqlalchemy import Vector

class Base(DeclarativeBase):
    pass

class PrayerRequestORM(Base):
    __tablename__ = 'prayer_request'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)
    request: Mapped[str] = mapped_column(String(collation='pg_catalog."default"'), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.current_timestamp())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.current_timestamp())
    contact_id: Mapped[int] = mapped_column(ForeignKey("contact.id"), nullable=False)
    archived_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    link_id: Mapped[int] = mapped_column(ForeignKey("link.id"), nullable=True)
    gte_base_embedding: Mapped[Vector] = mapped_column(Vector(768), nullable=True)
    msmarco_base_embedding: Mapped[Vector] = mapped_column(Vector(768), nullable=True)

    # Foreign key relationships
    account: Mapped["AccountORM"] = relationship(back_populates="prayer_requests")
    contact: Mapped["ContactORM"] = relationship(back_populates="prayer_requests")
    link: Mapped["LinkORM"] = relationship(back_populates="prayer_requests")

class ContactORM(Base):
    __tablename__ = 'contact'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(collation='pg_catalog."default"'), nullable=False)
    description: Mapped[str] = mapped_column(String(collation='pg_catalog."default"'), nullable=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("contact_group.id"), nullable=True)

    # Relationships
    prayer_requests: Mapped[List["PrayerRequestORM"]] = relationship(back_populates="contact")
    account: Mapped["AccountORM"] = relationship(back_populates="contacts")
    group: Mapped["GroupORM"] = relationship(back_populates="contacts")

class AccountORM(Base):
    __tablename__ = 'account'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(collation='pg_catalog."default"'), nullable=False)

    # Relationships
    prayer_requests: Mapped[List["PrayerRequestORM"]] = relationship(back_populates="account")
    contacts: Mapped[List["ContactORM"]] = relationship(back_populates="account")
    groups: Mapped[List["GroupORM"]] = relationship(back_populates="account")

class GroupORM(Base):
    __tablename__ = 'contact_group'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(collation='pg_catalog."default"'), nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)

    # Relationships
    account: Mapped["AccountORM"] = relationship(back_populates="groups")
    contacts: Mapped[List["ContactORM"]] = relationship(back_populates="group")

class LinkORM(Base):
    __tablename__ = 'link'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Relationships
    prayer_requests: Mapped[List["PrayerRequestORM"]] = relationship(back_populates="link")


def OpenPool(pg_uri: str)->scoped_session[Session]:
    engine = create_engine(pg_uri)
    Base.metadata.create_all(engine)

    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)