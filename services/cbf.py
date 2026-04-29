# =============================
# PREPROCESS QUERY
# =============================
def preprocess_query(text):
    text = text.lower()

    # =============================
    # SYNONYM MAPPING (Normalisasi ke istilah baku)
    # =============================
    synonym_map = {
        "kol": "kol",
        "kubis": "kol",
        "cabe": "cabai",
        "cabé": "cabai",
        "cabai": "cabai",
        "coklat": "cokelat",
        "cokelat": "cokelat",
        "saos": "saus",
        "saus": "saus",
        "telor": "telur",
        "telur": "telur",
        "mie": "mi",
        "mi": "mi",
        "toge": "tauge",
        "taoge": "tauge",
        "tauge": "tauge",
        "kare": "kari",
        "kareh": "kari",
        "karih": "kari",
        "kari": "kari",
    }

    stopwords = [
        "dan",
        "yang",
        "dengan",
        "untuk",
        "di",
        "ke",
        "dari",
        "atau",
        "ini",
        "itu",
        "adalah",
    ]

    words = text.split()

    # Filter stopwords dan normalisasi sinonim
    normalized_words = []
    for w in words:
        if w not in stopwords:
            # Normalisasi sinonim jika ada di mapping
            normalized_word = synonym_map.get(w, w)
            normalized_words.append(normalized_word)

    return " ".join(normalized_words)


# =============================
# CBF RANKING
# =============================
def cbf_ranking(query, data_makanan, top_n=5):

    # lazy import (untuk Railway)
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

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
    # AMBIL DOKUMEN
    # =============================
    dokumen_list = [(m.get("dokumen") or "") for m in data_makanan]

    # tambahkan query di akhir
    dokumen_list.append(query)

    # =============================
    # TF-IDF + BIGRAM
    # =============================
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)

    tfidf_matrix = vectorizer.fit_transform(dokumen_list)

    # =============================
    # COSINE SIMILARITY
    # =============================
    similarity = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

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
    hasil = sorted(hasil, key=lambda x: x["similarity"], reverse=True)

    # =============================
    # FILTER DENGAN THRESHOLD
    # =============================
    threshold = 0.10
    hasil_filtered = [m for m in hasil if m["similarity"] >= threshold]

    # =============================
    # STRATEGI OUTPUT
    # =============================
    if hasil_filtered:
        return hasil_filtered[:top_n]
    else:
        # Jika tidak ada hasil yang relevan, return list kosong
        return []
