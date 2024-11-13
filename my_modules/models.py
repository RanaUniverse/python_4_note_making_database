"""
This is the file where i will keep my table structers
"""

import datetime

from sqlmodel import (
    Field,  # type: ignore
    Relationship,
    SQLModel,
)


class UserPart(SQLModel, table=True):

    __tablename__: str = "user_data"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)

    # Below are User's Profile Details
    user_id: int = Field(index=True, unique=True)
    full_name: str | None = Field(default=None)
    email_id: str | None = Field(default=None)
    phone_no: int | None = Field(default=None)
    register_time: datetime.datetime | None = Field(default=None)

    # Some other parts
    notes_count: int | None = Field(default=None)
    is_allowed: bool = Field(default=True)
    password: str | None = Field(default=None)

    notes: list["NotePart"] = Relationship(back_populates="user")


class NotePart(SQLModel, table=True):

    __tablename__: str = "note_data"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    title: str | None = Field(default=None)
    note: str | None = Field(default=None)
    note_id: int | None = Field(index=True, unique=True)
    created_date: datetime.datetime | None = Field(default=None)
    edited_date: datetime.datetime | None = Field(default=None)

    user_id: int | None = Field(default=None, foreign_key="user_data.user_id")
    user: UserPart | None = Relationship(back_populates="notes")
