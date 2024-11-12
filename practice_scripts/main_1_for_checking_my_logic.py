"""
Here i will make write the final topic of 
my database logic, where the user and note will be
connected to each others

*** The Steps i am following ***

1. I will make a User Table
2. I will make a Note storing Table
3. User -> One Part && Note -> Many Part

4. I keep email id of users as not-unique as maybe
    different people can have same email id or phone number.


"""

import datetime
import random

from sqlmodel import (
    create_engine,
    Field,  # type: ignore
    Relationship,
    select,
    Session,
    SQLModel,
)

from faker import Faker  # type: ignore

fake = Faker()


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


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(url=sqlite_url)


def create_db_and_engine():
    SQLModel.metadata.create_all(engine)


def insert_fake_data1():
    """
    This fun adding the data into database without using the relationship, just
    this add first user and then note separately so i dont want to use this
    I just made this for testing purpose.
    """
    fake_username = f"{fake.word("noun")}_{fake.word("adjective")}"
    fake_user_id = fake.random_number(5)
    fake_full_name = fake.name()
    fake_email_id = fake.ascii_free_email()

    # Below line phone no will come as str, so i need to do int(str) to check
    # so i used random_int for now
    # fake_phone_no = fake.basic_phone_number()

    fake_phone_no = fake.random_int(9000000000, 9999999999)
    fake_register_time = fake.date_time_between("-7d", "now")
    password = random.choice([fake.bothify("??##??"), None])

    fake_note_title = fake.sentence(3)
    fake_note = fake.paragraph()
    fake_note_id = fake.pyint(1, 9999)
    now_time_ist = datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    )
    with Session(engine) as session:
        fake_user = UserPart(
            username=fake_username,
            user_id=fake_user_id,
            full_name=fake_full_name,
            email_id=fake_email_id,
            phone_no=fake_phone_no,
            register_time=fake_register_time,
            password=password,
        )

        fake_note = NotePart(
            title=fake_note_title,
            note=fake_note,
            note_id=fake_note_id,
            created_date=now_time_ist,
            # edited_data=now_time_ist,
            user_id=fake_user_id,
        )
        session.add(fake_user)
        session.add(fake_note)
        session.commit()

        session.refresh(fake_user)
        session.refresh(fake_note)
        print(f"✅ User added: {fake_user}")
        print(f"✅ Note added: {fake_note}")


def insert_fake_user_and_note():
    """
    I am trying to add the relationship here
    This is working this making a new user and note and linking both
    goodly and this is one user one note like this
    """
    fake_username = f"{fake.word("noun")}_{fake.word("adjective")}"
    fake_user_id = fake.random_number(5)
    fake_full_name = fake.name()
    fake_email_id = fake.ascii_free_email()

    # Below line phone no will come as str, so i need to do int(str) to check
    # so i used random_int for now
    # fake_phone_no = fake.basic_phone_number()

    fake_phone_no = fake.random_int(9000000000, 9999999999)
    fake_register_time = fake.date_time_between("-7d", "now")
    password = random.choice([fake.bothify("??##??"), None])

    fake_note_title = fake.sentence(3)
    fake_note = fake.paragraph()
    fake_note_id = fake.pyint(1, 9999)
    now_time_ist = datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    )
    with Session(engine) as session:
        fake_user = UserPart(
            username=fake_username,
            user_id=fake_user_id,
            full_name=fake_full_name,
            email_id=fake_email_id,
            phone_no=fake_phone_no,
            register_time=fake_register_time,
            password=password,
        )

        fake_note = NotePart(
            title=fake_note_title,
            note=fake_note,
            note_id=fake_note_id,
            created_date=now_time_ist,
            # edited_data=now_time_ist,
            # user_id=fake_user_id,
            user=fake_user,
        )
        session.add(fake_user)
        session.add(fake_note)
        session.commit()

        session.refresh(fake_user)
        session.refresh(fake_note)
        print(f"✅ User added: {fake_user}")
        print(f"✅ Note added: {fake_note}")


