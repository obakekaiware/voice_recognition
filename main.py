import time
from functools import partial
from tqdm import tqdm as std_tqdm
from pathlib import Path
import speech_recognition as sr
import streamlit as st

tqdm = partial(std_tqdm, dynamic_ncols=True)


def recognize(file_path: Path) -> str:
    texts = []
    r = sr.Recognizer()
    audio_file = sr.AudioFile(file_path)
    split_time = 179
    with audio_file as source:
        duration = source.DURATION
        progress_text = "音声文字起こし中..."
        my_bar = st.progress(0, text=progress_text)
        for i in range(0, int(duration), split_time):
            start = i
            end = min(i + split_time, duration)
            audio = r.record(source, duration=end - start)
            try:
                text = r.recognize_google(audio, language="ja-JP")
                my_bar.progress((i + 1) / duration, text=progress_text)
                texts.append(text)
                print(text)
            except sr.UnknownValueError:
                # 認識できなかった場合の処理
                print("Could not understand audio")
            time.sleep(1)
    all_text = "".join(texts)
    return all_text


def main():
    st.title("日本語音声文字起こしアプリ")
    explain = "音声ファイル（WAV）をドロップしてください。（10分の音声ファイルを文字起こしするのに2分くらいかかります。精度はあんま良くないです。）"
    uploaded_file = st.file_uploader(explain)
    if uploaded_file is not None:
        text = recognize(uploaded_file)
        st.write("以下が音声文字起こしの結果です。")
        st.write(text)
        st.write("上記のテキストをコピーしてご利用ください。")


if __name__ == "__main__":
    main()
