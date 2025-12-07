from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ==========================
# نموذج المستخدم (للتسجيل الحقيقي)
# ==========================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    # اسم المستخدم لعملية الدخول
    username = db.Column(db.String(80), unique=True, nullable=False)

    # إيميل المستخدم
    email = db.Column(db.String(120), unique=True, nullable=False)

    # الاسم الكامل (اختياري يظهر في البروفايل)
    full_name = db.Column(db.String(120), nullable=True)

    # رقم الهاتف (اختياري)
    phone = db.Column(db.String(30), nullable=True)

    # عنوان المستخدم (اختياري)
    address = db.Column(db.String(255), nullable=True)

    # رابط صورة (اختياري) – صورة البروفايل
    avatar_url = db.Column(db.String(255), nullable=True)

    # كلمة المرور بعد التشفير
    password_hash = db.Column(db.String(255), nullable=False)

    # عملة مفضّلة لعرض الأسعار (EUR / USD / AED ...)
    preferred_currency = db.Column(db.String(3), default="EUR")

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    # ربط مراجعات الأهالي بالمستخدم (اختياري)
    reviews = db.relationship("Review", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.username!r}>"


# ==========================
# نموذج الحضانة
# ==========================
class Nursery(db.Model):
    __tablename__ = "nurseries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    reviews_count = db.Column(db.Integer, nullable=False)

    # نخزن القوائم كـ string مفصولة بفواصل أو رموز
    curriculum = db.Column(db.String(200), nullable=False)      # "Montessori,International"
    features = db.Column(db.String(400), nullable=False)        # "Outdoor Garden,Art Studio,Music Classes"

    # السعر الأساسي
    price = db.Column(db.Integer, nullable=False)               # مثلاً 850

    # كود العملة (EUR / USD / AED ...)
    currency = db.Column(db.String(3), nullable=False, default="EUR")

    phone = db.Column(db.String(50), nullable=False)

    capacity = db.Column(db.Integer, nullable=False)
    age_groups = db.Column(db.String(100), nullable=False)      # "6 months - 6 years"
    total_children = db.Column(db.Integer, nullable=False)
    staff_ratio = db.Column(db.String(20), nullable=False)      # "1:4"

    parent_satisfaction = db.Column(db.Integer, nullable=False) # 96
    teacher_quality = db.Column(db.Integer, nullable=False)
    facilities_rating = db.Column(db.Integer, nullable=False)
    safety_rating = db.Column(db.Integer, nullable=False)

    description = db.Column(db.Text, nullable=False)

    # رابط جوجل مابس لموقع الحضانة
    google_maps_url = db.Column(db.String(300), nullable=True)

    reviews = db.relationship("Review", backref="nursery", lazy=True)

    def __repr__(self):
        return f"<Nursery {self.name!r}>"


# ==========================
# نموذج مراجعات الأهالي
# ==========================
class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    nursery_id = db.Column(db.Integer, db.ForeignKey("nurseries.id"), nullable=False)

    # ربط اختياري بالمستخدم (لو المراجعة مسجلة باسم يوزر)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    reviewer_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Review {self.reviewer_name!r} ⭐{self.rating}>"
