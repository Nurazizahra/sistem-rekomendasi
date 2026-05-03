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
        response = (
            supabase.table("makanan_coba")
            .select("*")
            .order("id")
            .range(offset, offset + limit - 1)
            .execute()
        )

        data = response.data

        if not data:
            break

        # parsing semua bahan - bahan adalah JSON string array
        for item in data:
            # Validasi: item harus dict
            if not isinstance(item, dict):
                print(f"WARNING: item bukan dict, tipe: {type(item)}, skip item")
                continue

            try:
                bahan_raw = item.get("bahan")

                # Kasus 1: bahan adalah string JSON array
                if isinstance(bahan_raw, str):
                    try:
                        item["bahan"] = json.loads(bahan_raw)
                    except:
                        # Jika parse gagal, wrap string dalam list
                        item["bahan"] = [bahan_raw]

                # Kasus 2: bahan sudah list
                elif isinstance(bahan_raw, list):
                    item["bahan"] = bahan_raw

                # Kasus 3: bahan null atau tidak ada
                else:
                    item["bahan"] = []

            except Exception as e:
                print(f"Error parsing bahan untuk item {item.get('id')}: {e}")
                item["bahan"] = []

        # Filter hanya dict items
        valid_data = [item for item in data if isinstance(item, dict)]
        semua_data.extend(valid_data)
        offset += limit

    return semua_data


# =============================
# AMBIL MAKANAN BERDASARKAN ID
# =============================
def get_makanan_by_id(id):

    response = supabase.table("makanan_coba").select("*").eq("id", id).execute()

    data = response.data

    if data:
        import json

        try:
            bahan_raw = data[0].get("bahan")

            # Kasus 1: bahan adalah string JSON array
            if isinstance(bahan_raw, str):
                try:
                    data[0]["bahan"] = json.loads(bahan_raw)
                except:
                    # Jika parse gagal, wrap string dalam list
                    data[0]["bahan"] = [bahan_raw]

            # Kasus 2: bahan sudah list
            elif isinstance(bahan_raw, list):
                data[0]["bahan"] = bahan_raw

            # Kasus 3: bahan null atau tidak ada
            else:
                data[0]["bahan"] = []

        except Exception as e:
            print(f"Error parsing bahan: {e}")
            data[0]["bahan"] = []

    return data
