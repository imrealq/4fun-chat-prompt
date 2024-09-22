import argparse

import db


def main():
    parser = argparse.ArgumentParser(description="Add a user to the database")
    parser.add_argument("email", help="User's email address")
    parser.add_argument("name", help="User's name")
    parser.add_argument("password", help="User's password")

    args = parser.parse_args()

    db.init_db()
    if db.add_user(args.email, args.name, args.password):
        print(f"User {args.email} added successfully.")
    else:
        print(f"Error: User with email {args.email} already exists.")


if __name__ == "__main__":
    main()
