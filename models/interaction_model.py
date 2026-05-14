from config.supabase import supabase

# =============================
# INSERT INTERACTION USER
# =============================
def insert_user_interaction(data):
    return supabase.table("user_interaksi").insert(data).execute()

# =============================
# AMBIL SEMUA INTERACTION USER
# DALAM 1 SESSION
# =============================
def get_user_interactions_by_session(user_id, session_id):

    response = supabase.table("user_interaksi") \
        .select("makanan_id") \
        .eq("user_id", user_id) \
        .eq("session_id", session_id) \
        .execute()

    return response.data

# =============================
# AMBIL SEMUA INTERAKSI
# UNTUK EVALUASI
# =============================
def get_all_user_interactions():

    response = (
        supabase
        .table("user_interaksi")
        .select("*")
        .order("created_at")
        .execute()
    )

    return response.data