from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, Nursery, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///nurseries.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "dev-secret-key"

db.init_app(app)


# -----------------------------
# اللغة الحالية
# -----------------------------
def get_lang():
    lang = request.args.get("lang")
    if lang not in ("en", "de", "ar"):
        lang = session.get("lang", "en")
    session["lang"] = lang
    return lang


@app.context_processor
def inject_lang():
    return {
        "current_lang": session.get("lang", "en"),
        "current_user_name": session.get("user_name"),
        "current_currency": session.get("currency", "EUR"),
    }


# -----------------------------
# الراوت الرئيسي → اللوجين
# -----------------------------
@app.route("/")
def home():
    return redirect(url_for("login_page"))


# -----------------------------
# صفحة تسجيل الدخول (GET)
# -----------------------------
@app.route("/login", methods=["GET"])
def login_page():
    lang = get_lang()

    error = session.pop("login_error", None)
    saved_identifier = session.get("remembered_identifier", "")
    saved_remember = session.get("remember_me_checked", False)

    return render_template(
        "login.html",
        lang=lang,
        error=error,
        saved_username=saved_identifier,  # ممكن يكون يوزر أو إيميل
        saved_remember=saved_remember,
    )


# -----------------------------
# معالجة تسجيل الدخول (POST)
# -----------------------------
@app.route("/login", methods=["POST"])
def login_post():
    lang = get_lang()

    # ممكن يكون Username أو Email في نفس الخانة
    identifier = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    remember = "remember_me" in request.form

    if not identifier or not password:
        session["login_error"] = "Invalid username, email or password."
        return redirect(url_for("login_page", lang=lang))

    # نبحث باليوزرنيم أو الإيميل
    user = User.query.filter(
        or_(User.username == identifier, User.email == identifier)
    ).first()

    if user and check_password_hash(user.password_hash, password):
        # نجاح
        session["user_id"] = user.id
        session["user_name"] = user.username
        session["currency"] = user.preferred_currency or "EUR"

        session["remember_me_checked"] = remember
        if remember:
            session["remembered_identifier"] = identifier
        else:
            session.pop("remembered_identifier", None)

        return redirect(url_for("nurseries_page", lang=lang))
    else:
        session["login_error"] = "Invalid username, email or password."
        return redirect(url_for("login_page", lang=lang))


# -----------------------------
# Forgot password (بسيطة مؤقتاً)
# -----------------------------
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    lang = get_lang()
    message = None

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        if email:
            message = "If this email exists, we have sent password reset instructions."

    return render_template("forgot_password.html", lang=lang, message=message)


# -----------------------------
# Sign up حقيقي
# -----------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    lang = get_lang()
    error = None
    success = False

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        confirm = request.form.get("confirm_password", "").strip()

        # تحقق بسيط
        if not username or not email or not password:
            error = "All fields are required."
        elif password != confirm:
            error = "Passwords do not match."
        elif len(password) < 6:
            error = "Password must be at least 6 characters."
        else:
            # تأكد ما فيش يوزر أو إيميل مكرر
            existing = User.query.filter(
                or_(User.username == username, User.email == email)
            ).first()
            if existing:
                error = "Username or email already exists."
            else:
                # إنشاء المستخدم
                hashed = generate_password_hash(password)
                user = User(
                    username=username,
                    email=email,
                    password_hash=hashed,
                    preferred_currency="EUR",
                )
                db.session.add(user)
                db.session.commit()
                success = True

    return render_template("signup.html", lang=lang, error=error, success=success)


# -----------------------------
# تسجيل الخروج
# -----------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))


