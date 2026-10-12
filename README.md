# 🌳 Urban Green Space Publications Dashboard

Web Application สำหรับสำรวจรายชื่อเอกสารเผยแพร่ด้านพื้นที่สีเขียวในเมือง ของสำนักงานนโยบายและแผนทรัพยากรธรรมชาติและสิ่งแวดล้อม (สผ.) พัฒนาด้วย **Python, Pandas, Plotly และ Streamlit**

🔗 **Live App:** `https://<ชื่อแอปของคุณ>.streamlit.app` (ใส่ลิงก์หลัง Deploy)

## Dataset
`data/urban-green-space-publication.csv` — 11 รายการ, ปี พ.ศ. 2548–2560
คอลัมน์: ลำดับ, ปี พศ, รายชื่อเอกสาร, ลิงก์ (PDF)

ข้อมูลที่แอปสร้างเพิ่ม: ปี ค.ศ., หมวดหมู่ (จัดจากคำสำคัญในชื่อเรื่อง), ความยาวชื่อเรื่อง

## ฟีเจอร์
**กราฟ (3 กราฟ)**
1. จำนวนเอกสารที่เผยแพร่ในแต่ละปี แยกตามหมวด (สลับเป็นกราฟเส้นรายปี + สะสมได้)
2. สัดส่วนเอกสารตามหมวดหมู่ (Donut chart)
3. ความยาวชื่อเอกสาร (Horizontal bar)

**Interactive Widgets (Sidebar)**
- Slider เลือกช่วงปี พ.ศ.
- Multiselect เลือกหมวดหมู่
- Text input ค้นหาจากชื่อเอกสาร
- Radio เลือกรูปแบบกราฟ (Bar / Line)
- ปุ่มดาวน์โหลดข้อมูลที่กรองแล้วเป็น CSV

## วิธีรันบนเครื่อง
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate   |   macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
เปิดเบราว์เซอร์ที่ http://localhost:8501

## โครงสร้างโปรเจกต์
```
green-space-app/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/config.toml
└── data/urban-green-space-publication.csv
```

## อัปโหลดขึ้น GitHub
1. สร้าง repository ใหม่ที่ https://github.com/new (ตั้งเป็น **Public**) เช่นชื่อ `green-space-app` — ไม่ต้องติ๊กสร้าง README
2. ในโฟลเดอร์โปรเจกต์ รัน:
```bash
git init
git add .
git commit -m "Streamlit green space publications app"
git branch -M main
git remote add origin https://github.com/<username>/green-space-app.git
git push -u origin main
```
(หรือใช้ปุ่ม **uploading an existing file** บนหน้า repo แล้วลากไฟล์ทั้งหมดขึ้นไป — อย่าลืมโฟลเดอร์ `data/`)

## Deploy บน Streamlit Community Cloud
1. ไปที่ https://share.streamlit.io แล้ว Sign in ด้วย GitHub
2. กด **Create app** → **Deploy a public app from GitHub**
3. เลือก Repository: `<username>/green-space-app`, Branch: `main`, Main file path: `app.py`
4. (ไม่บังคับ) ตั้ง App URL ที่ต้องการ แล้วกด **Deploy**
5. รอ 1–3 นาที ระบบจะติดตั้งแพ็กเกจจาก `requirements.txt` แล้วได้ลิงก์ `https://xxx.streamlit.app`
6. นำลิงก์มาใส่ในหัวข้อ Live App ด้านบน

ทุกครั้งที่ `git push` โค้ดใหม่ แอปบน Cloud จะอัปเดตอัตโนมัติ
