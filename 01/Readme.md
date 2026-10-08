# Praktikum Minggu 01-Pengenalan Sistem Terdistribusi dan Terdesentralisasi - Git dan GitHub

**Mata Kuliah:** Praktikum Sistem Terdistribusi dan Terdesentralisasi
**Topik:** Git dan Github

---

# 📚 Tujuan Praktikum

Praktikum ini bertujuan untuk:

1. Memahami fungsi dasar Git dan GitHub.
2. Melakukan instalasi Git pada komputer.
3. Melakukan konfigurasi identitas pengguna Git.
4. Membuat dan mengelola repository.
5. Menghubungkan repository lokal dengan GitHub.
6. Melakukan commit dan mengunggah perubahan ke repository.
7. Memahami dasar kolaborasi menggunakan Git dan GitHub.

---

# 📚Dasar Teori

Materi yang dipelajari dalam praktikum meliputi:

1. Instalasi Git
   Pada tahap ini dilakukan instalasi Git pada komputer. Git digunakan untuk mengelola perubahan pada file dan project secara terstruktur.

2. Konfigurasi Git
   Setelah Git berhasil diinstal, dilakukan konfigurasi nama pengguna dan email. Konfigurasi ini digunakan untuk mengidentifikasi pengguna ketika melakukan commit.

3. Pengelolaan Repository
   Tahap ini membahas pembuatan dan pengelolaan repository. Repository dapat digunakan untuk menyimpan source code, dokumentasi, dan file project lainnya.

4. Repository pada Account Sendiri
   Materi ini membahas cara mengelola repository yang berada pada akun GitHub pribadi, mulai dari membuat repository sampai melakukan sinkronisasi dengan repository lokal.

5. Repository pada Organisasi
   Materi ini membahas penggunaan repository yang berada dalam organisasi. Repository organisasi dapat digunakan ketika beberapa pengguna bekerja dalam satu kelompok atau project.

6. Kolaborasi
   Tahap terakhir membahas penggunaan Git dan GitHub untuk bekerja secara bersama-sama dalam sebuah project. Setiap anggota dapat melakukan perubahan pada project dan mengelola perubahan tersebut menggunakan Git.

---

# ⏩ PEMBAHASAN PRAKTIKUM

## PRAKTIK 1 - INSTALASI GIT

### 1. Download Git dari web resmi

   <img src="images/01_Install_Git.png" width="700">

Pembahasan :

---

### 2. Setelah download Git, double click pada file yang di-download. Akan dimunculkan lisensi. Klik install untuk lanjut.

   <img src="images/02_Install_Git.png" width="700">

Pembahasan :

---

### 3. Setelah itu, pilih lokasi instalasi. Secara default akan terisi C:\Program Files\Git. Kemudian klik Next

   <img src="images/03_Install_Git.png" width="700">

Pembahasan :

---

### 4. Pilih komponen. Tidak perlu diubah-ubah, sesuai dengan default saja. Klik pada Next

   <img src="images/04_Install_Git.png" width="700">

Pembahasan :

---

### 5. Mengisi shortcut untuk menu Start. Gunakan default (Git)

   <img src="images/05_Install_Git.png" width="700">

Pembahasan :

---

### 6. Pilih editor yang akan digunakan bersama dengan Git

   <img src="images/06_Install_Git.png" width="700">

Pembahasan :

---

### 7. Setiap melakukan inisialisasi repo Git, suatu nama branch akan diberikan. Default nama adalah master tetapi umumnya sekarang diganti dengan main. Ubahlah konfigurasi tersebut:

   <img src="images/07_Install_Git.png" width="700">

Pembahasan :

---

### 8. Pada saat instalasi, Git menyediakan akses git melalui Bash maupun command prompt. Pilih pilihan kedua supaya bisa menggunakan dari dua antarmuka tersebut. Bash adalah shell di Linux. Dengan menggunakan bash di Windows, pekerjaan di command line Windows bisa dilakukan menggunakan bash - termasuk ekskusi dari Git.

   <img src="images/08_Install_Git.png" width="700">

