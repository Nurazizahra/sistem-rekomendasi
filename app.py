from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import insert_user, get_user_by_username, update_user
from services.kalori import hitung_kebutuhan_energi
from services.rule_based import filter_makanan_rule_based
from models.food_model import get_all_makanan
from models.food_model import get_makanan_by_id
from services.cbf import cbf_ranking

app = Flask(__name__)
app.secret_key = "secret123"  # wajib untuk session


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
            "password": hashed_password
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

    username = session.get("username")

    if not username:
        return redirect(url_for("login"))

    user_data = get_user_by_username(username)

    if not user_data:
        return redirect(url_for("login"))

    user = user_data[0]

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
        min_kalori = float(min_kalori)
        max_kalori = float(max_kalori)

        target_min = (min_kalori / 100) * tee
        target_max = (max_kalori / 100) * tee

        # =============================
        # SIMPAN KE SESSION
        # =============================
        session["query"] = query
        session["target_min"] = target_min
        session["target_max"] = target_max
        session["porsi"] = porsi

        return redirect(url_for("search"))

    # =============================
    # TAMPILKAN HOME (TEE TETAP ADA)
    # =============================
    return render_template("home.html", user=user, tee=tee)

# =============================
# SEARCH RESULT
# =============================
@app.route("/search")
def search():

    # =============================
    # CEK LOGIN
    # =============================
    username = session.get("username")

    if not username:
        return redirect(url_for("login"))

    user_data = get_user_by_username(username)

    if not user_data:
        return redirect(url_for("login"))

    user = user_data[0]

    # =============================
    # AMBIL DATA DARI SESSION
    # =============================
    target_min = session.get("target_min")
    target_max = session.get("target_max")
    query = session.get("query")
    porsi = session.get("porsi")

    # validasi sederhana
    if not query:
        return redirect(url_for("home"))

    # =============================
    # AMBIL DATA MAKANAN
    # =============================
    data_makanan = get_all_makanan()

    # =============================
    # RULE-BASED FILTERING
    # =============================
    filtered = filter_makanan_rule_based(
        data_makanan,
        user,
        target_min,
        target_max,
        porsi
    )

    # =============================
    # PREPROCESS QUERY (MINIMAL)
    # =============================
    query_clean = query.lower().replace("-", " ").strip()

    # =============================
    # CBF RANKING
    # =============================
    if filtered:
        hasil = cbf_ranking(query_clean, filtered, top_n=5)
    else:
        hasil = []

    # =============================
    # DEBUG (opsional)
    # =============================
    print("Query:", query_clean)
    print("Jumlah setelah rule-based:", len(filtered))
    print("Jumlah hasil akhir:", len(hasil))

    # =============================
    # RENDER
    # =============================
    return render_template(
        "search.html",
        user=user,
        query=query,
        target_min=target_min,
        target_max=target_max,
        porsi=porsi,
        hasil=hasil
    )

# =============================
# DETAIL FOOD
# =============================
@app.route("/detail/<int:id>")
def detail(id):

    username = session.get("username")

    if not username:
        return redirect(url_for("login"))

    # ambil user (buat header)
    user_data = get_user_by_username(username)

    if not user_data:
        return redirect(url_for("login"))

    user = user_data[0]

    # ambil data makanan
    data = get_makanan_by_id(id)

    if not data:
        return "Makanan tidak ditemukan"

    makanan = data[0]

    return render_template("detail.html", user=user, makanan=makanan)

# =============================
# PROFILE EDIT
# =============================
@app.route("/profile", methods=["GET", "POST"])
def profile():

    username = session.get("username")

    if not username:
        return redirect(url_for("login"))

    user_data = get_user_by_username(username)

    if not user_data:
        return redirect(url_for("login"))

    user = user_data[0]

    message = None
    message_type = None

    if request.method == "POST":

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
                return render_template("profile.html", user=user, message=message, message_type=message_type)

        # cek konfirmasi password
        if new_password or confirm_password:
            if new_password != confirm_password:
                message = "Konfirmasi password tidak cocok"
                message_type = "error"
                return render_template("profile.html", user=user, message=message, message_type=message_type)

        # data update
        update_data = {
            "usia": usia,
            "berat_badan": berat,
            "tinggi_badan": tinggi,
            "aktivitas_harian": aktivitas,
            "alergi": alergi
        }

        # update password jika ada
        if new_password:
            hashed_password = generate_password_hash(new_password)
            update_data["password"] = hashed_password

        update_user(username, update_data)

        message = "Data berhasil diperbarui"
        message_type = "success"

        # ambil ulang data
        user_data = get_user_by_username(username)
        user = user_data[0]

    return render_template("profile.html", user=user, message=message, message_type=message_type)


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
    app.run(debug=True)