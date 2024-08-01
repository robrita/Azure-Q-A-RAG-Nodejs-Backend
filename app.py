import os
import requests
import streamlit as st
import app.pages
import app.sidebar
from dotenv import load_dotenv

load_dotenv()


def prob1():
    question = st.text_area(
        "1.)",
        "Apa yang membedakan user 'root' dengan user biasa?",
        height=200,
    )
    st.subheader("Answer:")
    answer = st.text_area(
        "Enter your answer here.",
        "Izin menjawab 1. Pengguna 'root' memiliki hak akses penuh ke sistem, sementara pengguna biasa memiliki hak akses terbatas terhadap file dan konfigurasi sistem. 2. Anda dapat menggunakan perintah 'sudo' sebelum perintah yang ingin Anda jalankan. Contoh: `sudo nano /etc/hosts`. 3. Anda dapat menggunakan perintah 'usermod' untuk menambahkan pengguna ke grup tertentu. Contoh: `sudo usermod -aG nama_grup nama_pengguna`.",
        height=200,
    )
    return question, answer


# https://tutorial.math.lamar.edu/problems/calci/areabetweencurves.aspx
def prob2():
    question = st.text_area(
        "2.)",
        "Bagaimana cara menjalankan suatu perintah (misal nano /etc/hosts) pada sesi user biasa dengan hak akses setara administrator (root) tanpa harus login sebagai root",
        height=200,
    )
    st.subheader("Answer:")
    answer = st.text_area(
        "Enter your answer here.",
        "1. User 'root' adalah akun superuser atau administrator pada sistem Linux/Unix yang memiliki akses penuh ke semua file dan perintah di sistem. User biasa, di sisi lain, memiliki keterbatasan akses yang ditetapkan oleh administrator sistem. 2. Salah satu cara untuk menjalankan suatu perintah dengan hak akses setara administrator (root) tanpa harus login sebagai root adalah dengan menggunakan perintah 'sudo'. kita dapat menambahkan 'sudo' sebelum perintah yang ingin dijalankan. 3. Untuk memasukkan user biasa ke dalam grup yang memiliki akses setara admin/root, kita dapat menggunakan perintah 'usermod'. Misalnya, jika kita ingin menambahkan user 'john' ke grup 'sudo' (grup yang biasanya memiliki hak akses sudo), kita dapat menjalankan perintah berikut: sudo usermod -aG sudo john Ini akan menambahkan user 'john' ke dalam grup 'sudo', yang memungkinkannya untuk menjalankan perintah dengan hak akses setara admin/root menggunakan 'sudo'. Pastikan untuk mengganti 'sudo' dengan nama grup yang sesuai jika grup admin yang digunakan memiliki nama yang berbeda. Setelah menjalankan perintah ini, user 'john' perlu logout dan login kembali untuk perubahan tersebut mulai berlaku.",
        height=200,
    )
    return question, answer


# https://tutorial.math.lamar.edu/classes/de/laplacetransforms.aspx
def prob3():
    question = st.text_area(
        "3.)",
        "Bagaimana memasukkan user biasa kedalam group, sehingga user tersebut bisa menjalankan perintah setara admin/root",
        height=200,
    )
    st.subheader("Answer:")
    answer = st.text_area(
        "Enter your answer here.",
        "Assalamualaikum Wr.. Wb.. User root memiliki hak akses penuh (superuser) terhadap semua file, direktori, dan program pada sistem. Sedangkan user biasa memiliki hak akses yang terbatas pada sistem, mengubah file dan direktori di direktori home mereka.  Untuk menjalankan suatu perintah pada sesi user biasa dengan hak akses setara administrator (root) tanpa harus login sebagai root bisa menggunakan perintah sudo. Perintah tersebut memungkinkan user biasa untuk menjalankan perintah dengan hak akses root dengan memasukkan password user root. Cara memasukkan user biasa ke dalam group, sehingga user tersebut bisa menjalankan perintah setara admin/root adalah menggunakan perintah sebagai berikut : #usermod –G admins, developer user1 : User1 menjadi anggota group admin atau root dan developer. Sumber : BMP – MSIM4308 – Administrasi Server – Modul 2",
        height=200,
    )
    return question, answer


if __name__ == "__main__":
    # App home page
    app.pages.show_home()

    # app sidebar
    with st.sidebar:
        appKey = app.sidebar.show_sidebar()

    # question items
    st.subheader("Question:")

    QUESTIONS = {
        "Problem #1": prob1,
        "Problem #2": prob2,
        "Problem #3": prob3,
    }

    page = st.selectbox("Select your question.", options=list(QUESTIONS.keys()))
    question, answer = QUESTIONS[page]()

    # Start LLM process
    start_button = st.button(
        "Validate", key="button_text_start", disabled=question == "" or answer == ""
    )
    st.subheader("Feedback:")

    if start_button:
        if appKey == os.environ["APP_KEY"]:
            with st.spinner("Processing ..."):
                try:
                    # Response generation
                    full_response = ""
                    message_placeholder = st.empty()

                    url = os.environ["API_URL"]
                    headers = {
                        "Content-Type": "application/json",
                        "x-api-key": os.environ["API_KEY"],
                    }
                    data = {"question": question, "answer": answer}

                    response = requests.post(url, headers=headers, json=data)
                    resObj = response.json()

                    print("*************************", response.status_code, resObj)
                    message_placeholder.json(resObj)

                    # Clear results
                    if st.button(":red[Clear]", key="button_text_clear"):
                        message_placeholder = st.empty()

                except Exception as e:
                    st.error(f"An error occurred: {e}")

        else:
            st.error("Invalid Access Key!")
            st.stop()
