# Praktikum Minggu 06 - Distributed File System - HDFS

<p align="justify"><strong>Mata Kuliah:</strong> Praktikum Sistem Terdistribusi dan Terdesentralisasi</p>

<p align="justify"><strong>Topik:</strong> Distributed File System - HDFS</p>

---

## 🎯 Tujuan Praktikum

---

## 📚 Dasar Teori

---

## 📜 PEMBAHASAN TUGAS

### 0. Pengantar

**1. Carilah berbagai contoh vendor/komunitas SaaS, PaaS, dan laaS masing-masing 1 saja**

#### Pembahasan

Contoh vendor atau komunitas SaaS, PaaS, dan laaS:

- SaaS (Software as a Service): Nextcloud (Komunitas Open Source) atau Google Workspace (Vendor Komersial).

- PaaS (Platform as a Service): Heroku (Salesforce) atau Dokku (Komunitas Open Source).

- IaaS (Infrastructure as a Service): Amazon Web Services (AWS) atau OpenStack (Komunitas Open Source).

---

**2. Uraikan apa yang menjadi service dari berbagai vendor untuk berbagai kategori XaaS tersebut**

#### Pembahasan

- **_SaaS - Google Workspace_**
  - **Layanan Utama**: Menyediakan paket aplikasi produktivitas dan kolaborasi berbasis cloud yang siap pakai langsung melalui browser tanpa perlu instalasi atau pemeliharaan server oleh pengguna (seperti Gmail, Google Docs, Google Drive, dan Google Meet).
  - **Cakupan Pengelolaan**: Seluruh lapisan sistem, mulai dari infrastruktur fisik, sistem operasi, keamanan data, pembaruan fitur hingga antarmuka aplikasi dikelola sepenuhnya oleh pihak Google.

- **_PaaS — Heroku_**
  - **Layanan Utama**: Menyediakan lingkungan runtime dan platform deployment aplikasi yang terkelola (seperti dukungan bahasa Python, Node.js, Go, layanan database PostgreSQL terkelola, serta integrasi Git push otomatis).
  - **Cakupan Pengelolaan**: Heroku mengelola infrastruktur server, jaringan, sistem operasi, container runtime (Dyno), dan middleware.

- **_IaaS — Amazon Web Services (AWS EC2 & VPC)_**
  - **Layanan Utama**: Menyediakan sumber daya infrastruktur komputasi dasar secara virtual melalui internet, meliputi mesin virtual (Amazon EC2), penyimpanan blok dan objek (Amazon EBS / S3), serta jaringan virtual (Amazon VPC).
  - **Cakupan Pengelolaan**: AWS bertanggung jawab atas pusat data fisik, perangkat keras server, jaringan fisik, dan lapisan virtualisasi (hypervisor).

---

**3. Jelaskan secara umum arsitektur dari XaaS tersebut dalam bentuk visualisasi gambar.**

<img src="images/00_Jawaban_Tugas_Nomor_3.jpeg" width="700">

#### Pembahasan

---

Selanjutnya mengclone repository github https://github.com/pallets/flask

Gunakan perintah

```bash
git clone https://github.com/pallets/flask
```

<img src="images/01_Clone_Github_Repository.png" width="700">

#### Pembahasan

---

Kemudian mengcopy direktori ke direktori tertentu

```bash
cp -R ~/Desktop/flask/examples/tutorial flask-app
```

<img src="images/02_Copy_Direktori.png" width="700">

#### Pembahasan

---

Selanjutnya cek isi file pada direktori dengan perintah

```bash
ls -la
```

<img src="images/03_Cek_Direktory.png" width="700">

#### Pembahasan

---

## ⏩ PEMBAHASAN PRAKTIKUM

### 1. Membuat env Python 3.14.4

Buat env untuk keperluan mata kuliah pertemuan ini. Python yang digunakan adalah Python versi 3.14.4.

Gunakan perintah

```bash
uv venv --python 3.14.4
```

<img src="images/04_Atur_Env_Python_3_14_4.png" width="700">

#### Pembahasan

---

Lalu mengaktifkan virtual environment

```bash
source .venv/Scripts/activate
```

<img src="images/05_Mengaktifkan_Env.png" width="700">

#### Pembahasan

---

Kemudian memeriksa isi folder

```bash
ls -la
```

<img src="images/06_Cek_Isi_Folder.png" width="700">

#### Pembahasan

---

### 2. Install Paket yang Diperlukan

Install paket yang diperlukan terlebih dahulu menggunakan perintah

```bash
uv pip install -e .
```

<img src="images/07_Install_Paket_Yang_Diperlukan.png" width="700">

#### Pembahasan

---

Kemudian lakukan inisialisasi database aplikasi dengan perintah

```bash
flask --app flaskr init-db
```

<img src="images/08_Inisialisasi_Database.png" width="700">

