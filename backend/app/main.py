from contextlib import asynccontextmanager
from sqlalchemy import text
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import engine, Base
from .seed import seed_database
from .routers import products, brands, categories, orders


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables, GIN index, and seed
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        # Full-text search GIN index
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_product_search "
            "ON products USING gin("
            "to_tsvector('english', "
            "coalesce(name, '') || ' ' || coalesce(tire_size, '') || ' ' || coalesce(description, '')"
            "))"
        ))
        # pg_trgm extension + trigram index for fuzzy tire size search
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_product_tire_size_trgm "
            "ON products USING gin(tire_size gin_trgm_ops)"
        ))
        conn.commit()
    # Seed database (idempotent — checks if data exists before inserting)
    seed_database()
    yield


app = FastAPI(
    title="TirePro B2B API",
    description="Wholesale Tire Ordering Platform",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(products.router)
app.include_router(brands.router)
app.include_router(categories.router)
app.include_router(orders.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
