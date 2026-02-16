from datetime import date
from .database import SessionLocal
from .models import Brand, Category, Product


def dot_to_date(dot_code: str) -> date:
    """Convert DOT date code (WWYY) to a Python date.
    Example: '2522' = week 25, year 2022 → June 2022"""
    week = int(dot_code[:2])
    year = 2000 + int(dot_code[2:])
    return date.fromisocalendar(year, max(1, min(week, 52)), 1)


def seed_database():
    db = SessionLocal()
    try:
        if db.query(Brand).count() > 0:
            print("Database already seeded.")
            return

        # --- Brands ---
        brands_data = [
            {"name": "Sumitomo", "slug": "sumitomo", "description": "Japanese manufacturer known for quality all-season and performance tires."},
            {"name": "Multi-Mile", "slug": "multi-mile", "description": "Value-oriented brand offering reliable tires across multiple categories."},
            {"name": "Power King", "slug": "power-king", "description": "Specializing in commercial, trailer, and specialty tires."},
            {"name": "Sigma", "slug": "sigma", "description": "Mid-range brand with a focus on passenger and crossover tires."},
            {"name": "Harvest King", "slug": "harvest-king", "description": "Agricultural and farm tire specialist."},
            {"name": "Cordovan", "slug": "cordovan", "description": "Budget-friendly passenger and touring tire manufacturer."},
            {"name": "Eldorado", "slug": "eldorado", "description": "Performance and passenger tire brand with competitive pricing."},
            {"name": "Duro", "slug": "duro", "description": "Commercial and industrial tire manufacturer."},
            {"name": "Achilles", "slug": "achilles", "description": "Indonesian tire brand offering performance and passenger tires."},
            {"name": "Telstar", "slug": "telstar", "description": "All-season and touring tire brand for everyday driving."},
        ]
        brands = {}
        for bd in brands_data:
            b = Brand(**bd)
            db.add(b)
            db.flush()
            brands[bd["name"]] = b.id

        # --- Categories ---
        categories_data = [
            {"name": "Passenger", "slug": "passenger", "description": "Standard passenger car tires for sedans, coupes, and hatchbacks."},
            {"name": "Light Truck/SUV", "slug": "light-truck-suv", "description": "Tires designed for light trucks, SUVs, and crossover vehicles."},
            {"name": "Commercial Truck", "slug": "commercial-truck", "description": "Heavy-duty tires for commercial trucks and fleet vehicles."},
            {"name": "Farm & AG", "slug": "farm-ag", "description": "Agricultural tires for tractors, combines, and farm equipment."},
            {"name": "Trailer & RV", "slug": "trailer-rv", "description": "Specialty tires for trailers, RVs, and towable equipment."},
        ]
        categories = {}
        for cd in categories_data:
            c = Category(**cd)
            db.add(c)
            db.flush()
            categories[cd["name"]] = c.id

        # --- Products (30 base + ~20 FEFO duplicates across warehouses) ---
        warehouses = ["Palm Beach Gardens, FL", "Dallas, TX", "Chicago, IL", "Phoenix, AZ"]

        # Base products — each now has a DOT code (WWYY format)
        products_data = [
            # Sumitomo (4)
            {"sku": "SUM-HTRAS-P03-22565R17", "name": "Sumitomo HTR A/S P03", "brand": "Sumitomo", "category": "Passenger", "tire_size": "225/65R17", "load_index": "102", "speed_rating": "H", "tire_type": "All-Season", "description": "Premium all-season passenger tire with excellent wet and dry traction. Features an asymmetric tread pattern for enhanced handling.", "wholesale_price": 89.50, "msrp": 129.99, "stock_quantity": 156, "warehouse": warehouses[0], "dot_code": "0125"},
            {"sku": "SUM-ENCAT2-26570R17", "name": "Sumitomo Encounter AT2", "brand": "Sumitomo", "category": "Light Truck/SUV", "tire_size": "265/70R17", "load_index": "115", "speed_rating": "T", "tire_type": "All-Terrain", "description": "Rugged all-terrain tire for trucks and SUVs. Aggressive tread design with stone ejectors for off-road capability.", "wholesale_price": 142.00, "msrp": 199.99, "stock_quantity": 89, "warehouse": warehouses[1], "dot_code": "3524"},
            {"sku": "SUM-HTRAS-P03-20555R16", "name": "Sumitomo HTR A/S P03", "brand": "Sumitomo", "category": "Passenger", "tire_size": "205/55R16", "load_index": "94", "speed_rating": "V", "tire_type": "All-Season", "description": "Versatile all-season tire offering a quiet ride and long tread life for compact and mid-size sedans.", "wholesale_price": 72.00, "msrp": 109.99, "stock_quantity": 234, "warehouse": warehouses[2], "dot_code": "1025"},
            {"sku": "SUM-HTRZ5-24540R18", "name": "Sumitomo HTR Z5", "brand": "Sumitomo", "category": "Passenger", "tire_size": "245/40R18", "load_index": "97", "speed_rating": "W", "tire_type": "Performance", "description": "Ultra-high performance summer tire with maximum grip and responsive handling for sports cars.", "wholesale_price": 115.00, "msrp": 169.99, "stock_quantity": 78, "warehouse": warehouses[0], "dot_code": "2024"},

            # Multi-Mile (4)
            {"sku": "MM-WCTXTX-27555R20", "name": "Multi-Mile Wild Country XTX Sport", "brand": "Multi-Mile", "category": "Light Truck/SUV", "tire_size": "275/55R20", "load_index": "117", "speed_rating": "T", "tire_type": "All-Terrain", "description": "Versatile all-terrain tire with aggressive styling and year-round traction for trucks and SUVs.", "wholesale_price": 118.75, "msrp": 174.99, "stock_quantity": 204, "warehouse": warehouses[1], "dot_code": "4824"},
            {"sku": "MM-MXTRS-20555R16", "name": "Multi-Mile Matrix Tour RS", "brand": "Multi-Mile", "category": "Passenger", "tire_size": "205/55R16", "load_index": "91", "speed_rating": "H", "tire_type": "Touring", "description": "Comfortable touring tire with low road noise and excellent tread wear for daily commuters.", "wholesale_price": 62.00, "msrp": 94.99, "stock_quantity": 312, "warehouse": warehouses[2], "dot_code": "1524"},
            {"sku": "MM-WCTXTX-23575R15", "name": "Multi-Mile Wild Country XTX Sport", "brand": "Multi-Mile", "category": "Light Truck/SUV", "tire_size": "235/75R15", "load_index": "109", "speed_rating": "S", "tire_type": "All-Terrain", "description": "All-terrain tire built for older trucks and SUVs. Provides dependable off-road traction with highway comfort.", "wholesale_price": 98.00, "msrp": 144.99, "stock_quantity": 167, "warehouse": warehouses[3], "dot_code": "2225"},
            {"sku": "MM-MXTRSP-21560R16", "name": "Multi-Mile Matrix Tour RS Plus", "brand": "Multi-Mile", "category": "Passenger", "tire_size": "215/60R16", "load_index": "95", "speed_rating": "H", "tire_type": "Touring", "description": "Enhanced touring tire with improved wet performance and extended tread life warranty.", "wholesale_price": 68.50, "msrp": 99.99, "stock_quantity": 278, "warehouse": warehouses[0], "dot_code": "0824"},

            # Power King (3)
            {"sku": "PK-TMSTR2-22575R15", "name": "Power King Towmax STR II", "brand": "Power King", "category": "Trailer & RV", "tire_size": "ST225/75R15", "load_index": "117", "speed_rating": "L", "tire_type": "Highway", "description": "Premium trailer tire with reinforced sidewalls and heat-resistant compound for long highway hauls.", "wholesale_price": 52.00, "msrp": 79.99, "stock_quantity": 445, "warehouse": warehouses[1], "dot_code": "3025"},
            {"sku": "PK-SHLT-24575R16", "name": "Power King Super Highway LT", "brand": "Power King", "category": "Light Truck/SUV", "tire_size": "LT245/75R16", "load_index": "120", "speed_rating": "S", "tire_type": "Highway", "description": "Light truck highway tire designed for load-carrying capability and long-distance durability.", "wholesale_price": 98.50, "msrp": 149.99, "stock_quantity": 67, "warehouse": warehouses[2], "dot_code": "4223"},
            {"sku": "PK-TMSTR2-20575R15", "name": "Power King Towmax STR II", "brand": "Power King", "category": "Trailer & RV", "tire_size": "ST205/75R15", "load_index": "107", "speed_rating": "L", "tire_type": "Highway", "description": "Reliable trailer tire for utility and boat trailers. Steel-belted construction for stability.", "wholesale_price": 45.00, "msrp": 69.99, "stock_quantity": 389, "warehouse": warehouses[3], "dot_code": "0525"},

            # Sigma (3)
            {"sku": "SIG-MCSLE-23560R18", "name": "Sigma Mirada Crosstour SLE", "brand": "Sigma", "category": "Passenger", "tire_size": "235/60R18", "load_index": "107", "speed_rating": "H", "tire_type": "All-Season", "description": "Crossover all-season tire with optimized contact patch for balanced handling and comfort.", "wholesale_price": 78.25, "msrp": 119.99, "stock_quantity": 178, "warehouse": warehouses[0], "dot_code": "2524"},
            {"sku": "SIG-MCSLE-22560R17", "name": "Sigma Mirada Crosstour SLE", "brand": "Sigma", "category": "Passenger", "tire_size": "225/60R17", "load_index": "99", "speed_rating": "H", "tire_type": "All-Season", "description": "Versatile all-season tire for mid-size crossovers. Four-groove tread design for water evacuation.", "wholesale_price": 74.00, "msrp": 112.99, "stock_quantity": 195, "warehouse": warehouses[1], "dot_code": "1825"},
            {"sku": "SIG-SPTRXL-21545R17", "name": "Sigma Sport Trax HP", "brand": "Sigma", "category": "Passenger", "tire_size": "215/45R17", "load_index": "91", "speed_rating": "W", "tire_type": "Performance", "description": "High-performance tire for sport sedans with enhanced cornering grip and responsive steering.", "wholesale_price": 82.50, "msrp": 124.99, "stock_quantity": 112, "warehouse": warehouses[2], "dot_code": "3624"},

            # Harvest King (2)
            {"sku": "HK-FPAP-169R30", "name": "Harvest King Field Pro All Purpose", "brand": "Harvest King", "category": "Farm & AG", "tire_size": "16.9-30", "load_index": "---", "speed_rating": "---", "tire_type": "AG/Farm", "description": "Heavy-duty agricultural tire for tractors and farm equipment. Deep lugs for superior field traction.", "wholesale_price": 485.00, "msrp": 649.99, "stock_quantity": 23, "warehouse": warehouses[1], "dot_code": "2023"},
            {"sku": "HK-FPHT-111L15", "name": "Harvest King Field Pro Highway", "brand": "Harvest King", "category": "Farm & AG", "tire_size": "11L-15", "load_index": "---", "speed_rating": "---", "tire_type": "AG/Farm", "description": "Farm implement tire for wagons and hay equipment. Designed for highway transport of agricultural machinery.", "wholesale_price": 68.00, "msrp": 99.99, "stock_quantity": 156, "warehouse": warehouses[3], "dot_code": "4024"},

            # Cordovan (3)
            {"sku": "CRD-GPTRS-19565R15", "name": "Cordovan Grand Prix Tour RS", "brand": "Cordovan", "category": "Passenger", "tire_size": "195/65R15", "load_index": "91", "speed_rating": "H", "tire_type": "Touring", "description": "Budget-friendly touring tire with a comfortable ride and dependable all-season performance.", "wholesale_price": 54.00, "msrp": 82.99, "stock_quantity": 267, "warehouse": warehouses[0], "dot_code": "0225"},
            {"sku": "CRD-GPTRS-18565R15", "name": "Cordovan Grand Prix Tour RS", "brand": "Cordovan", "category": "Passenger", "tire_size": "185/65R15", "load_index": "88", "speed_rating": "H", "tire_type": "Touring", "description": "Economical touring tire for compact cars. Provides quiet highway driving and good fuel efficiency.", "wholesale_price": 48.00, "msrp": 74.99, "stock_quantity": 340, "warehouse": warehouses[2], "dot_code": "4525"},
            {"sku": "CRD-GPTAS-22565R17", "name": "Cordovan Grand Prix Tour AS", "brand": "Cordovan", "category": "Passenger", "tire_size": "225/65R17", "load_index": "102", "speed_rating": "H", "tire_type": "All-Season", "description": "All-season touring tire for crossovers and mid-size SUVs. Optimized for long tread life.", "wholesale_price": 65.00, "msrp": 99.99, "stock_quantity": 198, "warehouse": warehouses[1], "dot_code": "3225"},

            # Eldorado (2)
            {"sku": "ELD-ZRS-24540R18", "name": "Eldorado ZR Sport", "brand": "Eldorado", "category": "Passenger", "tire_size": "245/40R18", "load_index": "97", "speed_rating": "W", "tire_type": "Performance", "description": "Max-performance tire with aggressive tread pattern for sport cars and coupes. Excellent dry grip.", "wholesale_price": 95.00, "msrp": 144.99, "stock_quantity": 134, "warehouse": warehouses[0], "dot_code": "1524"},
            {"sku": "ELD-LGTAS-21555R17", "name": "Eldorado Legend Tour A/S", "brand": "Eldorado", "category": "Passenger", "tire_size": "215/55R17", "load_index": "94", "speed_rating": "V", "tire_type": "All-Season", "description": "Premium all-season tire with silica compound for wet traction and a smooth, quiet ride.", "wholesale_price": 79.00, "msrp": 119.99, "stock_quantity": 221, "warehouse": warehouses[3], "dot_code": "2825"},

            # Duro (3)
            {"sku": "DUR-DL6210-22570R195", "name": "Duro DL6210 Frontrunner", "brand": "Duro", "category": "Commercial Truck", "tire_size": "225/70R19.5", "load_index": "128", "speed_rating": "L", "tire_type": "All-Position", "description": "Commercial all-position tire for regional and urban delivery trucks. Long-lasting tread compound.", "wholesale_price": 195.00, "msrp": 279.99, "stock_quantity": 56, "warehouse": warehouses[2], "dot_code": "0824"},
            {"sku": "DUR-DL6220-11R225", "name": "Duro DL6220 Stronghaul", "brand": "Duro", "category": "Commercial Truck", "tire_size": "11R22.5", "load_index": "146", "speed_rating": "L", "tire_type": "Drive", "description": "Heavy-duty drive tire for long-haul trucks. Deep tread depth for maximum mileage and traction.", "wholesale_price": 225.00, "msrp": 329.99, "stock_quantity": 34, "warehouse": warehouses[1], "dot_code": "1923"},
            {"sku": "DUR-DL6300-29575R225", "name": "Duro DL6300 Hauler", "brand": "Duro", "category": "Commercial Truck", "tire_size": "295/75R22.5", "load_index": "144", "speed_rating": "L", "tire_type": "Drive", "description": "Premium drive axle tire with enhanced fuel efficiency and retreadable casing.", "wholesale_price": 245.00, "msrp": 359.99, "stock_quantity": 28, "warehouse": warehouses[3], "dot_code": "3524"},

            # Achilles (3)
            {"sku": "ACH-ATRS2-22545R18", "name": "Achilles ATR Sport 2", "brand": "Achilles", "category": "Passenger", "tire_size": "225/45R18", "load_index": "95", "speed_rating": "W", "tire_type": "Performance", "description": "Ultra-high performance tire with silica-infused compound for superior wet and dry grip.", "wholesale_price": 72.50, "msrp": 109.99, "stock_quantity": 198, "warehouse": warehouses[0], "dot_code": "2025"},
            {"sku": "ACH-ATRS2-24535R20", "name": "Achilles ATR Sport 2", "brand": "Achilles", "category": "Passenger", "tire_size": "245/35R20", "load_index": "95", "speed_rating": "W", "tire_type": "Performance", "description": "Low-profile performance tire for luxury and sport sedans. Directional tread for water evacuation.", "wholesale_price": 88.00, "msrp": 134.99, "stock_quantity": 145, "warehouse": warehouses[1], "dot_code": "4424"},
            {"sku": "ACH-868AS-20560R16", "name": "Achilles 868 All Seasons", "brand": "Achilles", "category": "Passenger", "tire_size": "205/60R16", "load_index": "92", "speed_rating": "H", "tire_type": "All-Season", "description": "Affordable all-season tire for sedans and compacts. Symmetric tread pattern for even wear.", "wholesale_price": 56.00, "msrp": 84.99, "stock_quantity": 310, "warehouse": warehouses[2], "dot_code": "1225"},

            # Telstar (3)
            {"sku": "TEL-WZAS-21560R16", "name": "Telstar Weatherizer AS", "brand": "Telstar", "category": "Passenger", "tire_size": "215/60R16", "load_index": "95", "speed_rating": "H", "tire_type": "All-Season", "description": "Dependable all-season tire engineered for wet weather performance and year-round reliability.", "wholesale_price": 58.00, "msrp": 89.99, "stock_quantity": 289, "warehouse": warehouses[3], "dot_code": "3825"},
            {"sku": "TEL-WZAS-22555R17", "name": "Telstar Weatherizer AS", "brand": "Telstar", "category": "Passenger", "tire_size": "225/55R17", "load_index": "97", "speed_rating": "V", "tire_type": "All-Season", "description": "Mid-size sedan all-season tire with variable pitch tread for reduced road noise.", "wholesale_price": 64.00, "msrp": 97.99, "stock_quantity": 256, "warehouse": warehouses[0], "dot_code": "0525"},
            {"sku": "TEL-WLDAT-23570R16", "name": "Telstar Wildcat A/T", "brand": "Telstar", "category": "Light Truck/SUV", "tire_size": "235/70R16", "load_index": "106", "speed_rating": "T", "tire_type": "All-Terrain", "description": "Light truck all-terrain tire with 3-ply sidewall construction for durability on and off road.", "wholesale_price": 105.00, "msrp": 159.99, "stock_quantity": 143, "warehouse": warehouses[1], "dot_code": "2224"},
        ]

        # --- FEFO Duplicate SKUs: same tire, different warehouses, different ages ---
        # These demonstrate FEFO by having the same product in multiple locations with
        # varying manufacture dates. The system should ship oldest stock first.
        fefo_duplicates = [
            # Sumitomo HTR A/S P03 225/65R17 — original is Fresh in PBG (DOT 0125)
            {"sku": "SUM-HTRAS-P03-22565R17-DAL", "name": "Sumitomo HTR A/S P03", "brand": "Sumitomo", "category": "Passenger", "tire_size": "225/65R17", "load_index": "102", "speed_rating": "H", "tire_type": "All-Season", "description": "Premium all-season passenger tire with excellent wet and dry traction. Features an asymmetric tread pattern for enhanced handling.", "wholesale_price": 89.50, "msrp": 129.99, "stock_quantity": 48, "warehouse": warehouses[1], "dot_code": "1522"},
            {"sku": "SUM-HTRAS-P03-22565R17-CHI", "name": "Sumitomo HTR A/S P03", "brand": "Sumitomo", "category": "Passenger", "tire_size": "225/65R17", "load_index": "102", "speed_rating": "H", "tire_type": "All-Season", "description": "Premium all-season passenger tire with excellent wet and dry traction. Features an asymmetric tread pattern for enhanced handling.", "wholesale_price": 89.50, "msrp": 129.99, "stock_quantity": 24, "warehouse": warehouses[2], "dot_code": "3020"},

            # Multi-Mile Wild Country XTX Sport 275/55R20 — original is Fresh in Dallas (DOT 4824)
            {"sku": "MM-WCTXTX-27555R20-PBG", "name": "Multi-Mile Wild Country XTX Sport", "brand": "Multi-Mile", "category": "Light Truck/SUV", "tire_size": "275/55R20", "load_index": "117", "speed_rating": "T", "tire_type": "All-Terrain", "description": "Versatile all-terrain tire with aggressive styling and year-round traction for trucks and SUVs.", "wholesale_price": 118.75, "msrp": 174.99, "stock_quantity": 36, "warehouse": warehouses[0], "dot_code": "2021"},
            {"sku": "MM-WCTXTX-27555R20-PHX", "name": "Multi-Mile Wild Country XTX Sport", "brand": "Multi-Mile", "category": "Light Truck/SUV", "tire_size": "275/55R20", "load_index": "117", "speed_rating": "T", "tire_type": "All-Terrain", "description": "Versatile all-terrain tire with aggressive styling and year-round traction for trucks and SUVs.", "wholesale_price": 118.75, "msrp": 174.99, "stock_quantity": 18, "warehouse": warehouses[3], "dot_code": "1019"},

            # Cordovan Grand Prix Tour RS 195/65R15 — original is Fresh in PBG (DOT 0225)
            {"sku": "CRD-GPTRS-19565R15-DAL", "name": "Cordovan Grand Prix Tour RS", "brand": "Cordovan", "category": "Passenger", "tire_size": "195/65R15", "load_index": "91", "speed_rating": "H", "tire_type": "Touring", "description": "Budget-friendly touring tire with a comfortable ride and dependable all-season performance.", "wholesale_price": 54.00, "msrp": 82.99, "stock_quantity": 92, "warehouse": warehouses[1], "dot_code": "2823"},
            {"sku": "CRD-GPTRS-19565R15-PHX", "name": "Cordovan Grand Prix Tour RS", "brand": "Cordovan", "category": "Passenger", "tire_size": "195/65R15", "load_index": "91", "speed_rating": "H", "tire_type": "Touring", "description": "Budget-friendly touring tire with a comfortable ride and dependable all-season performance.", "wholesale_price": 54.00, "msrp": 82.99, "stock_quantity": 15, "warehouse": warehouses[3], "dot_code": "0820"},

            # Duro DL6220 Stronghaul 11R22.5 — original is Normal in Dallas (DOT 1923)
            {"sku": "DUR-DL6220-11R225-CHI", "name": "Duro DL6220 Stronghaul", "brand": "Duro", "category": "Commercial Truck", "tire_size": "11R22.5", "load_index": "146", "speed_rating": "L", "tire_type": "Drive", "description": "Heavy-duty drive tire for long-haul trucks. Deep tread depth for maximum mileage and traction.", "wholesale_price": 225.00, "msrp": 329.99, "stock_quantity": 12, "warehouse": warehouses[2], "dot_code": "4520"},
            {"sku": "DUR-DL6220-11R225-PHX", "name": "Duro DL6220 Stronghaul", "brand": "Duro", "category": "Commercial Truck", "tire_size": "11R22.5", "load_index": "146", "speed_rating": "L", "tire_type": "Drive", "description": "Heavy-duty drive tire for long-haul trucks. Deep tread depth for maximum mileage and traction.", "wholesale_price": 225.00, "msrp": 329.99, "stock_quantity": 8, "warehouse": warehouses[3], "dot_code": "2219"},

            # Achilles ATR Sport 2 225/45R18 — original is Fresh in PBG (DOT 2025)
            {"sku": "ACH-ATRS2-22545R18-DAL", "name": "Achilles ATR Sport 2", "brand": "Achilles", "category": "Passenger", "tire_size": "225/45R18", "load_index": "95", "speed_rating": "W", "tire_type": "Performance", "description": "Ultra-high performance tire with silica-infused compound for superior wet and dry grip.", "wholesale_price": 72.50, "msrp": 109.99, "stock_quantity": 64, "warehouse": warehouses[1], "dot_code": "3522"},
            {"sku": "ACH-ATRS2-22545R18-PHX", "name": "Achilles ATR Sport 2", "brand": "Achilles", "category": "Passenger", "tire_size": "225/45R18", "load_index": "95", "speed_rating": "W", "tire_type": "Performance", "description": "Ultra-high performance tire with silica-infused compound for superior wet and dry grip.", "wholesale_price": 72.50, "msrp": 109.99, "stock_quantity": 20, "warehouse": warehouses[3], "dot_code": "1521"},

            # Telstar Wildcat A/T 235/70R16 — original is Normal in Dallas (DOT 2224)
            {"sku": "TEL-WLDAT-23570R16-CHI", "name": "Telstar Wildcat A/T", "brand": "Telstar", "category": "Light Truck/SUV", "tire_size": "235/70R16", "load_index": "106", "speed_rating": "T", "tire_type": "All-Terrain", "description": "Light truck all-terrain tire with 3-ply sidewall construction for durability on and off road.", "wholesale_price": 105.00, "msrp": 159.99, "stock_quantity": 42, "warehouse": warehouses[2], "dot_code": "0821"},
            {"sku": "TEL-WLDAT-23570R16-PHX", "name": "Telstar Wildcat A/T", "brand": "Telstar", "category": "Light Truck/SUV", "tire_size": "235/70R16", "load_index": "106", "speed_rating": "T", "tire_type": "All-Terrain", "description": "Light truck all-terrain tire with 3-ply sidewall construction for durability on and off road.", "wholesale_price": 105.00, "msrp": 159.99, "stock_quantity": 10, "warehouse": warehouses[3], "dot_code": "2519"},

            # Sigma Mirada Crosstour SLE 235/60R18 — original is Normal in PBG (DOT 2524)
            {"sku": "SIG-MCSLE-23560R18-DAL", "name": "Sigma Mirada Crosstour SLE", "brand": "Sigma", "category": "Passenger", "tire_size": "235/60R18", "load_index": "107", "speed_rating": "H", "tire_type": "All-Season", "description": "Crossover all-season tire with optimized contact patch for balanced handling and comfort.", "wholesale_price": 78.25, "msrp": 119.99, "stock_quantity": 55, "warehouse": warehouses[1], "dot_code": "1022"},
            {"sku": "SIG-MCSLE-23560R18-PHX", "name": "Sigma Mirada Crosstour SLE", "brand": "Sigma", "category": "Passenger", "tire_size": "235/60R18", "load_index": "107", "speed_rating": "H", "tire_type": "All-Season", "description": "Crossover all-season tire with optimized contact patch for balanced handling and comfort.", "wholesale_price": 78.25, "msrp": 119.99, "stock_quantity": 22, "warehouse": warehouses[3], "dot_code": "3020"},

            # Power King Towmax STR II ST225/75R15 — original is Fresh in Dallas (DOT 3025)
            {"sku": "PK-TMSTR2-22575R15-CHI", "name": "Power King Towmax STR II", "brand": "Power King", "category": "Trailer & RV", "tire_size": "ST225/75R15", "load_index": "117", "speed_rating": "L", "tire_type": "Highway", "description": "Premium trailer tire with reinforced sidewalls and heat-resistant compound for long highway hauls.", "wholesale_price": 52.00, "msrp": 79.99, "stock_quantity": 120, "warehouse": warehouses[2], "dot_code": "1521"},
            {"sku": "PK-TMSTR2-22575R15-PHX", "name": "Power King Towmax STR II", "brand": "Power King", "category": "Trailer & RV", "tire_size": "ST225/75R15", "load_index": "117", "speed_rating": "L", "tire_type": "Highway", "description": "Premium trailer tire with reinforced sidewalls and heat-resistant compound for long highway hauls.", "wholesale_price": 52.00, "msrp": 79.99, "stock_quantity": 30, "warehouse": warehouses[3], "dot_code": "0819"},

            # Eldorado ZR Sport 245/40R18 — original is Normal in PBG (DOT 1524)
            {"sku": "ELD-ZRS-24540R18-DAL", "name": "Eldorado ZR Sport", "brand": "Eldorado", "category": "Passenger", "tire_size": "245/40R18", "load_index": "97", "speed_rating": "W", "tire_type": "Performance", "description": "Max-performance tire with aggressive tread pattern for sport cars and coupes. Excellent dry grip.", "wholesale_price": 95.00, "msrp": 144.99, "stock_quantity": 28, "warehouse": warehouses[1], "dot_code": "2021"},
            {"sku": "ELD-ZRS-24540R18-CHI", "name": "Eldorado ZR Sport", "brand": "Eldorado", "category": "Passenger", "tire_size": "245/40R18", "load_index": "97", "speed_rating": "W", "tire_type": "Performance", "description": "Max-performance tire with aggressive tread pattern for sport cars and coupes. Excellent dry grip.", "wholesale_price": 95.00, "msrp": 144.99, "stock_quantity": 16, "warehouse": warehouses[2], "dot_code": "4518"},
        ]

        all_products = products_data + fefo_duplicates

        for pd in all_products:
            product = Product(
                sku=pd["sku"],
                name=pd["name"],
                brand_id=brands[pd["brand"]],
                category_id=categories[pd["category"]],
                tire_size=pd["tire_size"],
                load_index=pd["load_index"],
                speed_rating=pd["speed_rating"],
                tire_type=pd["tire_type"],
                description=pd["description"],
                wholesale_price=pd["wholesale_price"],
                msrp=pd["msrp"],
                stock_quantity=pd["stock_quantity"],
                warehouse_location=pd["warehouse"],
                dot_code=pd["dot_code"],
                manufacture_date=dot_to_date(pd["dot_code"]),
                image_url=f"https://via.placeholder.com/400x400.png?text={pd['sku']}",
                is_active=True,
            )
            db.add(product)

        db.commit()
        print(f"Seeded {len(brands_data)} brands, {len(categories_data)} categories, {len(all_products)} products ({len(fefo_duplicates)} FEFO duplicates).")

    except Exception as e:
        db.rollback()
        print(f"Seed error: {e}")
        raise
    finally:
        db.close()
