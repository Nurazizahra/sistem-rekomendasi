from dotenv import load_dotenv

load_dotenv()
import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import (
    insert_user,
    get_user_by_username,
    get_user_by_id,
    update_user_by_id,
)
from models.interaction_model import insert_user_interaction, get_user_interactions_by_session
from services.kalori import hitung_kebutuhan_energi
from services.rule_based import filter_makanan_rule_based
from models.food_model import get_all_makanan, get_makanan_by_id

app = Flask(__name__)
app.secret_key = "secret123"  # wajib untuk session


def get_current_user():
    
    user_id = session.get("user_id")
    if user_id:
        user_data = get_user_by_id(user_id)
        if user_data:
            return user_data[0]

    username = session.get("username")
    if username:
        user_data = get_user_by_username(username)
        if user_data:
            user = user_data[0]
            if user.get("id"):
                session["user_id"] = user["id"]
            return user

    return None


# =============================
# HALAMAN AWAL → LOGIN
# =============================
@app.route("/")
def index():
    return redirect(url_for("login"))


# =============================
# LOGIN
# =============================
@app.route("/login", methods=["GET", "POST"])
def login():

    message = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user_data = get_user_by_username(username)

        if user_data:
            user = user_data[0]

            if check_password_hash(user["password"], password):
                user_id = user.get("id")
                if user_id:
                    session["user_id"] = user_id
                    session.pop("username", None)
                else:
                    session["username"] = username
                return redirect(url_for("home"))
            else:
                message = "Password salah"
        else:
            message = "User tidak ditemukan"

    return render_template("login.html", message=message)


# =============================
# REGISTER
# =============================
@app.route("/register", methods=["GET", "POST"])
def register():

    message = None
    success = False

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            message = "Konfirmasi password tidak cocok"
            return render_template("register.html", message=message, success=success)

        hashed_password = generate_password_hash(password)

        data = {
            "username": username,
            "usia": int(request.form.get("usia")),
            "jenis_kelamin": request.form.get("jenis_kelamin"),
            "berat_badan": int(request.form.get("berat")),
            "tinggi_badan": int(request.form.get("tinggi")),
            "aktivitas_harian": request.form.get("aktivitas"),
            "alergi": request.form.get("alergi"),
            "password": hashed_password,
        }

        insert_user(data)

        message = "Akun berhasil dibuat"
        success = True

    return render_template("register.html", message=message, success=success)


# =============================
# HOME
# =============================
@app.route("/home", methods=["GET", "POST"])
def home():

    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    # =============================
    # HITUNG BMR & TEE
    # =============================
    energi = hitung_kebutuhan_energi(user)
    tee = energi["tee"]

    # =============================
    # POST (PENCARIAN)
    # =============================
    if request.method == "POST":

        query = request.form.get("query")
        min_kalori = request.form.get("min_kalori")
        max_kalori = request.form.get("max_kalori")
        porsi = request.form.get("porsi")

        # =============================
        # HITUNG TARGET KALORI
        # =============================
        min_kalori = max(0, min(100, float(min_kalori)))
        max_kalori = max(0, min(100, float(max_kalori)))

        target_min = (min_kalori / 100) * tee
        target_max = (max_kalori / 100) * tee

        # =============================
        # SIMPAN KE SESSION
        # =============================
        session["query"] = query
        session["target_min"] = target_min
        session["target_max"] = target_max
        session["porsi"] = porsi
        session["interaction_session_id"] = str(uuid.uuid4())
        session["interaction_liked"] = False

        return redirect(url_for("search"))

    # =============================
    # TAMPILKAN HOME (TEE TETAP ADA)
    # =============================
    return render_template("home.html", user=user, tee=tee)


