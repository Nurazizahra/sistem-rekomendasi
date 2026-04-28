from config.supabase import get_supabase
import json


# =============================
# AMBIL SEMUA DATA MAKANAN (LIMIT)
# =============================
def get_all_makanan():
    supabase = get_supabase()

    response = supabase.table("makanan") \
        .select("*") \
        .limit(50) \
        .execute()

    data = response.data

    for item in data:
        try:
            item["bahan"] = json.loads(item["bahan"])
        except:
            item["bahan"] = [item["bahan"]]

    return data


# =============================
# AMBIL MAKANAN BERDASARKAN ID
# =============================
def get_makanan_by_id(id):
    supabase = get_supabase()

    response = supabase.table("makanan") \
        .select("*") \
        .eq("id", id) \
        .limit(1) \
        .execute()

    data = response.data

    if data:
        try:
            data[0]["bahan"] = json.loads(data[0]["bahan"])
        except:
            data[0]["bahan"] = [data[0]["bahan"]]

    return data