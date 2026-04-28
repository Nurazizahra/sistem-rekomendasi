from config.supabase import get_supabase


# =============================
# INSERT USER
# =============================
def insert_user(data):
    supabase = get_supabase()

    return supabase.table("pengguna") \
        .insert(data) \
        .execute()


# =============================
# AMBIL USER BERDASARKAN USERNAME
# =============================
def get_user_by_username(username):
    supabase = get_supabase()

    response = supabase.table("pengguna") \
        .select("*") \
        .eq("username", username) \
        .execute()

    return response.data


# =============================
# UPDATE DATA PENGGUNA
# =============================
def update_user(username, data):
    supabase = get_supabase()

    return supabase.table("pengguna") \
        .update(data) \
        .eq("username", username) \
        .execute()