#### Pembahasan

---

Lalu menjalankan server web Flask dengan perintah

```bash
flask --app flaskr run
```

<img src="images/09_Menjalankan_Server.png" width="700">

Kita bisa melihat aplikasi yang berjalan pada browser:

<img src="images/10_Menjalankan_Server.png" width="700">

#### Pembahasan

---

Untuk mencoba, pilih “Register” kemudian “Log In”

<img src="images/11_Mencoba_Browser.png" width="700">

Kemudian Login dan masukan data yang telah didaftarkan sebelumnya

<img src="images/12_Mencoba_Login.png" width="700">

Setelah login tampilan nya akan berubah menjadi seperti ini

<img src="images/13_Hasil_Login.png" width="700">

#### Pembahasan

---

### 3. Buat Aplikasi Menjadi CA - Docker

Buat File DockerFile terlebih dahulu pada direktori flask-app dengan perintah

```bash
touch Dockerfile
```

<img src="images/14_Buat_Docker_File.png" width="700">

#### Pembahasan

---

Kemudian isi file DockerFile dengan kode

```
FROM python:3.14
RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -e .
RUN flask --app flaskr init-db
EXPOSE 5000
CMD ["flask", "--app", "flaskr", "run", "--host=0.0.0.0", "--port=5000"]
```

<img src="images/15_Buat_Aplikasi_Menjadi_CA_Docker.png" width="700">

#### Pembahasan

---

Lalu Build Docker Image gunakan perintah

```bash
docker build -f Dockerfile -t flaskr:1.0.0 .
```

<img src="images/16_Build_Docker_Image.png" width="700">

#### Pembahasan

---

Kemudian periksa daftar Docker Image dengan perintah

```bash
docker image ls
```

<img src="images/17_Daftar_Docker_Image.png" width="700">

#### Pembahasan

---

jika ada banyak image container di node, hapus yang tidak digunakan lagi dengan mengacu pada ID dari image tersebut dengan perintah

```bash
docker rmi <ID_IMAGE>
```

Contoh:

 <img src="images/18_Hapus_Image_DockerFile.png" width="700">

#### Pembahasan

---

Kemudian tampilkan daftar docker image after dilakukan beberapa penghapusan

<img src="images/19_Daftar_Docker_Lanjutan.png" width="700">

#### Pembahasan

---

### 4. Menjalankan Image

Jalankan dengan memetakan port 5000 pada aplikasi di container ke port 5001 di localhost:

Gunakan perintah

```bash
docker run -p 5001:5000 flaskr:1.0.0
```

<img src="images/20_Menjalankan_Tugas.png" width="700">

#### Pembahasan

---

Kemudian akses web browser pada http://localhost:5001

<img src="images/21_Menjalankan_Tugas_Browser.png" width="700">

#### Pembahasan

---

Lalu di terminal tempat menjalankan Tugas akan muncul

<img src="images/22_Tampilan_Terminal_After_Open_Browser.png" width="700">

#### Pembahasan

---

### 4. Buat Aplikasi Menjadi CA - Podman

Jika menggunakan Podman, maka dockerd tidak perlu diaktifkan. Jika dockerd aktif, matikan service-nya terlebih dahulu

Kemudian install Podman terlebih dahulu dengan perintah

```bash
winget install RedHat.Podman
```

<img src="images/23_Install_Podman.png" width="700">

#### Pembahasan

---

Kemudian nyalakan mesin Podman dengan cara memanggil lokasi instalasi bawaan Podman dengan perintah

```bash
"/c/Program Files/RedHat/Podman/podman.exe" machine init
```

<img src="images/24_Memanggil_lokasi_instalasi_Bawaan_Podman.png" width="700">

dan

```bash
"/c/Program Files/RedHat/Podman/podman.exe" machine start
```

<img src="images/25_Menjalankan_Lokasi_Instalasi_Bawaan_Podman.png" width="700">

#### Pembahasan

---

Lalu membangun image dengan perintah

```bash
podman build -f Dockerfile -t flaskr:1.0.0 .
```

<img src="images/26_Membangun_Image.png" width="700">

<img src="images/27_Membangun_Image_Lanjutan.png" width="700">

#### Pembahasan

---

Kemudian periksa daftar image podman

<img src="images/28_Periksa_Daftar_Image_Podman.png" width="700">

#### Pembahasan

---

Lalu Jalankan Podman pada port 5001 dengan perintah

```bash
podman run -p 5001:5000 flaskr:1.0.0
```

<img src="images/29_Menjalankan_Podman.png" width="700">

#### Pembahasan

---

Kemudian cek hasil nya pada http://127.0.0.1:5001 di browser

<img src="images/30_Open_Browser.png" width="700">

#### Pembahasan

---

## 📝 Kesimpulan

---

## 🗒️ Referensi
