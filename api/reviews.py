from flask import jsonify
from . import api_bp
from models import Review


@api_bp.get("/reviews")
def get_reviews():
    reviews = Review.query.all()
    return jsonify(
        [
            {
                "id": r.id,
                "nursery_id": r.nursery_id,
                "name": r.reviewer_name,
                "rating": r.rating,
                "comment": r.comment,
            }
            for r in reviews
        ]
    )
