# ระบบแนะนำหนังสือ (Book Recommendation System)

## ข้อมูลที่ใช้ในการฝึกโมเดล

* ข้อมูลหนังสือ: ได้รับจาก [Book Recommendation Dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset) บน Kaggle ซึ่งรวบรวมข้อมูลจากแหล่งต่างๆ เพื่อใช้ในการฝึกโมเดล

## วัตถุประสงค์

ด้วยระบบแนะนำหนังสือที่แม่นยำ คุณจะไม่พลาดหนังสือเล่มโปรดเล่มใหม่ ระบบของเราจะวิเคราะห์ความชอบของคุณและแนะนำหนังสือที่ตรงใจคุณที่สุด

## คุณสมบัติหลัก

* แนะนำหนังสือยอดนิยม
* แนะนำหนังสือตามความคล้ายคลึงกับหนังสือที่ผู้ใช้สนใจ
* มีการแสดงแสดงผลข้อมูลหนังสือ ชื่อผู้แต่ง และภาพปก ในการแนะนำให้กับผู้ใช้งานเพื่อง่ายต่อการตัดสินใจ

## วิธีใช้งาน

1.  **ดาวน์โหลดไฟล์โมเดลที่จำเป็น:**
    * `popular.pkl`
    * `similarity.pkl`
    * `books.pkl`
2.  **ติดตั้งไลบรารีที่จำเป็น:**
    ```bash
    pip install flask pickle numpy pandas
    ```
3.  **รันแอปพลิเคชัน:**
    ```bash
    python app.py
    ```
4.  **เข้าถึงเว็บไซต์:** เปิดเว็บเบราว์เซอร์และไปที่ `http://127.0.0.1:5000/`
5.  **สำรวจเว็บไซต์:**
    * `index.html`: หน้าแรกของเว็บไซต์ แสดงหนังสือยอดนิยม
    * `recommend.html`: หน้าแสดงหนังสือแนะนำตามความคล้ายคลึง

## การติดตั้งจาก GitHub

1.  **โคลนโปรเจกต์:**
    ```bash
    git clone [https://github.com/yourusername/book-recommendation.git](https://github.com/yourusername/book-recommendation.git)
    cd book-recommendation
    ```
2.  **ติดตั้งไลบรารี:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **รันแอปพลิเคชัน:**
    ```bash
    python app.py
    ```

## ข้อมูลผู้พัฒนา
ชื่อ: นางสาวณัฏฐธิชา วงศ์เดช
นักศึกษาชั้นปีที่ 2 คณะวิศวกรรมศาสตร์ สาขาปัญญาประดิษฐ์
ช่องทางการติดต่อ:
📧 Email: nattatichawongdet@gmail.com