# =============================
# SEARCH RESULT
# =============================
@app.route("/search", methods=["GET", "POST"])
def search():
    from services.cbf import cbf_ranking

    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    message = None

    if request.method == "POST":
        makanan_id = request.form.get("makanan_id")

        interaction_session_id = session.get("interaction_session_id")
        if not interaction_session_id:
            interaction_session_id = str(uuid.uuid4())
            session["interaction_session_id"] = interaction_session_id

        # Ambil meta dari session
        search_meta = session.get("detail_search_meta", [])
        detail_meta = next((item for item in search_meta if item.get("id") == int(makanan_id)), None)

        if detail_meta:
            query = detail_meta.get("query", session.get("query", ""))
            rank = detail_meta.get("rank", "")
            similarity = detail_meta.get("similarity", "")
            total_result = detail_meta.get("total_result", "")
        else:
            query = session.get("query", "")
            rank = ""
            similarity = ""
            total_result = ""

        interaction_data = {
            "user_id": user["id"],
            "makanan_id": int(makanan_id),
            "query": query,
            "rank": int(rank) if rank else None,
            "similarity": float(similarity) if similarity else None,
            "total_result": int(total_result) if total_result else None,
            "session_id": interaction_session_id,
        }

        try:
            insert_user_interaction(interaction_data)
            message = "Makanan berhasil dilike!"
        except Exception as e:
            if "duplicate key value violates unique constraint" in str(e) or "23505" in str(e):
                message = "Makanan ini sudah Anda like."
            else:
                raise

        return redirect(url_for('search'))

    # Cek cache hasil di session
    cached_hasil = session.get("cached_hasil")
    cached_query = session.get("cached_query")
    cached_porsi = session.get("cached_porsi")
    cached_target_min = session.get("cached_target_min")
    cached_target_max = session.get("cached_target_max")
    cached_alergi = session.get("cached_alergi")

    query = session.get("query")
    porsi = session.get("porsi")
    target_min = session.get("target_min")
    target_max = session.get("target_max")

    current_alergi = user.get("alergi", "")

    try:
        target_min = float(target_min)
        target_max = float(target_max)
    except:
        target_min = 0
        target_max = 9999

    # Jika cache valid (query, porsi, target sama), gunakan cache
    if (
        cached_hasil
        and cached_query == query
        and cached_porsi == porsi
        and cached_target_min == target_min
        and cached_target_max == target_max
        and cached_alergi == current_alergi
    ):
        hasil = cached_hasil
    else:
        # Lakukan processing
        data_makanan = get_all_makanan()
        filtered = filter_makanan_rule_based(data_makanan, user, target_min, target_max, porsi)
        query_clean = query.lower().replace("-", " ").strip()

        if filtered:
            hasil = cbf_ranking(query_clean, filtered, top_n=5)
        else:
            hasil = []

        # Cache hasil
        session["cached_hasil"] = hasil
        session["cached_query"] = query
        session["cached_porsi"] = porsi
        session["cached_target_min"] = target_min
        session["cached_target_max"] = target_max
        session["cached_alergi"] = current_alergi

    search_meta = []
    for idx, item in enumerate(hasil, start=1):
        search_meta.append({
            "id": item.get("id"),
            "query": query,
            "rank": idx,
            "similarity": float(item.get("similarity", 0)),
            "total_result": len(hasil),
        })

        session["detail_search_meta"] = search_meta

    # =============================
    # AMBIL SEMUA LIKE USER
    # DALAM 1 SESSION
    # =============================
    interaction_session_id = session.get("interaction_session_id")

    liked_makanan_ids = set()

    if interaction_session_id:

        all_interactions = get_user_interactions_by_session(
            user["id"],
            interaction_session_id
        )

        liked_makanan_ids = {
            int(i["makanan_id"])
            for i in all_interactions
        }

    # =============================
    # SET STATUS LIKE
    # =============================
    for item in hasil:
        item["is_liked"] = item["id"] in liked_makanan_ids

    return render_template(
    "search.html",
    hasil=hasil,
    query=query,
    message=message,
    user=user,
    target_min=target_min,
    target_max=target_max,
    porsi=porsi
)


# =============================
# DETAIL FOOD
# =============================
@app.route("/detail/<int:id>")
def detail(id):

    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    # ambil data makanan
    data = get_makanan_by_id(id)

    if not data:
        return "Makanan tidak ditemukan"

    makanan = data[0]

    search_meta = session.get("detail_search_meta", [])
    detail_meta = next((item for item in search_meta if item.get("id") == id), None)

    if detail_meta:
        query = detail_meta.get("query", session.get("query", ""))
        rank = detail_meta.get("rank", "")
        similarity = detail_meta.get("similarity", "")
        total_result = detail_meta.get("total_result", "")
    else:
        query = session.get("query", "")
        rank = ""
        similarity = ""
        total_result = ""

    return render_template(
        "detail.html",
        user=user,
        makanan=makanan,
        query=query,
        rank=rank,
        similarity=similarity,
        total_result=total_result,
    )


# =============================
# PROFILE EDIT
# =============================
@app.route("/profile", methods=["GET", "POST"])
def profile():

    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    message = None
    message_type = None

    if request.method == "POST":

        username_input = request.form.get("username")
        usia = int(request.form.get("usia"))
        berat = int(request.form.get("berat"))
        tinggi = int(request.form.get("tinggi"))
        aktivitas = request.form.get("aktivitas")
        alergi = request.form.get("alergi")

        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        # cek password lama
        if old_password:
            if not check_password_hash(user["password"], old_password):
                message = "Password sekarang salah"
                message_type = "error"
                return render_template(
                    "profile.html",
                    user=user,
                    message=message,
                    message_type=message_type,
                )

        # cek konfirmasi password
        if new_password or confirm_password:
            if new_password != confirm_password:
                message = "Konfirmasi password tidak cocok"
                message_type = "error"
                return render_template(
                    "profile.html",
                    user=user,
                    message=message,
                    message_type=message_type,
                )

        # cek username baru
        if username_input and username_input != user["username"]:
            existing_user = get_user_by_username(username_input)
            if existing_user and existing_user[0].get("id") != user.get("id"):
                message = "Username sudah digunakan oleh pengguna lain"
                message_type = "error"
                return render_template(
                    "profile.html",
                    user=user,
                    message=message,
                    message_type=message_type,
                )

        # data update
        update_data = {
            "username": username_input,
            "usia": usia,
            "berat_badan": berat,
            "tinggi_badan": tinggi,
            "aktivitas_harian": aktivitas,
            "alergi": alergi,
        }

        # update password jika ada
        if new_password:
            hashed_password = generate_password_hash(new_password)
            update_data["password"] = hashed_password

        update_user_by_id(user["id"], update_data)

        if session.get("username"):
            session["username"] = username_input

        message = "Data berhasil diperbarui"
        message_type = "success"

        # ambil ulang data
        user_data = get_user_by_id(user["id"])
        user = user_data[0]

    return render_template(
        "profile.html", user=user, message=message, message_type=message_type
    )


# =============================
# LOGOUT
# =============================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# =============================
# RUN
# =============================
if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