Pembahasan :

---

### 9. Pilih native Windows Secure Channel library HTTPS. Git menggunakan https untuk akes ke repo GitHub atau repo-repo lain (GitLab, Assembla).

   <img src="images/09_Install_Git.png" width="700">

Pembahasan :

---

### 10. Pilih pilihan pertama untuk konversi akhir baris (CR-LF).

   <img src="images/10_Install_Git.png" width="700">

Pembahasan :

---

### 11. Pilih MinTTY untuk terminal yang digunakan untuk mengakses Git Bash.

   <img src="images/11_Install_Git.png" width="700">

Pembahasan :

---

### 12. Tetapkan perilaku standar dari git pull. Pilih default saja yaitu Fast-forward or merge.

   <img src="images/12_Install_Git.png" width="700">

Pembahasan :

---

### 13. Memilih credential helper.

   <img src="images/13_Install_Git.png" width="700">

Pembahasan :

---

### 14. Untuk opsi ekstra, pilih serta aktifkan file system caching.

   <img src="images/14_Install_Git.png" width="700">

Pembahasan :

---

### 15. Setelah itu proses instalasi akan dilakukan.

   <img src="images/15_Install_Git.png" width="700">

tunggu hingga proses intalasi selesai. Setelah proses selesai, lalu klik: **Finish**

   <img src="images/16_Install_Git.png" width="700">

---

### 16. Mengecek Instalasi Git

   <img src="images/17_Install_Git.png" width="700">

---

### 17. Mengecek Versi git

```
git --version
```

   <img src="images/18_Install_Git.png" width="700">

---

## PRAKTIK 2 - KONFIGURASI GIT

### 1. Konfigurasi Username

```
git config --global user.name "Nama Anda di GitHub"
```

<img src="images/01_Konfigurasi_Git.png" width="700">

---

### 2. Membuat Konfigurasi Email

```
git config --global user.email email@domain.tld
```

<img src="images/02_Konfigurasi_Git.png" width="700">

---

### 3. Melihat Konfigurasi

```
cat ~/.gitconfig
```

<img src="images/03_Konfigurasi_Git.png" width="700">

---

```
git config --list
```

<img src="images/03_Konfigurasi_Git.png" width="700">

## PRAKTIK 3 - MENGELOLA REPO SENDIRI

### 1. Klik tanda + pada bagian atas setelah login, pilih **_New repository_**

<img src="images/01_Repo_Sendiri.png" width="700">

---

### 2. Isikan nama, keterangan, serta lisensi.

<img src="images/02_Repo_Sendiri.png" width="700">

Pembahasan :

---

### 3. Hasil Pembuatan Repository

<img src="images/04_Repo_Sendiri.png" width="700">

Pembahasan :

---

### 4. Clone Repo

Gunakan perintah

```
git clone <URL Link Repo>
```

Contoh :

<img src="images/05_Repo_Sendiri.png" width="700">

Pembahasan :

---

### 5. Masuk ke Folder Repository

Setelah meng-clone repository tadi, masuk ke folder repoitory menggunakan perintah:

```
cd nama-repository
```

Contoh :

```
cd .\prac-dis-dec-Membuat-Repository\
```

<img src="images/06_Repo_Sendiri.png" width="700">

Pembahasan :

---

### 6. Mengubah Isi dengan Branching and Merging

<img src="images/07_Repo_Sendiri.png" width="700">

<img src="images/08_Repo_Sendiri.png" width="700">

---

# 📝 Kesimpulan

Praktikum Git dan GitHub memberikan pemahaman dasar mengenai pengelolaan project menggunakan version control. Git digunakan untuk mencatat dan mengelola perubahan pada project, sedangkan GitHub digunakan untuk menyimpan repository secara online dan mendukung proses kolaborasi.

🗒️ Referensi

Materi praktikum mengacu pada dokumentasi Git dan GitHub serta materi petunjuk penggunaan Git dan GitHub dari repository NEO-X-School (https://github.com/NEO-X-School/notes/tree/main/petunjuk-git-github).

```

```
