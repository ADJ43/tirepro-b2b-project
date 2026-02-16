#!/usr/bin/env python3
"""
One-time database seed job for Cloud Run.
Run after initial deployment to populate the Cloud SQL database.

Usage (Cloud Run job):
  gcloud run jobs execute tirepro-seed --region us-central1 --wait
"""
import sys
from app.database import engine, Base
from sqlalchemy import text
from app.seed import seed_database

if __name__ == "__main__":
    print("Starting database seed...")

    # Create tables
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

    # Create indexes
    print("Creating indexes...")
    with engine.connect() as conn:
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_product_search "
            "ON products USING gin("
            "to_tsvector('english', "
            "coalesce(name, '') || ' ' || coalesce(tire_size, '') || ' ' || coalesce(description, '')"
            "))"
        ))
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_product_tire_size_trgm "
            "ON products USING gin(tire_size gin_trgm_ops)"
        ))
        conn.commit()

    # Seed data
    print("Seeding data...")
    try:
        seed_database()
        print("Database seeded successfully!")
        sys.exit(0)
    except Exception as e:
        print(f"Seed failed: {e}")
        sys.exit(1)
