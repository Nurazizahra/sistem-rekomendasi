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
    response = supabase.table("pengguna").select("*").eq("username", username).execute()

    return response.data


# =============================
# AMBIL USER BERDASARKAN ID
# =============================
def get_user_by_id(user_id):
    response = supabase.table("pengguna").select("*").eq("id", user_id).execute()

    return response.data


# =============================
# UPDATE DATA PENGGUNA BERDASARKAN ID
# =============================
def update_user_by_id(user_id, data):
    return supabase.table("pengguna").update(data).eq("id", user_id).execute()