# -----------------------------
# صفحة الحضانات بعد تسجيل الدخول
# -----------------------------
@app.route("/nurseries")
def nurseries_page():
    lang = get_lang()

    if "user_id" not in session:
        return redirect(url_for("login_page", lang=lang))

    nurseries = Nursery.query.order_by(Nursery.rating.desc()).all()

    search_query = request.args.get("q", "", type=str).strip()
    curriculum_filter = request.args.get("curriculum", "", type=str).strip()
    sort_by = request.args.get("sort", "rating", type=str)

    if search_query:
        q = search_query.lower()
        nurseries = [
            n
            for n in nurseries
            if q in n.name.lower()
            or (n.location and q in n.location.lower())
        ]

    if curriculum_filter and curriculum_filter != "All":
        nurseries = [
            n
            for n in nurseries
            if n.curriculum and curriculum_filter in n.curriculum
        ]

    if sort_by == "name":
        nurseries = sorted(nurseries, key=lambda n: n.name)
    elif sort_by == "price_low":
        nurseries = sorted(nurseries, key=lambda n: n.price)
    elif sort_by == "price_high":
        nurseries = sorted(nurseries, key=lambda n: n.price, reverse=True)
    else:
        nurseries = sorted(nurseries, key=lambda n: n.rating, reverse=True)

    return render_template(
        "index.html",
        lang=lang,
        nurseries=nurseries,
        search_query=search_query,
        curriculum_filter=curriculum_filter,
        sort_by=sort_by,
    )


# -----------------------------
# صفحة تفاصيل الحضانة
# -----------------------------
@app.route("/nursery/<int:nursery_id>")
def nursery_detail(nursery_id):
    lang = get_lang()

    if "user_id" not in session:
        return redirect(url_for("login_page", lang=lang))

    nursery = Nursery.query.get_or_404(nursery_id)

    return render_template(
        "nursery_detail.html",
        lang=lang,
        nursery=nursery,
    )


# -----------------------------
# صفحة البروفايل (عرض + تعديل)
# -----------------------------
@app.route("/profile", methods=["GET", "POST"])
def profile():
    lang = get_lang()

    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login_page", lang=lang))

    user = User.query.get_or_404(user_id)
    error = None
    success = False

    if request.method == "POST":
        # حقول البروفايل
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        full_name = request.form.get("full_name", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        avatar_url = request.form.get("avatar_url", "").strip()
        preferred_currency = request.form.get("preferred_currency", "").strip() or "EUR"

        # تحقق مبدئي
        if not username or not email:
            error = "Username and email are required."
        else:
            # تأكد أن اليوزرنيم / الإيميل مش مكرر عند مستخدم آخر
            existing = User.query.filter(
                or_(User.username == username, User.email == email)
            ).filter(User.id != user.id).first()

            if existing:
                error = "Username or email is already taken by another user."
            else:
                user.username = username
                user.email = email
                user.full_name = full_name or None
                user.phone = phone or None
                user.address = address or None
                user.avatar_url = avatar_url or None

                if preferred_currency in ("EUR", "USD", "AED"):
                    user.preferred_currency = preferred_currency
                    session["currency"] = preferred_currency

                # حدّث اسم المستخدم في السيشن
                session["user_name"] = user.username

                db.session.commit()
                success = True

    return render_template(
        "profile.html",
        lang=lang,
        user=user,
        error=error,
        success=success,
    )


# -----------------------------
# API صغيرة لتغيير العملة (AJAX)
# -----------------------------
@app.route("/set-currency", methods=["POST"])
def set_currency():
    if "user_id" not in session:
        return jsonify({"ok": False, "error": "not_authenticated"}), 401

    data = request.get_json(silent=True) or {}
    currency = (data.get("currency") or "").upper()

    if currency not in ("EUR", "USD", "AED"):
        return jsonify({"ok": False, "error": "invalid_currency"}), 400

    session["currency"] = currency

    user = User.query.get(session["user_id"])
    if user:
        user.preferred_currency = currency
        db.session.commit()

    return jsonify({"ok": True})


# -----------------------------
# صفحة About Us بسيطة
# -----------------------------
@app.route("/about")
def about():
    lang = get_lang()
    return render_template("about.html", lang=lang)


# -----------------------------
# تشغيل التطبيق
# -----------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
