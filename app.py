import streamlit as st

# --- ページ設定 ---
st.set_page_config(page_title="伝送値換算 (200-999)", layout="centered")

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
st.title('📱 伝送値換算 (200-999)')

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
    
    # 電圧自動計算
    v_min = (a_min / 1000.0) * resistance
    v_max = (a_max / 1000.0) * resistance

    st.caption(f"💡 設定: {resistance}Ω により {a_min}mA→{v_min:.3f}V / {a_max}mA→{v_max:.3f}V")

# --- 2. 入力セクション ---
mode = st.radio("項目を選択して入力", ["伝送値", "指示値", "割合(%)", "電流(mA)", "電圧(V)"], horizontal=True)

T_OFFSET = 200
T_DIV = 800
percent = 0.0

if mode == "伝送値":
    val = st.number_input("現在の伝送値 (200-999)", value=999, step=1)
    # 999bitの時のみ1000bitとして計算する読み替え
    calc_val = val
    if val == 999:
        calc_val = 1000
        st.markdown('<p class="calc-note">※999bitを1000bitとして計算中</p>', unsafe_allow_html=True)
    percent = (float(calc_val) - T_OFFSET) / T_DIV
elif mode == "指示値":
    val = st.number_input("指示値", value=s_max)
    percent = (val - s_min) / (s_max - s_min)
elif mode == "割合(%)":
    val = st.number_input("％値", value=100.0)
    percent = val / 100.0
elif mode == "電流(mA)":
    val = st.number_input("電流値", value=a_max)
    percent = (val - a_min) / (a_max - a_min)
elif mode == "電圧(V)":
    val = st.number_input("電圧値", value=v_max)
    percent = (val - v_min) / (v_max - v_min)

# --- 3. 計算結果の算出 ---
res_scale = s_min + (s_max - s_min) * percent
res_ma = a_min + (a_max - a_min) * percent
res_v = v_min + (v_max - v_min) * percent

# 表示用の伝送値（内部で1000になっても表示は999で止める）
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
c_r3.metric("電圧", f"{res_v:.3f} V")

st.metric("伝送値 (bit)", f"{res_t_display}")
st.markdown('</div>', unsafe_allow_html=True)

st.caption("※分母を800bitとして計算し、999bit入力時は100%（1000bit相当）として読み替えています。")
