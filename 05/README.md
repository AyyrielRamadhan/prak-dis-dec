# Praktikum Minggu 05 - Fault Tolerance

**Mata Kuliah:** Praktikum Sistem Terdistribusi dan Terdesentralisasi

**Topik:** Fault Tolerance

---

## 🎯 Tujuan Praktikum

1.
2.
3.
4.
5.

---

## 📚 Dasar Teori

---

# ⏩ PEMBAHASAN PRAKTIKUM

### 4.1 Load Balancing Aplikasi

#### 4.1.1 Persiapan

#### Install Docker

Langkah pertama yaitu menginstall Docker Dekstop terlebih dahulu, karena pada praktikum sebelumnya sudah menginstall docker, maka cukup cek versi saja:

<img src="images/01_Version_Docker.png" width="700">

#### Pembahasan

---

#### Buat Folder Kerja

<img src="images/02_Buat_Folder_Kerja.png" width="700">

#### Pembahasan

---

#### Cek List Versi Python yang tersedia

<img src="images/03_Cek_Python_List.png" width="700">

#### Pembahasan

---

#### Menyematkan Versi Python

<img src="images/04_Sematkan_Versi_Python_.png" width="700">

#### Pembahasan

---

#### Menampilkan daftar seluruh berkas dan folder secara rinci, termasuk yang tersembunyi

<img src="images/05_Daftar_Seluruh_Berkas.png" width="700">

#### Pembahasan

---

#### Membuat lingkungan virtual Python (virtual environment) baru.

<img src="images/06_Membuat_Lingkungan_Virtual_Python.png" width="700">

#### Pembahasan

---

#### Mengaktifkan lingkungan virtual (virtual environment) Python di sistem operasi Windows

Untuk mengaktifkan virtual environment Python di windows dapat menggunakan perintah:

```bash
source .venv/Scripts/activate
```

<img src="images/07_Mengaktifkan_Lingkungan_Virtual.png" width="700">

#### Pembahasan

---

#### Install blacksheep dan blacksheep-cli

Untuk membuat aplikasi web menggunakan Blacksheep, install blacksheep dan blacksheep-cli terlebih dahulu:

_Install Blacksheep_

Untuk menginstall Blacksheep dapat menggunakan perintah:

```bash
uv pip install blacksheep
```

<img src="images/08_Install_Package_Blacksheep.png" width="700">

#### Pembahasan

---

_Install Blacksheep CLI_

Untuk menginstall Blacksheep CLI dapat menggunakan perintah:

```bash
uv pip install blacksheep-cli
```

<img src="images/09_Install_Blacksheep_CLI.png" width="700">

#### Pembahasan

---

#### 4.1.2 Pembuatan Aplikasi Web

Setelah itu, buat aplikasi menggunakan cli dengan perintah:

```bash
blacksheep create
```

<img src="images/10_Pembuatan_Aplikasi_Web.png" width="700">

#### Pembahasan

---

Install paket yang diperlukan:

Masuk terlebih dahulu ke folder direktori blacksheep_lb dengan perintah:

```bash
cd blacksheep_lb
```

Kemudian menginstall paket yang diperlukan dengan perintah:

```bash
uv pip install -r requirements.txt
```

<img src="images/11_Install_Paket.png" width="700">

#### Pembahasan

---

Memastikan bahwa aplikasi tersebut bisa berjalan dengan baik:

```bash
python dev.py
```

<img src="images/12_Uji_Jalan_Aplikasi.png" width="700">

kemudian akses ke http://localhost:44777/ menggunakan browser

<img src="images/13_Open_Browser.png" width="700">

Lalu pada shell tempat mengaktifkan server, muncul:

<img src="images/14_Shell_After_Menjalankan_Di_Browser.png" width="700">

Pada titik ini, sudah berhasil membuat aplikasi menggunakan Blacksheep. Perhatikan, dalam direktori blacksheep_lb sudah ada Dockerfile yang bisa digunakan:

<img src="images/15_Isi_Direktori_blacksheep_lb.png" width="700">

#### Pembahasan

---

#### 4.1.3 Siapkan Dockerfile dan docker-compose.yml

Struktur yang dihasilkan harus terdiri dari:

```
workspace-05/
├── blacksheep_lb/
│   ├── app/
│   ├── dev.py
│   ├── Dockerfile
│   ├── domain/
│   ├── pyproject.toml
│   ├── README.md
│   ├── requirements.txt
│   ├── settings.dev.toml
│   ├── settings.toml
│   └── tests/
├── docker-compose.yml
├── env.sh
└── nginx/
    ├── Dockerfile
    └── nginx.conf
```

_File blacksheep_lb/Dockerfile_

```
# Build the Server
FROM python:3.13.1-slim AS server_builder
WORKDIR /home
RUN echo "APT::Get::Assume-Yes \"true\";" > /etc/apt/apt.conf.d/90assumeyes
RUN apt-get update && apt-get install make \
    apt-utils \
    lsb-release \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    sqlite3 \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libsqlite3-dev \
    unixodbc-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libreadline-dev \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    wget
COPY . /home
RUN python -m venv venv && . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 80

FROM python:3.13.1-slim
WORKDIR /home
COPY --from=server_builder /home/ /home/

ENV APP_ENV=prod BG_COLOR="#1abc9c" APP_ROUTE_PREFIX=""
RUN echo "APT::Get::Assume-Yes \"true\";" > /etc/apt/apt.conf.d/90assumeyes
RUN apt-get update && apt-get install \
    ca-certificates \
    sqlite3 \
    libsqlite3-dev \
    libjpeg-dev \
    zlib1g-dev
CMD ["sh", "-c", ". venv/bin/activate && uvicorn \"app.main:app\" --host 0.0.0.0 --port 80 --log-level info"]
```

#### Pembahasan

---

---

## 📝 Kesimpulan

---

## 🗒️ Referensi
