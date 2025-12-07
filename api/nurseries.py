from flask import request, jsonify
from sqlalchemy import or_
from . import api_bp
from models import db, Nursery


@api_bp.get("/nurseries")
def list_nurseries():
    """إرجاع الحضانات مع إمكانية البحث + الفلترة + الترتيب"""
    q = request.args.get("q", "").strip().lower()
    curriculum = request.args.get("curriculum", "").strip()
    sort = request.args.get("sort", "rating_desc")

    query = Nursery.query

    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                Nursery.name.ilike(like),
                Nursery.city.ilike(like),
                Nursery.country.ilike(like),
            )
        )

    if curriculum:
        query = query.filter(
            (Nursery.curriculum_main == curriculum)
            | (Nursery.curriculum_second == curriculum)
        )

    if sort == "fee_asc":
        query = query.order_by(Nursery.monthly_fee.asc())
    elif sort == "fee_desc":
        query = query.order_by(Nursery.monthly_fee.desc())
    else:
        query = query.order_by(Nursery.rating.desc())

    items = query.all()

    def to_dict(n):
        return {
            "id": n.id,
            "name": n.name,
            "city": n.city,
            "country": n.country,
            "curriculum_main": n.curriculum_main,
            "curriculum_second": n.curriculum_second,
            "rating": n.rating,
            "reviews_count": n.reviews_count,
            "capacity": n.capacity,
            "monthly_fee": n.monthly_fee,
            "features": n.features or "",
        }

    return jsonify([to_dict(n) for n in items])