def insert_example_data():
    with Session(engine) as session:
        user = UserPart(
            username="john_doe14",
            user_id=1004,
            full_name="John Doe",
            email_id="johndoe@example.com",
            phone_no=1234567890,
            notes_count=1,
            password="password123",
        )

        note = NotePart(
            title="Leaving Note",
            note="I am going to exis this room.",
            note_id=104,
            created_date=datetime.datetime.now(),
            user=user,
        )

        session.add(user)
        session.add(note)
        session.commit()
        session.refresh(user)
        session.refresh(note)
        print(f"✅ User added: {user}")
        print(f"✅ Note added: {note}")


def search_note_by_user_id(user_id: int):
    """I am making this which will take the user_id and find the list of note obj"""
    with Session(engine) as session:
        statement = select(NotePart).where(NotePart.user_id == user_id)
        results = session.exec(statement).all()
        print(results)
        print("You will get", len(results), "numbers of notes made by u")


# This below two function are doing one work no need later i make good funcion


def get_one_note_obj(note_id: int):
    "i will pass the note id and then it will give me None or a note obj"
    with Session(engine) as session:
        statement = select(NotePart).where(NotePart.note_id == note_id)
        result = session.exec(statement).first()
        print(result)
        return result


def edit_a_old_note(
    note_obj: NotePart | None, new_title: str | None, new_note: str | None
):
    """This will get a note obj and then it will do edit the old things"""
    if not note_obj:
        print("Sorry You have not passed any Note Obj i am not doing anything now")
        return None
    with Session(engine) as session:
        note_obj.title = new_title
        note_obj.note = new_note
        session.add(note_obj)
        session.commit()
        session.refresh(note_obj)
        print(note_obj)


# Now i will merger this upper two fun in one fun below


def edit_note_by_note_id(note_id: int, new_title: str | None, new_note: str | None):
    with Session(engine) as session:
        statement = select(NotePart).where(NotePart.note_id == note_id)
        note_obj = session.exec(statement).first()
        now_time_ist = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=5, minutes=30))
        )
        if not note_obj:
            print(
                "\033[31m❌ Sorry, no note found with this note ID. "
                "Please send a valid note ID. ❌\033[0m"
            )
            return None
        else:
            note_obj.title = new_title
            note_obj.note = new_note
            note_obj.edited_date = now_time_ist
            session.add(note_obj)
            session.commit()
            session.refresh(note_obj)
            print(note_obj)
            return note_obj


def get_user_from_note_id(note_id: int):
    if type(note_id) != int:
        print("Pleas send valid note id which is integer value")
    with Session(engine) as session:
        statement = select(NotePart).where(NotePart.note_id == note_id)
        note_obj = session.exec(statement).first()
        if not note_obj:
            print(f"No Note found with this current {note_id}")
        else:
            print(note_obj.user)


def note_ownership_checking(note_id: int, password: str | None, user_id: int):
    """
    pass the noteid and password and it will retrun the title and
    data of the note if password match and user id also
    """
    with Session(engine) as session:
        statement = select(NotePart).where(NotePart.note_id == note_id)
        note_obj = session.exec(statement).first()

        if not note_obj:
            print(f"No note found with note ID {note_id}.")
            return

        user = note_obj.user
        if not user:
            print("No user associated with this note.")
            return

        if user.user_id == user_id and user.password == password:
            print(f"Thanks For provide correct id and password")
            print(f"Title: {note_obj.title}")
            print(f"Content: {note_obj.note}")
        else:
            print("User ID or password does not match. Access denied.")


def main():
    create_db_and_engine()
    # insert_example_data()
    # note_ownership_checking(1938, None, 10773)

    # get_user_from_note_id(97)

    # note_id_tochange = 97
    # new_title_to_change = fake.word("noun")
    # new_note_data = fake.sentence(10)
    # edit_note_by_note_id(note_id_tochange, new_title_to_change, new_note_data)

    # abc = get_one_note_obj(5793)
    # edit_a_old_note(abc, "new title", "this is new data")

    for _ in range(10):
        insert_fake_user_and_note()
        if _ == 9:
            print("All The 10 Data has been inserted")


if __name__ == "__main__":
    main()
