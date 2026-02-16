from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Category, Product
from ..schemas import CategoryOut

router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.get("", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    results = (
        db.query(Category, func.count(Product.id).label("product_count"))
        .outerjoin(Product, Product.category_id == Category.id)
        .group_by(Category.id)
        .order_by(Category.name)
        .all()
    )
    return [
        CategoryOut(
            id=cat.id,
            name=cat.name,
            slug=cat.slug,
            description=cat.description,
            product_count=count,
        )
        for cat, count in results
    ]
