# =============================
# HITUNG BMR (Mifflin-St Jeor)
# =============================


def hitung_bmr(jenis_kelamin, berat, tinggi, usia):
    """
    jenis_kelamin: 'laki-laki' / 'perempuan'
    berat: kg
    tinggi: cm
    usia: tahun
    """

    if jenis_kelamin.lower() == "laki-laki":
        bmr = (10 * berat) + (6.25 * tinggi) - (5 * usia) + 5
    elif jenis_kelamin.lower() == "perempuan":
        bmr = (10 * berat) + (6.25 * tinggi) - (5 * usia) - 161
    else:
        raise ValueError("Jenis kelamin tidak valid")

    return bmr


# =============================
# PAL (Physical Activity Level)
# =============================


def get_pal(aktivitas):
    """
    aktivitas:
    - sedentary
    - active
    - vigorous
    """

    aktivitas = aktivitas.lower()

    if aktivitas == "sedentary":
        return 1.40
    elif aktivitas == "active":
        return 1.84
    elif aktivitas == "vigorous":
        return 2.20
    else:
        raise ValueError("Aktivitas tidak valid")


# =============================
# HITUNG TEE
# =============================


def hitung_tee(bmr, aktivitas):
    pal = get_pal(aktivitas)
    tee = bmr * pal
    return tee


# =============================
# FUNGSI UTAMA (ALL-IN-ONE)
# =============================


def hitung_kebutuhan_energi(user):
    """
    user: dict dari database
    """

    bmr = hitung_bmr(
        user["jenis_kelamin"], user["berat_badan"], user["tinggi_badan"], user["usia"]
    )

    tee = hitung_tee(bmr, user["aktivitas_harian"])

    return {"bmr": round(bmr, 2), "tee": round(tee, 2)}
