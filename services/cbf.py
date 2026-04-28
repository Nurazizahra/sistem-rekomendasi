from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =============================
# PREPROCESS QUERY SAJA
# =============================
def preprocess_query(text):
    text = text.lower()

    stopwords = [
        "dan", "yang", "dengan", "untuk", "di", "ke", "dari",
        "atau", "ini", "itu", "adalah"
    ]

    words = text.split()
    words = [w for w in words if w not in stopwords]

    return " ".join(words)


# =============================
# CBF RANKING
# =============================
def cbf_ranking(query, data_makanan, top_n=5):

    # =============================
    # VALIDASI
    # =============================
    if not data_makanan:
        return []

    # =============================
    # PREPROCESS QUERY
    # =============================
    query = preprocess_query(query)

    # =============================
    # AMBIL DOKUMEN (hindari kosong)
    # =============================
    dokumen_list = [
        m.get("dokumen", "") or "" for m in data_makanan
    ]

    # tambahkan query
    dokumen_list.append(query)

    # =============================
    # TF-IDF + BIGRAM
    # =============================
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(dokumen_list)

    # =============================
    # COSINE SIMILARITY
    # =============================
    similarity = cosine_similarity(
        tfidf_matrix[-1], tfidf_matrix[:-1]
    ).flatten()

    # =============================
    # GABUNGKAN HASIL
    # =============================
    hasil = []
    for i, m in enumerate(data_makanan):
        m_copy = m.copy()
        m_copy["similarity"] = float(similarity[i])
        hasil.append(m_copy)

    # =============================
    # SORTING
    # =============================
    hasil = sorted(
        hasil,
        key=lambda x: x["similarity"],
        reverse=True
    )

    # =============================
    # FILTER NILAI 0 (opsional)
    # =============================
    hasil = [m for m in hasil if m["similarity"] > 0]

    # =============================
    # TOP N
    # =============================
    return hasil[:top_n]