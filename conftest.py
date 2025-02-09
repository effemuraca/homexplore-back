import pathlib
import sys
from dotenv import load_dotenv


load_dotenv()
CURRENT_PATH = pathlib.Path(__file__).parent.absolute()
src_dir_path = str(CURRENT_PATH)
sys.path.insert(0, src_dir_path)

from setup.sql_setup.sql_setup import get_db_session
from entities.User.db.SQL_user import User
from modules.Auth.helpers.auth_helpers import hash_password
from modules.Auth.helpers.JwtHandler import JWTHandler
from sqlalchemy import text

def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    #Create admin user
    admin = User(
        email="testAdmin@test.com",
        first_name="testAdmin",
        last_name="testAdmin",
        password=hash_password("testAdmin"),
        user_type_id=10,
        verified=True
    )
    with get_db_session() as session:
        try:
            session.add(admin)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
            
    # Create user user
    user = User(
        email="testUser@test.com",
        first_name="testUser",
        last_name="testUser",
        password=hash_password("testUser"),
        user_type_id=1,
        verified=True
    )
    with get_db_session() as session:
        try:
            session.add(user)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
    
    # Create guest user
    guest = User(
        email="testGuest@test.com",
        first_name="testGuest",
        last_name="testGuest",
        password=hash_password("testGuest"),
        user_type_id=0,
        verified=True
    )
    with get_db_session() as session:
        try:
            session.add(guest)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
            

def decrement_sequence_value(sequence_name: str, decrement_by: int):
    with get_db_session() as session:
        try:
            # Get the current value of the sequence
            current_value = session.execute(text(f"SELECT last_value FROM {sequence_name};")).scalar()

            # Calculate the new value
            new_value = current_value - decrement_by
            if new_value < 1:
                new_value = 1  # Avoid negative values

            # Set the new value of the sequence
            session.execute(text(f"ALTER SEQUENCE {sequence_name} RESTART {new_value};"))
            session.commit()
            print(f"Sequence {sequence_name} value decremented by {decrement_by}, new value is {new_value}.")
        except Exception as e:
            print(f"Error decrementing sequence value: {e}")
            session.rollback()
        finally:
            session.close()

def pytest_sessionfinish(session, exitstatus):
    """
    Called after the whole test run finished, right before
    returning the exit status to the system.
    """
    print("Cleaning up")

    emails = ["testAdmin@test.com", "testUser@test.com", "testGuest@test.com"]

    for email in emails:
        with get_db_session() as sessionDb:
            try:
                user = sessionDb.query(User).filter_by(email=email).one_or_none()
                if user:
                    sessionDb.delete(user)
                    sessionDb.commit()
            except Exception as e:
                print(f"Error deleting user with email {email}: {e}")
                sessionDb.rollback()
    
    # Reset user counter
    # decrement_sequence_value('user_id_seq', 4)

    