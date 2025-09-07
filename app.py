from flask import Flask, render_template, request
from recommendation import hybrid_recommend

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie = request.form['movie']
    user_id = request.form.get('user_id')
    user_id = int(user_id) if user_id else None
    recommendations = hybrid_recommend(movie, user_id=user_id, top_n=5)
    return render_template('index.html', movie=movie, recommendations=recommendations)

if __name__ == "__main__":
    # Custom port 8000
    app.run(debug=True, host="0.0.0.0", port=8000)
