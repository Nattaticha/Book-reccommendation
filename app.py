from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

# กำหนดพาธของไฟล์โมเดลและข้อมูล
MODEL_PATH = "C:/Users/ASUS/Desktop/ml/model/"
DATA_PATH = "C:/Users/ASUS/Desktop/ml/templates/"

# โหลดโมเดลและข้อมูลที่จำเป็น
popular_df = pickle.load(open('C:/Users/ASUS/Desktop/ml/model/popular.pkl', 'rb'))
pt = pickle.load(open('C:/Users/ASUS/Desktop/ml/model/pt.pkl', 'rb'))
books = pickle.load(open('C:/Users/ASUS/Desktop/ml/model/books.pkl', 'rb'))
similarity_scores = pickle.load(open('C:/Users/ASUS/Desktop/ml/model/similarity_scores.pkl', 'rb'))
df = pd.read_csv('C:/Users/ASUS/Desktop/ml/templates/Books.csv', encoding='utf-8')

# สร้างรายการชื่อหนังสือจาก pt.index
book_titles = list(pt.index)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', book_name=popular_df['Book-Title'].values,
                           author=popular_df['Book-Author'].values,
                           image=popular_df['Image-URL-M'].values,
                           votes=popular_df['num_ratings'].values,
                           rating=popular_df['avg_rating'].values)

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html', book_titles=book_titles)

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input', '').strip().lower()
    
    # สร้าง Mapping ของ pt.index
    book_map = {title.strip().lower(): idx for idx, title in enumerate(pt.index)}
    
    if user_input not in book_map:
        return render_template('recommend.html', book_titles=book_titles, data=[],
                               error="❌ ไม่พบหนังสือที่เลือก กรุณาเลือกจากรายการ")

    index = book_map[user_input]
    
    # คำนวณหนังสือที่คล้ายกัน
    similar_items = sorted(enumerate(similarity_scores[index]), key=lambda x: x[1], reverse=True)[1:6]
    
    data = []
    for i in similar_items:
        temp_df = books[books['Book-Title'].str.strip().str.lower() == pt.index[i[0]].strip().lower()]
        if temp_df.empty:
            continue
        
        item = temp_df.drop_duplicates('Book-Title')[['Book-Title', 'Book-Author', 'Image-URL-M']].iloc[0].tolist()
        data.append(item)
    
    if not data:
        return render_template('recommend.html', book_titles=book_titles, data=[],
                               error="❌ ไม่พบหนังสือที่คล้ายกัน กรุณาลองเลือกเล่มอื่น")
    
    return render_template('recommend.html', book_titles=book_titles, data=data)

if __name__ == '__main__':
    app.run(debug=True)
