from dotenv import load_dotenv
load_dotenv()

from services.cbf import cbf_ranking
from models.food_model import get_all_makanan

# ====================================
# DATA PENGUJIAN
# ====================================
test_queries = [

    {
        "query": "ayam goreng",
        "relevant": [
            "Ayam Goreng Bumbu Kuning",
            "Ayam Geprek Rendah Kalori"
        ]
    },

    {
        "query": "ayam",
        "relevant": [
            "Ayam Rica Rica",
            "Dada Ayam Suwir",
            "Sup Ayam",
            "Ayam Goreng Bumbu Kuning",
            "Tumis Timun dan Ayam",
            "Salad Sayur dengan Ayam, Tahu, dan Tempe",
            "Rebusan Ayam Saus Tiram",
            "Ayam Teriyaki",
            "Ramen Ayam Shirataki",
            "Sate Campur Ayam dan Jamur"
        ]
    },

    {
        "query": "nasi goreng",
        "relevant": [
            "Nasi Goreng Sayuran",
            "Nasi Goreng Mentega",
            "Nasi Goreng Receh",
            "Nasi Goreng China",
            "Nasi Goreng Spesial",
            "Nasi Goreng Ayam"
        ]
    },
    
    {
        "query": "mi goreng",
        "relevant": [
            "Mi Shirataki Goreng"
        ]
    },

    {
        "query": "mi",
        "relevant": [
            "Mi Shirataki Goreng",
            "Mi Shirataki Soto",
            "Mie Keju",
            "Ayam Teriyaki & Mi Soba",
            "Carbonara Ayam dengan Mi Shirataki",
            "Seblak Mi Shirataki",
            "Mi Shirataki",
            "Sup Mi Ayam",
            "Sup Mi Udang",
            "Mi Angel Hair dengan Udang"
        ]
    },

    {
        "query": "soto ayam",
        "relevant": [
            "Soto Ayam",
            "Mi Shirataki Soto"
        ]
    },

    {
        "query": "bakso",
        "relevant": [
            "Bakso Ayam Oat",
            "Bakso Lohoa",
            "Bakso Tempe",
            "Bakso Daging Keju",
            "Sup Bakso Ikan",
            "Tumis Udang dan Bakso",
            "Bakso Kentang Fettuccine"
        ]
    },

    {
        "query": "ikan",
        "relevant": [
            "Ikan Tongkol Asam Pedas",
            "Ikan Kukus",
            "Stim Ikan Ala Chinese",
            "Sup Ikan Brodetto",
            "Sup Bakso Ikan",
            "Sup Ikan Kod dengan Sayuran dan Bijian",
            "Tumis Tahu dan Tuna"
        ]
    },
    
    {
        "query": "bubur ayam",
        "relevant": [
            "Bubur Ayam Oat",
            "Bubur Ayam Merah",
            "Bubur Ayam Oatmeal",
            "Bubur Oat"
        ]
    },

    {
        "query": "telur",
        "relevant": [
            "Telur Dadar Sayur",
            "Tahu Goreng Telur",
            "Telur Isi Barat Daya",
            "Telur Orak-Arik",
            "Salad Telur",
            "Sup Telur",
            "Omelet Putih Telur",
            "Sandwich Telur Dadar",
            "Tumis Telur Tahu",
            "Sup Tofu Telur"
        ]
    },

    {
        "query": "telur dadar",
        "relevant": [
            "Telur Dadar Sayur",
            "Sandwich Telur Dadar",
            "Telur Dadar"
        ]
    },

    {
        "query": "omelet",
        "relevant": [
            "Omelet Tahu Telur",
            "Bubur Oat Goreng dan Omelet",
            "Omelet Bayam",
            "Mini Omelet Panggang",
            "Omelet Jamur Bayam",
            "Omelet Tuna",
            "Omelet Putih Telur",
            "Gigitan Omelet"
        ]
    },

    {
        "query": "sup sayur",
        "relevant": [
            "Sup Sayuran dengan Sosis",
            "Sup Sayuran dengan Pesto",
            "Sup Tomat",
            "Sup Brokoli Arugula",
            "Hati Ayam Panggang dalam Sup Sayuran",
            "Sup Sayuran Kebun",
            "Sup Kale dan Leek"
        ]
    },
    
    {
        "query": "sup daging",
        "relevant": [
            "Sup Daging Selada Air",
            "Sup Daging Tahu",
            "Sup Daging Sapi dengan Kacang Panjang"
        ]
    },

    {
        "query": "tumis sayur",
        "relevant": [
            "Tumis Sayuran",
            "Ayam Tumis Sayuran",
            "Tumis Sayur dengan Telur",
            "Tumis Sayuran dengan Ayam",
            "Tumis Bunga Kol dan Daging Sapi",
            "Tumis Kol",
            "Tumis Brokoli"
        ]
    },

    {
        "query": "daging sapi",
        "relevant": [
            "Souvlaki Daging Sapi",
            "Segitiga Kentang dan Daging Sapi",
            "Daging Sapi dan Brokoli",
            "Tumis Bunga Kol dan Daging Sapi",
            "Stroganoff Daging Sapi",
            "Sandwich Daging Sapi Panggang",
            "Gulungan Salad Daging Sapi Asap",
            "Bowl Burrito"
        ]
    },

    {
        "query": "salad",
        "relevant": [
            "Salad Kol",
            "Salad Kale dan Brussel Sprout",
            "Salad Kol yang Mudah",
            "Salad Selada Nanas Tomat Cerry",
            "Salad Salmon Cobb",
            "Salad Hijau Campur dengan Keju",
            "Salad Kol Brokoli dan Bacon",
            "Salad Sayur",
            "Bungkus Salad Ayam",
            "Salad Sayur dengan Ayam, Tahu, dan Tempe"
        ]
    },

    {
        "query": "tempe",
        "relevant": [
            "Tempe Goreng",
            "Bakso Tempe",
            "Tempe Tahu Orek",
            "Ayam Tempe Penyet",
            "Tempe Teriyaki",
            "Tempe Kecap",
            "Tumis Ayam Jamur Tempe",
            "Steak Tempe",
            "Oseng Buncis Tempe",
            "Salad Sayur dengan Ayam, Tahu, dan Tempe"
        ]
    },
    
    {
        "query": "tahu",
        "relevant": [
            "Tahu Kuping",
            "Tahu Gejrot Cirebon",
            "Tahu Lumpia",
            "Tahu Telur",
            "Tumis Brokoli Jamur Tahu",
            "Oseng Tauge Tahu Telur",
            "Tahu Goreng Telur",
            "Sup Tahu Wortel",
            "Omelet Tahu Telur",
            "Salad Sayur dengan Ayam, Tahu, dan Tempe"
        ]
    },

    {
        "query": "udang",
        "relevant": [
            "Dimsum Ayam Udang",
            "Pasta Udang Cajun",
            "Salad Udang Bang Bang",
            "Tumis Brokoli Udang",
            "Sawi Isi Ayam Udang",
            "Tumis Udang",
            "Tumis Udang dan Bakso",
            "Bola Ikan Udang Wortel",
            "Udang Nori",
            "Sup Mi Udang"
        ]
    },

    {
        "query": "pancake",
        "relevant": [
            "Pancake Tanpa Gluten",
            "Pancake Blueberry",
            "Kue Pancake",
            "Pancake Pisang Oat",
            "Pancake Rendah Karbohidrat",
            "Pancake Pisang Protein Oat",
            "Pancake Oat",
            "Pancake Keto"
        ]
    },

    {
        "query": "bubur",
        "relevant": [
            "Bubur Oat Pisang",
            "Bubur Beras Nepali",
            "Bubur Manis Oat",
            "Bubur Oat",
            "Bubur Ayam Oat",
            "Bubur Oat Goreng",
            "Bubur Oat Goreng dan Omelet",
            "Bubur Ayam Oatmeal",
            "Bubur Oat dengan Kefir & Buah-Buahan",
            "Bubur Ayam Merah"
        ]
    },

    {
        "query": "sayur",
        "relevant": [
            "Campuran Sayuran",
            "Fajitas Air Fryer",
            "Tumis Kacang Panjang dan Tauge",
            "Tumis Sayuran",
            "Sayur Bayam Bening",
            "Salad Mentimun dengan Salad Kol",
            "Sup Kale dan Leek",
            "Cah Sayur",
            "Bihun dengan Sayuran",
            "Telur Dadar Sayur"
        ]
    },

    {
        "query": "brownies",
        "relevant": [
            "Brownies Vegan",
            "Brownies Sehat Pisang",
            "Brownies Mocaf",
            "Brownies Fudgy Matcha",
            "Brownies Oatmeal",
            "Brownies Berprotein",
            "Brownies Selai Kacang"
        ]
    },
    
    {
        "query": "menu oat",
        "relevant": [
            "Pancake Oat",
            "Bubur Oat Pisang",
            "Kue Pisang Oat",
            "Pizza Bubur Oat",
            "Bubur Oat",
            "Bubur Ayam Oat",
            "Nasi Goreng Oat",
            "Roti Oat dengan Tomat",
            "Muffin Oat Pisang Sehat",
            "Brownies Oatmeal"
        ]
    }
]

# ====================================
# THRESHOLD YANG DIUJI
# ====================================
thresholds = [0.1, 0.2, 0.3, 0.4, 0.5]

# ====================================
# AMBIL DATA MAKANAN
# ====================================
data_makanan = get_all_makanan()

# ====================================
# HITUNG PRECISION
# ====================================
for threshold in thresholds:

    total_precision = 0

    print("\n=================================")
    print(f"THRESHOLD : {threshold}")
    print("=================================")

    for test in test_queries:

        query = test["query"]
        relevant_keywords = test["relevant"]

        hasil = cbf_ranking(
            query,
            data_makanan,
            top_n=5,
            threshold=threshold
        )

        if not hasil:
            precision = 0

        else:

            relevant_count = 0

            for item in hasil:

                nama = item["nama_makanan"].lower()

                if any(keyword.lower() in nama for keyword in relevant_keywords):
                    relevant_count += 1

            precision = relevant_count / len(hasil)

        total_precision += precision

        print(f"\nQuery : {query}")
        print(f"Precision : {precision:.2f}")

    average_precision = total_precision / len(test_queries)

    print("\n---------------------------------")
    print(f"RATA-RATA PRECISION : {average_precision:.2f}")
    print("---------------------------------")