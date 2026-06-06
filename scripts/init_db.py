from backend.models.database import init_db, engine


def main():
    print("Initializing database...")
    init_db()
    print(f"Database initialized at {engine.url}")


if __name__ == "__main__":
    main()
