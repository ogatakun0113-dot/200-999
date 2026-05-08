import streamlit as st

# --- ページ設定 ---
st.set_page_config(page_title="伝送値換算 (200-999)(DEC)", layout="centered")

# --- 見た目の設定 (CSS) ---
st.markdown("""
<style>
.stNumberInput label { font-size: 18px !important; font-weight: 800 !important; color: #4169E1 !important; }
.stSelectbox label { font-size: 18px !important; font-weight: 800 !important; color: #FF4B4B !important; }
.result-box {
    background-color: #f0f2f6;
    padding: 15px;
    border-radius: 10px;
    border-left: 5px solid #4169E1;
    margin-top: 20px;
}
.credit { text-align: right; font-size: 14px; color: #666; margin-bottom: -20px; }
.calc-note { color: #d63384; font-weight: bold; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="credit">開発/制作：緒方</p>', unsafe_allow_html=True)
st.title('📱 伝送値換算 (200-999)(DEC)')

# --- 1. 基本情報設定 ---
with st.expander("⚙️ 基本情報設定 (200-999基準)", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        s_min = st.number_input("指示 0%", value=0.00)
    with col2:
        s_max = st.number_input("指示 100%", value=100.00)
    
    col3, col4 = st.columns(2)
    with col3:
        a_min = st.number_input("電流 4mA", value=4.00, format="%.2f")
    with col4:
        a_max = st.number_input("電流 20mA", value=20.00, format="%.2f")

    resistance = st.selectbox("入力抵抗を選択 (Ω)", [250, 500, 50], index=0)
    
    # 電圧自動計算（表示用）
    v_min_base = (a_min / 1000.0) * resistance
    v_max_base = (a_max / 1000.0) * resistance

    st.caption(f"💡 設定: {resistance}Ω により {a_min}mA→{v_min_base:.3f}V / {a_max}mA→{v_max_base:.3f}V")

st.markdown("---")

# --- 2. 入力セクション ---
mode = st.radio("項目を選択して入力", ["伝送値", "指示値", "割合(%)", "電流(mA)", "電圧(V)"], horizontal=True)

T_OFFSET = 200
T_DIV = 800
percent = 0.0

if mode == "伝送値":
    val = st.number_input("現在の伝送値 (200-999)", value=999, step=1)
    calc_val = val
    if val == 999:
        calc_val = 1000
        st.markdown('<p class="calc-note">※999bitを1000bitとして計算中</p>', unsafe_allow_html=True)
    percent = (float(calc_val) - T_OFFSET) / T_DIV

elif mode == "指示値":
    val = st.number_input("指示値", value=s_max)
    percent = (val - s_min) / (s_max - s_min) if (s_max - s_min) != 0 else 0

elif mode == "割合(%)":
    val = st.number_input("％値", value=100.0)
    percent = val / 100.0

elif mode == "電流(mA)":
    val = st.number_input("電流値", value=a_max, format="%.2f")
    percent = (val - a_min) / (a_max - a_min) if (a_max - a_min) != 0 else 0

elif mode == "電圧(V)":
    # --- ここを修正：format="%.3f" を追加し、stepを小さくしました ---
    val = st.number_input("電圧値 (V)", value=v_max_base, format="%.3f", step=0.001)
    percent = (val - v_min_base) / (v_max_base - v_min_base) if (v_max_base - v_min_base) != 0 else 0

# --- 3. 計算結果の算出 ---
res_scale = s_min + (s_max - s_min) * percent
res_ma = a_min + (a_max - a_min) * percent
res_v = v_min_base + (v_max_base - v_min_base) * percent

# 表示用の伝送値
res_t_raw = T_OFFSET + (T_DIV * percent)
res_t_display = int(round(res_t_raw))
if res_t_display >= 1000:
    res_t_display = 999

# --- 4. 結果表示 ---
st.markdown('<div class="result-box">', unsafe_allow_html=True)
st.subheader("📊 換算結果")
c_r1, c_r2, c_r3 = st.columns(3)
c_r1.metric("指示値", f"{res_scale:.2f}")
c_r2.metric("電流", f"{res_ma:.2f} mA")
c_r3.metric("電圧", f"{res_v:.3f} V") # 結果も3桁表示

st.metric("伝送値 (bit)", f"{res_t_display}")
st.markdown('</div>', unsafe_allow_html=True)

# --- 画面下部中央に「戻る」ボタンを配置 ---
st.markdown("---")  # 区切り線
col1, col2, col3 = st.columns([1, 1, 1])

with col2:  # 中央の列を使用
    # 水色のアイコン（🏠）と「戻る」を表示するボタン
    if st.link_button("🏠\n\n戻る", "https://menue3-pkwzfkwnoxnnuljkqg7mdt.streamlit.app/", use_container_width=True):
        pass

# ボタンの色（水色）を調整するカスタム設定
st.markdown("""
    <style>
    div.stLinkButton > a {
        background-color: #00BFFF !important; /* 水色（DeepSkyBlue） */
        color: white !important;
        border-radius: 10px;
        text-align: center;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)
