# =============================
# RULE-BASED FILTERING
# =============================

def filter_makanan_rule_based(data_makanan, user, target_min, target_max, porsi_input):
    """
    data_makanan : list of dict (dari database makanan)
    user         : dict (data user dari database)
    target_min   : float
    target_max   : float
    porsi_input  : string ("1" atau "lebih")
    """

    hasil = []

    # =============================
    # 1. FILTER ALERGI
    # =============================
    alergi_user = user.get("alergi")

    if alergi_user:
        alergi_list = alergi_user.lower().split(",")
        alergi_list = [a.strip() for a in alergi_list]

        data_after_alergi = []

        for makanan in data_makanan:
            bahan = makanan.get("bahan", "").lower()

            # cek apakah ada alergi di bahan
            if any(alergi in bahan for alergi in alergi_list):
                continue  # buang makanan

            data_after_alergi.append(makanan)

    else:
        # jika tidak ada alergi → skip
        data_after_alergi = data_makanan

    # =============================
    # 2. FILTER PORSI
    # =============================
    data_after_porsi = []

    for makanan in data_after_alergi:
        porsi_makanan = makanan.get("porsi", 1)

        if porsi_input == "1":
            if porsi_makanan == 1:
                data_after_porsi.append(makanan)

        elif porsi_input == "lebih":
            if porsi_makanan > 1:
                data_after_porsi.append(makanan)

        else:
            # fallback (kalau tidak jelas)
            data_after_porsi.append(makanan)

    # =============================
    # 3. FILTER TARGET KALORI
    # =============================
    data_final = []

    for makanan in data_after_porsi:
        kalori = makanan.get("kalori", 0)

        if target_min <= kalori <= target_max:
            data_final.append(makanan)

    return data_final