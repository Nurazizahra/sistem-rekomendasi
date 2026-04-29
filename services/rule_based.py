def filter_makanan_rule_based(data_makanan, user, target_min, target_max, porsi_input):
    """
    data_makanan : list of dict
    user         : dict
    target_min   : float
    target_max   : float
    porsi_input  : string
    """
    
    # Validasi input
    if not isinstance(data_makanan, list):
        return []
    
    if not isinstance(user, dict):
        return []

    # =============================
    # 1. FILTER ALERGI
    # =============================
    alergi_user = user.get("alergi")

    # Konversi alergi ke list jika masih string
    alergi_list = []
    
    if alergi_user:
        # Jika sudah list
        if isinstance(alergi_user, list):
            alergi_list = [str(a).strip().lower() for a in alergi_user if a]
        # Jika string
        elif isinstance(alergi_user, str):
            alergi_list = [a.strip().lower() for a in alergi_user.split(",") if a.strip()]
        # Konversi ke string dulu jika tipe lain
        else:
            alergi_str = str(alergi_user)
            alergi_list = [a.strip().lower() for a in alergi_str.split(",") if a.strip()]
    
    # Jika tidak ada alergi, return semua data
    if not alergi_list:
        data_after_alergi = data_makanan
    else:
        data_after_alergi = []

        for makanan in data_makanan:
            try:
                # Validasi: pastikan makanan adalah dict
                if not isinstance(makanan, dict):
                    continue
                    
                bahan = makanan.get("bahan", [])
                
                # Pastikan bahan adalah list (sudah di-parse di food_model)
                if not isinstance(bahan, list):
                    bahan = [bahan] if bahan else []

                # Gabung semua bahan menjadi text dan lowercase
                bahan_text = " ".join([str(b) for b in bahan]).lower()

                # Cek apakah ada alergi yang match
                if any(alergi in bahan_text for alergi in alergi_list):
                    continue

                data_after_alergi.append(makanan)
            except Exception:
                continue

    # =============================
    # 2. FILTER PORSI
    # =============================
    data_after_porsi = []

    for makanan in data_after_alergi:
        try:
            if not isinstance(makanan, dict):
                continue
                
            porsi_makanan = makanan.get("porsi", 1)

            if porsi_input == "1":
                if porsi_makanan == 1:
                    data_after_porsi.append(makanan)

            elif porsi_input == "lebih":
                if porsi_makanan > 1:
                    data_after_porsi.append(makanan)

            else:
                data_after_porsi.append(makanan)
        except Exception:
            continue

    # =============================
    # 3. FILTER KALORI
    # =============================
    data_final = []

    for makanan in data_after_porsi:
        try:
            if not isinstance(makanan, dict):
                continue
                    
            kalori = makanan.get("kalori", 0)

            try:
                kalori = float(kalori)
            except:
                kalori = 0

            if target_min <= kalori <= target_max:
                data_final.append(makanan)
                
        except Exception:
            continue

    return data_final