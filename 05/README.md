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

**_Install Blacksheep_**

Untuk menginstall Blacksheep dapat menggunakan perintah:

```bash
uv pip install blacksheep
```

<img src="images/08_Install_Package_Blacksheep.png" width="700">

#### Pembahasan

---

**_Install Blacksheep CLI_**

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

**_Install paket yang diperlukan_**

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

#### Pembahasan

---

kemudian akses ke http://localhost:44777/ menggunakan browser

<img src="images/13_Open_Browser.png" width="700">

#### Pembahasan

---

Lalu pada shell tempat mengaktifkan server, muncul:

<img src="images/14_Shell_After_Menjalankan_Di_Browser.png" width="700">

#### Pembahasan

---

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
FROM python:3.14.4-slim AS server_builder
WORKDIR /home
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY . /home
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 80

FROM python:3.14.4-slim
WORKDIR /home
COPY --from=server_builder /home /home

ENV APP_ENV=prod BG_COLOR="#1abc9c" APP_ROUTE_PREFIX=""
CMD ["sh", "-c", ". venv/bin/activate && uvicorn \"app.main:app\" --host 0.0.0.0 --port 80 --log-level info"]
```

<img src="images/16_Isi_Dockerfile_Pada_blacksheep_lb.png" width="700">

#### Pembahasan

---

Kemudian membuat direktori baru bernama _nginx_ pada workspace-05 dengan perintah:

```bash
mkdir nginx
```

Lalu masuk ke folder tersebut dengan perintah:

```bash
cd nginx
```

<img src="images/17_Buat_Folder_nginx.png" width="700">

#### Pembahasan

---

Selanjutnya membuat file Dockerfile dan nginx.conf pada direktori nginx

**_Dockerfile_**

Gunakan perintah:

```bash
touch Dockerfile
```

<img src="images/18_Buat_File_Dockerfile_Pada_Folder_nginx.png" width="700">

#### Pembahasan

---

Kemudian **_Dockerfile_** di isi dengan kode:

```
FROM nginx

# Override the default nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf
```

<img src="images/19_Isi_File_Dockerfile.png" width="700">

#### Pembahasan

---

**_nginx.conf_**

Gunakan perintah:

```bash
touch nginx.conf
```

<img src="images/20_Buat_File_nginx_conf_Pada_Folder_nginx.png" width="700">

#### Pembahasan

---

Kemudian **_nginx.conf_** di isi dengan kode:

```
events {
    worker_connections 4096;
}

http {
    # Definisi grup, lihat di docker-compose.yml
    upstream backend {
        server bs_app:80;
        }
        server {
            listen 80;
            location / {
                # sesuaikan dengan nama upstream di atas
                proxy_pass http://backend;
                }
            }
}
```

<img src="images/21_Isi_File_nginx_conf.png" width="700">

#### Pembahasan

---

**_docker-compose.yml_**

Selanjutnya membuat file bernama **_docker-compose.yml_** pada workspace-05 dengan perintah:

```bash
touch docker-compose.yml
```

<img src="images/22_Buat_File_docker_compose_yml.png" width="700">

#### Pembahasan

---

Kemudian **_docker-compose.yml_** di isi dengan kode:

```
services:
  # aplikasi yang akan di-scale
  # ada pada direktori blacksheep_lb
  bs_app:
    build: ./blacksheep_lb
  # aktifkan nginx dengan menggunakan nginx/Dockerfile
  # lihat pada build
  nginx:
    container_name: nginx
    build: ./nginx
    ports:
      - "80:80"
    depends_on:
      - bs_app
```

<img src="images/23_Isi_File_docker_compose_yml.png" width="700">

#### Pembahasan

**_env.sh_**

Selanjutnya membuat file bernama **_env.sh_** pada workspace-05 dengan perintah:

```bash
touch env.sh
```

<img src="images/24_Membuat_File_env_sh.png" width="700">

#### Pembahasan

---

Kemudian **_env.sh_** di isi dengan kode:

```
alias dcu="docker-compose up --build -d --scale bs_app=2"
alias dcd="docker compose down"
alias dps="docker ps --format '{{.Image}} {{.Names}}'"
alias dcln="docker logs nginx"
```

<img src="images/25_Isi_File_env_sh.png" width="700">

#### Pembahasan

---

Sebelum menjalankan Docker, Muat Alias terlebih dahulu dengan perintah:

```bash
source env.sh
```

<img src="images/26_Muat_Alias.png" width="700">

#### Pembahasan

---

#### 4.1.4 Jalankan Docker Compose

**_Jalankan Docker Compose_**

Gunakan perintah:

```bash
dcu
```

<img src="images/27_Alias_dcu.png" width="700">
<img src="images/28_Alias_dcu.png" width="700">

#### Pembahasan

---

Untuk memeriksa, bisa melihat pada browser

<img src="images/29_Uji_Jalankan_Blacksheep_Localhost.png" width="700">

#### Pembahasan

---

**_Cek status Container_**

Gunakan perintah:

```bash
dps
```

<img src="images/30_Cek_Status_Container.png" width="700">

#### Pembahasan

---

**_Periksa Log Distribusi Request_**

Gunakan perintah:

```bash
docker logs workspace-05-bs_app-2
```

dan

```bash
docker logs workspace-05-bs_app-1
```

<img src="images/31_Periksa_Log_Distribusi_Request.png" width="700">

#### Pembahasan

---

**_Mematikan Semua Container_**

Jika sudah selesai, matikan semua container dengan perintah:

```bash
dcd
```

<img src="images/32_Mematikan_Semua_Container.png" width="700">

#### Pembahasan

---

### 4.2 Failure Detection

**_Heartbeat_**

Buat file **_check-server.py_** dengan isi kode:

```
# taken from:
# https://stackoverflow.com/questions/20867184/how-to-check-whether-my-server-is-up-and-running-using-python

