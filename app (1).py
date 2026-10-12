import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Quản lý điểm sinh viên", page_icon="🎓", layout="wide")

# Du lieu mau: thay bang du lieu duoc giao neu giang vien yeu cau
data = {
    "Ho_ten": [
        "Nguyen Van An", "Tran Thi Binh", "Le Van Cuong", "Pham Thi Dung",
        "Hoang Van Em", "Vo Thi Giang", "Do Van Hung", "Bui Thi Lan",
        "Dang Van Minh", "Ngo Thi Nga"
    ],
    "Chuyen_can": [9, 8, 7, 10, 6, 8, 5, 9, 7, 6],
    "Giua_ky":    [8, 7, 6, 9, 5, 8, 4, 9, 7, 6],
    "Cuoi_ky":    [9, 8, 7, 9, 6, 7, 4, 10, 8, 5]
}

df = pd.DataFrame(data)

# Tinh diem tong ket theo cong thuc trong de
df["Tong_ket"] = (
    0.2 * df["Chuyen_can"]
    + 0.3 * df["Giua_ky"]
    + 0.5 * df["Cuoi_ky"]
).round(2)

# Xep loai theo cac moc trong de
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    return "Yếu"

df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# Tieu de
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# Bang diem
st.subheader("Bảng điểm 10 sinh viên")
bang_hien_thi = df.rename(columns={
    "Ho_ten": "Họ tên",
    "Chuyen_can": "Chuyên cần",
    "Giua_ky": "Giữa kỳ",
    "Cuoi_ky": "Cuối kỳ",
    "Tong_ket": "Tổng kết",
    "Xep_loai": "Xếp loại"
})
st.dataframe(bang_hien_thi, use_container_width=True, hide_index=True)

# Thong ke
diem_tb = df["Tong_ket"].mean()
idx_max = df["Tong_ket"].idxmax()
idx_min = df["Tong_ket"].idxmin()
sv_cao_nhat = df.loc[idx_max]
sv_thap_nhat = df.loc[idx_min]
so_sv_dat = int((df["Tong_ket"] >= 5).sum())

c1, c2, c3 = st.columns(3)
c1.metric("Điểm trung bình lớp", f"{diem_tb:.2f}")
c2.metric("Số sinh viên đạt (≥ 5)", f"{so_sv_dat}/10")
c3.metric("Số sinh viên", f"{len(df)}")

c4, c5 = st.columns(2)
with c4:
    st.info(f"Sinh viên cao nhất: {sv_cao_nhat['Ho_ten']} — {sv_cao_nhat['Tong_ket']:.2f} điểm")
with c5:
    st.info(f"Sinh viên thấp nhất: {sv_thap_nhat['Ho_ten']} — {sv_thap_nhat['Tong_ket']:.2f} điểm")

# Selectbox
st.subheader("Tra cứu điểm theo sinh viên")
ten_chon = st.selectbox("Chọn một sinh viên", df["Ho_ten"].tolist())
sv = df.loc[df["Ho_ten"] == ten_chon].iloc[0]
st.write(f"**Họ tên:** {sv['Ho_ten']}")
d1, d2, d3, d4 = st.columns(4)
d1.metric("Chuyên cần", f"{sv['Chuyen_can']:.1f}")
d2.metric("Giữa kỳ", f"{sv['Giua_ky']:.1f}")
d3.metric("Cuối kỳ", f"{sv['Cuoi_ky']:.1f}")
d4.metric("Tổng kết", f"{sv['Tong_ket']:.2f}")
st.write(f"**Xếp loại:** {sv['Xep_loai']}")

# Bieu do cot
st.subheader("Biểu đồ điểm tổng kết")
fig, ax = plt.subplots(figsize=(11, 5))
ax.bar(df["Ho_ten"], df["Tong_ket"])
ax.set_title("Điểm tổng kết của 10 sinh viên")
ax.set_xlabel("Họ tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)
ax.tick_params(axis="x", labelrotation=45)
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# Thong tin nguoi tao app theo de bai
st.markdown("---")
st.caption("Người tạo ứng dụng: Nguyễn Thế Sơn | MSSV: 054208009618")
