"""
Streamlit Data Visualization App
Dataset: รายชื่อเอกสารเผยแพร่ด้านพื้นที่สีเขียวในเมือง (สผ. / ONEP)
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------------
# ตั้งค่าหน้าเว็บ
# ---------------------------------------------------------------
st.set_page_config(
    page_title="Urban Green Space Publications",
    page_icon="🌳",
    layout="wide",
)

APP_DIR = Path(__file__).parent
CSV_NAME = "urban-green-space-publication.csv"


def find_data_file() -> Path | None:
    """หาไฟล์ CSV ทั้งในโฟลเดอร์ data/ และโฟลเดอร์เดียวกับ app.py"""
    for candidate in (APP_DIR / "data" / CSV_NAME, APP_DIR / CSV_NAME):
        if candidate.exists():
            return candidate
    # เผื่อชื่อไฟล์ถูกเปลี่ยน ให้หยิบ CSV ไฟล์แรกที่เจอ
    found = sorted(APP_DIR.glob("*.csv")) + sorted((APP_DIR / "data").glob("*.csv"))
    return found[0] if found else None

CATEGORY_COLORS = {
    "คู่มือ": "#2E7D32",
    "พรรณไม้ลดมลพิษ": "#81C784",
    "แนวทาง/มาตรฐาน": "#00897B",
    "เอกสารเผยแพร่ความรู้": "#C0CA33",
}


def classify(title: str) -> str:
    """จัดหมวดหมู่เอกสารจากคำสำคัญในชื่อเรื่อง"""
    if "คู่มือ" in title:
        return "คู่มือ"
    if "พรรณไม้" in title or "ไม้ประดับ" in title:
        return "พรรณไม้ลดมลพิษ"
    if any(k in title for k in ("แนวทาง", "มาตรฐาน", "แนวปฏิบัติ")):
        return "แนวทาง/มาตรฐาน"
    return "เอกสารเผยแพร่ความรู้"


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    # utf-8-sig ตัด BOM ที่หัวคอลัมน์แรกออก
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    df = df.rename(
        columns={
            "ลำดับ": "no",
            "ปี พศ": "year_be",
            "รายชื่อเอกสาร": "title",
            "ลิงก์": "link",
        }
    )
    df["year_ce"] = df["year_be"] - 543
    df["category"] = df["title"].apply(classify)
    df["title_length"] = df["title"].str.len()
    return df


DATA_PATH = find_data_file()
if DATA_PATH is None:
    st.error(
        f"ไม่พบไฟล์ `{CSV_NAME}` — กรุณาอัปโหลดไฟล์ CSV ไว้ในโฟลเดอร์ `data/` "
        "หรือโฟลเดอร์เดียวกับ `app.py` ใน GitHub repository"
    )
    st.stop()

df = load_data(DATA_PATH)

# ---------------------------------------------------------------
# Sidebar: Interactive widgets
# ---------------------------------------------------------------
st.sidebar.header("🔎 ตัวกรองข้อมูล")

min_year, max_year = int(df["year_be"].min()), int(df["year_be"].max())
year_range = st.sidebar.slider(
    "ช่วงปีที่เผยแพร่ (พ.ศ.)",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
)

all_categories = list(CATEGORY_COLORS.keys())
selected_categories = st.sidebar.multiselect(
    "หมวดหมู่เอกสาร",
    options=all_categories,
    default=all_categories,
)

keyword = st.sidebar.text_input("ค้นหาจากชื่อเอกสาร", placeholder="เช่น คาร์บอน, พรรณไม้")

chart_type = st.sidebar.radio(
    "รูปแบบกราฟจำนวนเอกสารรายปี",
    options=["กราฟแท่ง (Bar)", "กราฟเส้น (Line)"],
)

# กรองข้อมูลตาม widget
filtered = df[
    df["year_be"].between(*year_range) & df["category"].isin(selected_categories)
]
if keyword:
    filtered = filtered[filtered["title"].str.contains(keyword, case=False, regex=False)]

# ---------------------------------------------------------------
# ส่วนหัว + ตัวเลขสรุป
# ---------------------------------------------------------------
st.title("🌳 เอกสารเผยแพร่ด้านพื้นที่สีเขียวในเมือง")
st.caption(
    "ข้อมูล: สำนักงานนโยบายและแผนทรัพยากรธรรมชาติและสิ่งแวดล้อม (สผ.) · "
    f"ทั้งหมด {len(df)} รายการ ปี พ.ศ. {min_year}–{max_year}"
)

if filtered.empty:
    st.warning("ไม่พบเอกสารตามเงื่อนไขที่เลือก ลองปรับตัวกรองด้านซ้ายใหม่")
    st.stop()

c1, c2, c3 = st.columns(3)
c1.metric("จำนวนเอกสาร", f"{len(filtered)} เล่ม")
c2.metric("จำนวนปีที่มีการเผยแพร่", f"{filtered['year_be'].nunique()} ปี")
peak = filtered["year_be"].value_counts().idxmax()
c3.metric("ปีที่เผยแพร่มากที่สุด", f"พ.ศ. {peak}",
          f"{filtered['year_be'].value_counts().max()} เล่ม", delta_color="off")

st.divider()

# ---------------------------------------------------------------
# กราฟที่ 1: จำนวนเอกสารต่อปี (แยกหมวด)
# ---------------------------------------------------------------
left, right = st.columns([3, 2])

with left:
    st.subheader("📊 จำนวนเอกสารที่เผยแพร่ในแต่ละปี")
    per_year = (
        filtered.groupby(["year_be", "category"]).size().reset_index(name="count")
    )
    if chart_type.startswith("กราฟแท่ง"):
        fig1 = px.bar(
            per_year, x="year_be", y="count", color="category",
            color_discrete_map=CATEGORY_COLORS,
            labels={"year_be": "ปี พ.ศ.", "count": "จำนวนเอกสาร", "category": "หมวดหมู่"},
        )
    else:
        yearly_total = filtered.groupby("year_be").size().reset_index(name="count")
        yearly_total["cumulative"] = yearly_total["count"].cumsum()
        fig1 = px.line(
            yearly_total, x="year_be", y=["count", "cumulative"], markers=True,
            labels={"year_be": "ปี พ.ศ.", "value": "จำนวนเอกสาร", "variable": ""},
            color_discrete_sequence=["#2E7D32", "#C0CA33"],
        )
        fig1.for_each_trace(
            lambda t: t.update(name={"count": "รายปี", "cumulative": "สะสม"}[t.name])
        )
    fig1.update_xaxes(type="category", categoryorder="category ascending")
    fig1.update_yaxes(dtick=1)
    fig1.update_layout(legend_title_text="", margin=dict(t=10),
                       legend=dict(orientation="h", y=-0.25, x=0))
    st.plotly_chart(fig1, width="stretch")

# ---------------------------------------------------------------
# กราฟที่ 2: สัดส่วนตามหมวดหมู่
# ---------------------------------------------------------------
with right:
    st.subheader("🍩 สัดส่วนตามหมวดหมู่")
    by_cat = filtered["category"].value_counts().reset_index()
    by_cat.columns = ["category", "count"]
    fig2 = px.pie(
        by_cat, names="category", values="count", hole=0.5,
        color="category", color_discrete_map=CATEGORY_COLORS,
    )
    fig2.update_traces(textinfo="value+percent")
    fig2.update_layout(legend_title_text="", margin=dict(t=10),
                       legend=dict(orientation="h", y=-0.15, x=0))
    st.plotly_chart(fig2, width="stretch")

# ---------------------------------------------------------------
# กราฟที่ 3: ความยาวชื่อเอกสาร
# ---------------------------------------------------------------
st.subheader("📏 ความยาวชื่อเอกสาร (จำนวนตัวอักษร)")
by_len = filtered.sort_values("title_length")
by_len = by_len.assign(
    short_title=by_len["title"].where(
        by_len["title"].str.len() <= 45, by_len["title"].str[:45] + "…"
    )
)
fig3 = px.bar(
    by_len, x="title_length", y="short_title", orientation="h",
    color="category", color_discrete_map=CATEGORY_COLORS,
    hover_data={"title": True, "year_be": True, "short_title": False},
    labels={"title_length": "จำนวนตัวอักษร", "short_title": "",
            "category": "หมวดหมู่", "title": "ชื่อเต็ม", "year_be": "ปี พ.ศ."},
)
fig3.update_layout(legend_title_text="", height=160 + 35 * len(by_len),
                   margin=dict(t=10), yaxis={"categoryorder": "total ascending"},
                   legend=dict(orientation="h", y=-0.12, x=0))
st.plotly_chart(fig3, width="stretch")

# ---------------------------------------------------------------
# ตารางข้อมูล + ลิงก์ดาวน์โหลด
# ---------------------------------------------------------------
st.subheader("📚 รายการเอกสาร")
st.dataframe(
    filtered[["no", "year_be", "title", "category", "link"]],
    hide_index=True,
    width="stretch",
    column_config={
        "no": st.column_config.NumberColumn("ลำดับ", width="small"),
        "year_be": st.column_config.NumberColumn("ปี พ.ศ.", format="%d", width="small"),
        "title": st.column_config.TextColumn("ชื่อเอกสาร", width="large"),
        "category": "หมวดหมู่",
        "link": st.column_config.LinkColumn("ไฟล์ PDF", display_text="เปิดอ่าน"),
    },
)

st.download_button(
    "⬇️ ดาวน์โหลดข้อมูลที่กรองแล้ว (CSV)",
    data=filtered.to_csv(index=False).encode("utf-8-sig"),
    file_name="filtered-green-space-publications.csv",
    mime="text/csv",
)
