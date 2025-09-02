import streamlit as st
import pickle
import os
from datetime import datetime

DATA_FILE = "worklog_data.pkl"
DEFAULT_CATEGORIES = [f"業務区分{i+1}" for i in range(10)]

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    else:
        return {
            "categories": DEFAULT_CATEGORIES.copy(),
            "times": [0.0] * 10,
            "last_update": None
        }

def save_data(data):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(data, f)

st.set_page_config(page_title="WorkLog", layout="centered")
st.title("WorkLog - 業務記録アプリ")

# データのロード
if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data

st.write("業務内容と時間を記録しましょう。")


st.markdown("""
    <style>
    .button {
        background-color: #F0F0F0;
    }
    </style>
""", unsafe_allow_html=True)


# 業務区分編集・時間操作
cols = st.columns([3, 2, 1, 1, 1])
cols[0].markdown("**業務区分名**")
cols[1].markdown("**時間 (h)**")
cols[2].markdown("**+**")
cols[3].markdown("**-**")
cols[4].markdown("**.**")

edited_names = data["categories"].copy()
updated = False

for i in range(10):
    c0, c1, c2, c3, c4 = st.columns([3, 2, 1, 1, 1])
    # 区分名編集
    edited_names[i] = c0.text_input(f"cat_{i}", value=data["categories"][i], label_visibility="collapsed", key=f"cat_{i}_input")
    # 時間表示
    c1.write(f"{data['times'][i]:.2f}")
    # +ボタン
    if c2.button(" ＋ ", key=f"plus_{i}"):
        data["times"][i] += 0.25
        data["last_update"] = datetime.now()
        updated = True,
        type = "secondary"
    # -ボタン
    if c3.button(" ー ", key=f"minus_{i}"):
        data["times"][i] = max(0.0, data["times"][i] - 0.25)
        data["last_update"] = datetime.now()
        updated = True

# 区分名の変更反映
if edited_names != data["categories"]:
    data["categories"] = edited_names
    data["last_update"] = datetime.now()
    updated = True

# 合計時間
total_time = sum(data["times"])
st.markdown(f"### 合計時間: {total_time:.2f} 時間")

# 最終登録日時
if data["last_update"]:
    st.write(f"最終登録日時: {data['last_update'].strftime('%Y-%m-%d %H:%M:%S')}")
else:
    st.write("最終登録日時: なし")

# リセットボタン
if st.button("リセット（全クリア）"):
    data["times"] = [0.0] * 10
    data["last_update"] = datetime.now()
    updated = True

# データ保存
if updated:
    save_data(data)
    st.session_state.data = data
    st.rerun()
