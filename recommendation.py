import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

# Load datasets
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

# ----- Content-Based Filtering -----
movies['combined_features'] = movies['genre'] + " " + movies['description']
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['combined_features'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

def content_based_recommend(title, top_n=5):
    if title not in movies['title'].values:
        return []
    idx = movies.index[movies['title']==title][0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    movie_indices = [i[0] for i in sim_scores]
    recommendations = []
    for i in movie_indices:
        row = movies.iloc[i]
        poster = row['poster_url'] if 'poster_url' in movies.columns and row['poster_url'] else "https://via.placeholder.com/150"
        recommendations.append({
            'title': row['title'],
            'poster_url': poster
        })
    return recommendations

# ----- Collaborative Filtering (User-Based) -----
user_movie_matrix = ratings.pivot_table(index='user_id', columns='movie_id', values='rating').fillna(0)
user_sim = cosine_similarity(user_movie_matrix)
user_sim_df = pd.DataFrame(user_sim, index=user_movie_matrix.index, columns=user_movie_matrix.index)

def collaborative_recommend(user_id, top_n=5):
    if user_id not in user_sim_df.index:
        return []
    sim_scores = user_sim_df[user_id].drop(user_id)
    similar_users = sim_scores.sort_values(ascending=False).index
    movie_scores = {}
    for u in similar_users:
        for movie_id, rating in user_movie_matrix.loc[u].items():
            if user_movie_matrix.loc[user_id, movie_id]==0:
                movie_scores[movie_id] = movie_scores.get(movie_id,0)+rating*sim_scores[u]
    top_movies = sorted(movie_scores.items(), key=lambda x:x[1], reverse=True)[:top_n]
    recommendations = []
    for mid,_ in top_movies:
        row = movies[movies['movie_id']==mid].iloc[0]
        poster = row['poster_url'] if 'poster_url' in movies.columns and row['poster_url'] else "https://via.placeholder.com/150"
        recommendations.append({
            'title': row['title'],
            'poster_url': poster
        })
    return recommendations

# ----- Hybrid Recommendation -----
def hybrid_recommend(user_input, user_id=None, top_n=5):
    content_recs = content_based_recommend(user_input, top_n=top_n)
    if user_id:
        collab_recs = collaborative_recommend(user_id, top_n=top_n)
        combined = {r['title']: r for r in content_recs}
        for r in collab_recs:
            combined[r['title']] = r
        return list(combined.values())[:top_n]
    return content_recs
