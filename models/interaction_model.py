from config.supabase import supabase


def insert_user_interaction(data):
    return supabase.table("user_interaksi").insert(data).execute()


def get_user_interaction(user_id, makanan_id, session_id):
    response = supabase.table("user_interaksi").select("*").eq("user_id", user_id).eq("makanan_id", makanan_id).eq("session_id", session_id).execute()
    return response.data