import sys
import socket

def servertest(argv):
    host = argv[1]
    port = int(argv[2])

    args = socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_STREAM)
    for family, socktype, proto, canonname, sockaddr in args:
        s = socket.socket(family, socktype, proto)
        try:
            s.connect(sockaddr)
        except socket.error:
            return False
        else:
            s.close()
            return True


if __name__ == "__main__":
    if servertest(sys.argv):
        print("Server up")
    else:
        print("Server down")
```

<img src="images/34_Check-Server_py.png" width="700">

#### Pembahasan

---

Untuk menguji Heartbeat dapat menggunakan perintah:

Untuk blacksheep pada **_port 44777_** gunakan perintah:

```bash
python check-server.py localhost 44777
```

dan

Untuk blacksheep pada **_port localhost_** gunakan perintah:

```bash
python check-server.py localhost 80
```

#### Pembahasan

---

Kemudian menguji ketika aplikasi blacksheep di port 44777 atau di localhost tidak aktif hasilnya seperti berikut:

<img src="images/35_Hasil_Before_On_Blacksheep.png" width="700">

Selanjutnya menguji aplikasi blacksheep di port 44777 atau di localhost yang aktif hasilnya seperti berikut:

<img src="images/36_Hasil_After_On_Blacksheep.png" width="700">

#### Pembahasan

---

**_failure-detection_**

Library tenacity (https://github.com/jd/tenacity) bisa digunakan untuk mengelola proses yang memerlukan keterkaitan dengan komponen di luar aplikasi. Hal ini diperlukan. karena selalu ada kemungkinan kegagalan untuk koneksi dengan komponen di luar aplikasi.

_Install Package tenacity dan request_

<img src="images/37_Menginstall_Package_Tenacity.png" width="700">

#### Pembahasan

---

Kemudian buat file bernama **_check-retry.py_** dengan isi kode:

```
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import requests

@retry(
    stop=stop_after_attempt(5),  # Stop after 5 attempts
    wait=wait_exponential(multiplier=1, min=4, max=10), # Exponential backoff with min 4s, max 10s
    retry=retry_if_exception_type(requests.exceptions.ConnectionError) # Retry only on connection errors
)

def make_http_request(url):
    print(f"Attempting to access {url}...")
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    print(f"Successfully accessed {url}")
    return response.text

try:
    content = make_http_request("http://localhost:44777")
    # Process the content
except Exception as e:
    print(f"Failed to access URL after multiple retries: {e}")
```

<img src="images/38_Isi_File_check-retry_py.png" width="700">

#### Pembahaasan

---

Lalu membuat file bernama **_check-circuit-breaker.py_** dengan isi:

```
import pybreaker
import requests

breaker = pybreaker.CircuitBreaker(fail_max=4, reset_timeout=20)

@breaker
def make_http_request(url):
    print(f"Attempting to access {url}...")
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    print(f"Successfully accessed {url}")
    return response.text

try:
    content = make_http_request("http://localhost:44777")
    # Process the content
except Exception as e:
    print(e)
```

<img src="images/39_Isi_File_check-circuit-breaker_py.png" width="700">

#### Pembahasan

---

Kemudian lakukan pengujian menggunakan perintah:

```bash
python check-retry.py
```

dan

```bash
python check-circuit-breaker.py
```

#### Pembahasan

---

menguji ketika aplikasi blacksheep di port 44777 atau di localhost tidak aktif hasilnya seperti berikut:

<img src="images/40_check_retry_Before_on_blacksheep.png" width="700">

<img src="images/41_check_retry_Before_on_blacksheep.png" width="700">

#### Pembahasan

---

menguji ketika aplikasi blacksheep di port 44777 atau di localhost aktif hasilnya seperti berikut:

<img src="images/42_check_retry_After_on_blacksheep.png" width="700">

<img src="images/43_check_retry_After_on_blacksheep.png" width="700">

#### Pembahasan

---

## 📝 Kesimpulan

---

## 🗒️ Referensi
