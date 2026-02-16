#!/usr/bin/env python3
"""
Database initialization script
Run this to create all database tables
"""

from app.models.database import init_db, engine, Base
from app.config import settings

def main():
    print(f"Initializing database for {settings.APP_NAME}...")
    print(f"Database URL: {engine.url}")
    
    # Create all tables
    init_db()
    
    print("\n✓ Database setup complete!")
    print("\nTables created:")
    for table in Base.metadata.sorted_tables:
        print(f"  - {table.name}")

if __name__ == "__main__":
    main()