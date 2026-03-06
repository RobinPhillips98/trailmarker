"""Contains functions for fetching enemy data and adding them to the database.

Fetches JSON files from the FoundryVTT GitHub detailing the stats of each
enemy, converts them into a format that matches the format needed by the
database, then adds the enemy to the database and deletes the raw JSON file.

"""

import argparse
import os

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import engine_sync
from models import Base, Character, Enemy, User
from populate.populate_characters import initialize_characters
from populate.populate_enemies import initialize_enemies

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session):
    username = "admin"
    password = os.getenv("ADMIN_PASSWORD")

    user = db.execute(select(User).filter(User.username == username)).scalar()

    if not user:
        hashed_password = pwd_context.hash(password)

        user = User(username=username, hashed_password=hashed_password)
        db.add(user)

    db.commit()


def drop_all_tables(engine=engine_sync):
    """Drop all tables in the database"""
    print("Starting table operations...")
    try:
        # Drop all tables
        print("Dropping all tables...")
        Base.metadata.drop_all(engine)
        # Clear any remaining connections
        print("Disposing engine...")
        engine.dispose()
        # Recreate empty tables
        print("Creating tables...")
        Base.metadata.create_all(engine)
        print("Tables created successfully")
    except Exception as e:
        print(f"Error in drop_all_tables: {str(e)}")
        raise


def drop_enemies_table(engine=engine_sync):
    """Drop and recreate only the enemies table in the database."""
    print("Starting enemies table operation...")
    try:
        print("Dropping enemies table...")
        Enemy.__table__.drop(engine)
        print("Disposing engine...")
        engine.dispose()
        print("Recreating enemies table...")
        Enemy.__table__.create(engine)
        print("Enemies table recreated successfully")
    except Exception as e:
        print(f"Error in drop_enemies_table: {str(e)}")
        raise


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r", "--rebuild", action="store_true", help="Rebuild the database"
    )
    parser.add_argument(
        "-e",
        "--rebuild_enemies",
        action="store_true",
        help="Rebuild the enemies table in the database",
    )
    args = parser.parse_args()

    # Print database URL (with password masked)
    db_url = str(engine_sync.url)
    print(f"Database URL: {db_url}")
    if "postgresql" in db_url:
        print(f"Connecting to database: {db_url.split('@')[1]}")

    if args.rebuild:
        print(
            """
###############################################
# Database Rebuild                            #
###############################################
--rebuild flag detected.
Dropping all tables and recreating the database
from scratch.
###############################################
            """
        )
        try:
            print("Dropping all tables...")
            drop_all_tables()
            print("Tables dropped successfully")
        except Exception as e:
            print(f"Error dropping tables: {e}")
            raise
    if args.rebuild_enemies:
        print(
            """
###############################################
# Enemies Table Rebuild                       #
###############################################
--rebuild_enemies flag detected.
Dropping and recreating the enemies table only.
###############################################
            """
        )
        try:
            print("Dropping enemies table...")
            drop_enemies_table()
            print("Enemies table dropped and recreated successfully")
        except Exception as e:
            print(f"Error dropping enemies table: {e}")
            raise

    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine_sync)
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise

    with Session(bind=engine_sync) as db:
        try:
            # Check if we already have data
            if (
                args.rebuild
                or args.rebuild_enemies
                or db.execute(select(Enemy).limit(1)).first() is None
            ):
                print("Populating enemy data...")
                initialize_enemies(db)
            else:
                print("Enemies already exist, skipping enemy creation")
            if (
                args.rebuild
                or db.execute(select(User).limit(1)).first() is None
            ):
                print("Populating user data...")
                create_user(db)
            else:
                print("Users already exist, skipping user creation")
            if (
                args.rebuild
                or db.execute(select(Character).limit(1)).first() is None
            ):
                print("Populating character data...")
                initialize_characters(db)
            else:
                print("Characters already exist, skipping character creation")

        except Exception as e:
            print(f"Error populating database: {e}")
            raise  # This will show the full stack trace


if __name__ == "__main__":
    main()
