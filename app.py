from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd
from flask_cors import CORS  # เปิด CORS ให้ Frontend เรียก API ได้

# กำหนดพาธของไฟล์โมเดลและข้อมูล
MODEL_PATH = "C:/Users/ASUS/Desktop/ml/model/"
DATA_PATH = "C:/Users/ASUS/Desktop/ml/templates/"

# โหลดโมเดลและข้อมูลที่จำเป็น
popular_df = pickle.load(open(MODEL_PATH + 'popular.pkl', 'rb'))
pt = pickle.load(open(MODEL_PATH + 'pt.pkl', 'rb'))
books = pickle.load(open(MODEL_PATH + 'books.pkl', 'rb'))
similarity_scores = pickle.load(open(MODEL_PATH + 'similarity_scores.pkl', 'rb'))
# df = pd.read_csv('C:/Users/ASUS/Desktop/ml/templates/Books.csv', encoding='utf-8')


# ✅ แก้ไข DtypeWarning โดยใช้ low_memory=False
df = pd.read_csv(DATA_PATH + 'Books.csv', encoding='utf-8', low_memory=False)

# ตรวจสอบว่ามี 'Book-Title' ใน pt.index หรือไม่
book_titles = list(pt.index) if isinstance(pt.index, pd.Index) else []

app = Flask(__name__)
CORS(app)  # เปิดให้สามารถเรียก API ได้จาก frontend

@app.route('/')
def index():
    return render_template('index.html', book_name=popular_df['Book-Title'].values,
                           author=popular_df['Book-Author'].values,
                           image=popular_df['Image-URL-M'].values,
                           votes=popular_df['num_ratings'].values,
                           rating=popular_df['avg_rating'].values)

# ✅ แก้ไข Navbar โดยเปลี่ยน href="#" เป็น href="/recommend"
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html', book_titles=book_titles)

@app.route('/recommend_books', methods=['POST'])
def recommend_books():
    user_input = request.form.get("user_input")
    if not user_input:
        return render_template('recommend.html', book_titles=book_titles, data=[])

    recommended_books = []
    book_map = {title.strip().lower(): idx for idx, title in enumerate(pt.index)}

    if user_input.strip().lower() in book_map:
        index = book_map[user_input.strip().lower()]
        similar_items = sorted(enumerate(similarity_scores[index]), key=lambda x: x[1], reverse=True)[1:4]

        for i in similar_items:
            temp_df = books[books['Book-Title'].str.strip().str.lower() == pt.index[i[0]].strip().lower()]
            if not temp_df.empty:
                item = temp_df.drop_duplicates('Book-Title')[['Book-Title', 'Book-Author', 'Image-URL-M']].iloc[0].to_dict()
                recommended_books.append([item['Book-Title'], item['Book-Author'], item['Image-URL-M']])

    return render_template('recommend.html', book_titles=book_titles, data=recommended_books)

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    data = request.json
    selected_books = data.get("selected_books", [])

    if not selected_books:
        return jsonify({"error": "กรุณาเลือกหนังสือก่อน"}), 400

    recommended_books = []
    book_map = {title.strip().lower(): idx for idx, title in enumerate(pt.index)}

    for book in selected_books:
        book_lower = book.strip().lower()
        if book_lower not in book_map:
            continue  # ข้ามหนังสือที่ไม่อยู่ในฐานข้อมูล
        
        index = book_map[book_lower]
        similar_items = sorted(enumerate(similarity_scores[index]), key=lambda x: x[1], reverse=True)[1:4]

        for i in similar_items:
            temp_df = books[books['Book-Title'].str.strip().str.lower() == pt.index[i[0]].strip().lower()]
            if temp_df.empty:
                continue
            
            item = temp_df.drop_duplicates('Book-Title')[['Book-Title', 'Book-Author', 'Image-URL-M']].iloc[0].to_dict()
            recommended_books.append({
                "title": item['Book-Title'],
                "author": item['Book-Author'],
                "image": item['Image-URL-M']
            })

    if not recommended_books:
        return jsonify({"error": "ไม่พบหนังสือแนะนำ"}), 400

    return jsonify({"recommended_books": recommended_books})

if __name__ == '__main__':
    app.run(debug=True)
