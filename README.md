# TirePro B2B — Wholesale Tire Ordering Platform

Full-stack B2B demo built with FastAPI, React, PostgreSQL, and Docker.
Features **FEFO (First Expired, First Out) inventory management** and **faceted search** — demonstrating tire industry domain expertise.

## Tech Stack

**Backend:** Python 3.11 / FastAPI / SQLAlchemy / PostgreSQL
**Frontend:** React 18 / Vite / Tailwind CSS / React Router / TanStack Query
**Infrastructure:** Docker / Docker Compose / Nginx
**Search:** PostgreSQL full-text search (GIN index) + pg_trgm trigram fuzzy matching
**Inventory:** FEFO allocation with DOT date code tracking and age-based pricing

## Quick Start

```bash
docker-compose up --build
```

- **Frontend:** http://localhost:3000
- **API Docs (Swagger):** http://localhost:8000/docs
- **API Health Check:** http://localhost:8000/api/health

The database is automatically created and seeded with 50 products on first startup.

## Key Features

### FEFO Inventory Management
- **DOT Date Tracking** — Every tire has a DOT manufacture date code (WWYY format)
- **Age Classification** — Tires are categorized: Fresh (<2yr), Normal (2-4yr), Aging (4-5yr), Old (5-6yr), Critical (6+yr)
- **Oldest-First Allocation** — Orders are fulfilled from the oldest available stock across all warehouses
- **Age-Based Discounts** — Aging: 10% off, Old: 20% off, Critical: 30% off (applied automatically)
- **Multi-Warehouse Demo** — 10 SKUs are duplicated across warehouses with different manufacture dates

### Faceted Search
- **Dynamic Filter Counts** — Each filter option shows the number of matching products (Amazon-style)
- **Cross-Dimensional Facets** — Brand, Category, Tire Type, Tire Size, Age, and Price Range
- **Smart Count Computation** — Counts are calculated with all OTHER filters applied (not the current dimension)
- **Collapsible Sections** — Clean UI with expandable filter groups

### Core Platform
- **Product Catalog** — Browse 50 wholesale tires across 10 brands and 5 categories
- **Full-Text Search** — PostgreSQL-powered search across tire name, size, and description
- **Shopping Cart** — Client-side cart with localStorage persistence
- **Order Placement** — Orders with automatic FEFO allocation, stock validation, and tax (7%)
- **Order History** — View orders with warehouse source, age badges, and discount details
- **Responsive Design** — Desktop, tablet, and mobile layouts

## API Endpoints

```
GET  /api/health                    → Health check
GET  /api/products                  → Paginated product list with filters
GET  /api/products/{id}             → Single product detail (with age/FEFO data)
GET  /api/products/facets           → Dynamic facet counts for all filter dimensions
GET  /api/products/inventory/{id}   → Warehouse inventory breakdown (FEFO order)
GET  /api/brands                    → All brands with product counts
GET  /api/categories                → All categories with product counts
POST /api/orders                    → Create order (FEFO allocation + age discounts)
GET  /api/orders                    → List orders (recent first)
GET  /api/orders/{order_number}     → Order detail with FEFO allocation info
```

## Project Structure

```
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── wait-for-db.sh
│   └── app/
│       ├── main.py            # FastAPI app, lifespan, CORS, GIN indexes
│       ├── config.py          # Settings from env
│       ├── database.py        # Engine, session, Base
│       ├── models.py          # SQLAlchemy models (with age properties)
│       ├── schemas.py         # Pydantic schemas (incl. facets)
│       ├── seed.py            # 50 products with DOT codes + FEFO duplicates
│       ├── fefo.py            # FEFO allocation engine + age discount logic
│       └── routers/
│           ├── products.py    # Product CRUD + facets + inventory
│           ├── brands.py      # Brand listing
│           ├── categories.py  # Category listing
│           └── orders.py      # Order CRUD with FEFO integration
└── frontend/
    ├── Dockerfile
    ├── nginx.conf
    └── src/
        ├── App.jsx
        ├── api/client.js
        ├── context/CartContext.jsx
        ├── components/
        │   ├── AgeBadge.jsx       # Color-coded age badge + legend
        │   ├── FilterSidebar.jsx  # Faceted filter UI with counts
        │   ├── ProductCard.jsx    # Card with age badge + effective pricing
        │   └── ...
        └── pages/
            ├── Catalog.jsx        # Faceted search catalog
            ├── ProductDetail.jsx  # Warehouse inventory table (FEFO)
            ├── Checkout.jsx       # FEFO allocation confirmation
            ├── Orders.jsx         # Order detail with warehouse/age info
            └── ...
```

## Brands

Sumitomo, Multi-Mile, Power King, Sigma, Harvest King, Cordovan, Eldorado, Duro, Achilles, Telstar

## FEFO Demo Walkthrough

1. Browse the catalog and notice age badges on each tire (Fresh, Normal, Aging, etc.)
2. Filter by "Aging" or "Old" in the FEFO filter to see discounted inventory
3. Click a tire that appears in multiple warehouses to see the inventory breakdown
4. Add it to cart and place an order — the system allocates from the oldest stock first
5. View the order to see which warehouse each item ships from and any age discounts applied

## Cloud Run Deployment

This project is structured for GCP Cloud Run deployment:
- Backend and frontend are separate containerized services
- Environment variables configure database connection and CORS
- PostgreSQL can be replaced with Cloud SQL
- Nginx reverse proxy handles API routing in production

## Built By

**Andres Jose** — Senior Full Stack Developer
