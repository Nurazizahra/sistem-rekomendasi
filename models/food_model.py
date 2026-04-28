from config.supabase import supabase

# =============================
# AMBIL SEMUA DATA MAKANAN
# =============================
def get_all_makanan():

    semua_data = []
    limit = 200
    offset = 0

    import json

    while True:
        response = supabase.table("makanan") \
            .select("*") \
            .order("id") \
            .range(offset, offset + limit - 1) \
            .execute()

        data = response.data

        if not data:
            break

        # 🔥 parsing semua bahan
        for item in data:
            try:
                item["bahan"] = json.loads(item["bahan"])
            except:
                item["bahan"] = [item["bahan"]]

        semua_data.extend(data)
        offset += limit

    return semua_data


# =============================
# AMBIL MAKANAN BERDASARKAN ID
# =============================
def get_makanan_by_id(id):

    response = supabase.table("makanan") \
        .select("*") \
        .eq("id", id) \
        .execute()

    data = response.data

    if data:
        import json

        try:
            data[0]["bahan"] = json.loads(data[0]["bahan"])
        except:
            data[0]["bahan"] = [data[0]["bahan"]]

    return data
