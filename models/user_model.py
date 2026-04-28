from config.supabase import supabase

# =============================
# INSERT USER
# =============================
def insert_user(data):
    return supabase.table("pengguna").insert(data).execute()


# =============================
# AMBIL USER BERDASARKAN USERNAME
# =============================
def get_user_by_username(username):
    response = supabase.table("pengguna") \
        .select("*") \
        .eq("username", username) \
        .execute()

    return response.data


# =============================
# UPDATE DATA PENGGUNA
# =============================
def update_user(username, data):
    return supabase.table("pengguna") \
        .update(data) \
        .eq("username", username) \
        .execute()