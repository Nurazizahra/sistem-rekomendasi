import os
from supabase import create_client

supabase = None

def get_supabase():
    global supabase

    if supabase is None:
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")

        supabase = create_client(url, key)

    return supabase