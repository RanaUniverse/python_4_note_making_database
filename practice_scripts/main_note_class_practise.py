"""

Here i will only checking about the idea of making notes
editing notes and little like this without 
connecting with user table just like a normal 
one table i will make this
"""

import datetime
import random  # type: ignore
from faker import Faker

from sqlmodel import (
    create_engine,
    Field,  # type: ignore
    SQLModel,
    Session,
    select,
)

fake = Faker()


class Note(SQLModel, table=True):
    __tablename__ = "note_data"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    title: str | None = Field(default=None)
    note_data: str | None = Field(default=None)
    note_id: int = Field(index=True, unique=True)
    user_id: int = Field(index=True, default=None)
    created_time: datetime.datetime
    edited_time: datetime.datetime | None = Field(default=None)


sqlite_file_name = "database_notes.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def add_new_note(
    note_obj: Note | None = None,
    title: str | None = None,
    note_data: str | None = None,
    note_id: int | None = None,
    user_id: int | None = None,
    created_time: datetime.datetime | None = None,
):
    """
    I am thinking how to do this goodly
    i will pass title, and note ie note data,user_id, and date
    """
    if not title:
        title = f"No Title is given by: {user_id}"
        print(title)
    else:
        title = f"{title.upper()}"
        print(title)

    if not note_id:
        note_id = fake.random_number(digits=5)
        print(note_id)
    if not user_id:
        user_id = 999
    if not created_time:
        now_time_ist = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=5, minutes=30))
        )

        created_time = now_time_ist
        print(created_time)

    if not note_obj:
        print("You have not given any Note Object to keep record in the database.")
        print("New Sample record will be used based on the data you provide.")
        note_obj = Note(
            title=title,
            note_data=note_data,
            note_id=note_id,
            user_id=user_id,
            created_time=created_time,
        )
        print(note_obj)
    try:
        with Session(engine) as session:
            session.add(note_obj)
            session.commit()
            session.refresh(note_obj)
            print("Note added successfully!")
            print(f"\033[32m{note_obj}\033[0m")
    except Exception as e:
        print(f"\033[31mAn error occurred while saving the note:\n{e}\033[0m")


def find_note_obj_by_note_id(note_id: int):
    """There the note id is unique per column so i will need one obj"""
    with Session(engine) as session:
        statement = select(Note).where(Note.note_id == note_id)
        note_obj = session.exec(statement).first()
        if note_obj:
            return note_obj
        else:
            print(f"No note found with note_id: {note_id}")
            return None


def find_note_by_user_id(user_id: int):
    """Here one user maybe have many notes so this is little problematic"""
    with Session(engine) as session:
        statement = select(Note).where(Note.user_id == user_id)
        results = session.exec(statement).all()
        if results:
            print(f"This has total {len(results)} Data for this user: {user_id}")
            return results
        else:
            return None


def edit_note(
    note_id: int,
    new_title: str | None = None,
    new_note_data: str | None = None,
):
    """
    This will take the note id which is unique and then it will
    update the data if no data get it will update default.
    I will call the find note by note id
    """
    if not new_title:
        new_title = f"New Title After Edit"
    if not new_note_data:
        text = f"You have not given any new data thats why i am not changeing anything 👋🖐👋🏻"
        print(text)
        return None
    now_time_ist = datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    )
    # Now i will check if the note id is valid or not then i will take the old obj and then edit this
    # i was thinnking to use upper fun instead of below code find_note_obj_by_note_id but how ???
    with Session(engine) as session:
        statement = select(Note).where(Note.note_id == note_id)
        note_obj = session.exec(statement).first()
        if note_obj:
            note_obj.title = new_title
            note_obj.note_data = new_note_data
            note_obj.edited_time = now_time_ist
            session.add(note_obj)
            session.commit()
            print(note_obj)
        else:
            print(f"No note found with note_id: {note_id}")
            return None


def main():
    create_db_and_tables()
    edit_note(40838,new_title="This is new title by me", new_note_data="dflkj")

    # note_title = "This is my new title"
    # note_to_store = fake.paragraph()
    # who_will_store = fake.random_number(12)
    # for _ in range(0):
    #     add_new_note(title=note_title, note_data=note_to_store, user_id=who_will_store)

    # abc = find_note_obj_by_note_id(93780)
    # if abc:
    #     print(abc.title)
    # else:
    #     print("No data found")

    # abc = find_note_by_user_id(67)
    # if abc:
    #     for _ in range(len(abc)):
    #         print(abc[_], "\n\n\n")
    # else:
    #     print("No data found")


if __name__ == "__main__":
    main()
