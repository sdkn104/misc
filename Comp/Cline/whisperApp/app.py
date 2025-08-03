import streamlit as st
import whisper
import tempfile
import os

st.set_page_config(page_title="Whisper 日本語音声テキスト化", layout="centered")
st.title("Whisper 日本語音声テキスト化アプリ")

st.write("音声ファイル（wav, mp3, m4a等）をアップロードしてください。Whisperで日本語テキスト化します。")

uploaded_file = st.file_uploader("音声ファイルを選択", type=["wav", "mp3", "m4a"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    st.info("Whisperモデルをロード中です。少々お待ちください。")
    model = whisper.load_model("small")  # 必要に応じてモデルサイズを変更

    st.info("音声をテキスト化しています...")
    result = model.transcribe(tmp_path, language="ja")
    text = result["text"]

    st.success("テキスト化が完了しました。")
    st.text_area("テキスト化結果", text, height=300)

    # ダウンロード機能
    st.download_button(
        label="テキストをダウンロード",
        data=text,
        file_name="transcription.txt",
        mime="text/plain"
    )

    # 一時ファイル削除
    os.remove(tmp_path)
