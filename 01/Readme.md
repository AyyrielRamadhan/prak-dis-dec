# Praktikum Minggu 01 - Pengenalan Sistem Terdistribusi dan Terdesentralisasi - Git dan GitHub

**Mata Kuliah:** Praktikum Sistem Terdistribusi dan Terdesentralisasi
**Topik:** Git dan Github

---

# 📚 Tujuan Praktikum

Praktikum ini dirancang agar kita benar-benar paham cara kerja Git dan GitHub, bukan sekadar hafal perintah. Kita mulai dari hal paling dasar: mengenal fungsi Git sebagai version control system dan GitHub sebagai platform penyimpanan repository di cloud. Dari situ, kita lanjut ke instalasi Git di komputer masing-masing — karena tanpa ini, tidak ada yang bisa dilakukan.

Setelah Git terinstall, kita perlu mengkonfigurasi identitas (nama dan email) agar setiap perubahan yang kita buat bisa dilacak siapa yang membuatnya. Ini penting terutama saat nanti bekerja dalam tim. Selanjutnya kita belajar membuat dan mengelola repository, baik yang ada di komputer lokal maupun yang ada di GitHub. Kita juga belajar menghubungkan keduanya sehingga perubahan di komputer lokal bisa diunggah ke GitHub.

Yang tidak kalah pentingnya adalah memahami mekanisme commit — bagaimana Git menyimpan setiap perubahan secara terstruktur — dan bagaimana cara mengunggah perubahan tersebut ke repository remote. Terakhir, kita kenalan dengan dasar kolaborasi: bagaimana beberapa orang bisa bekerja dalam satu proyek tanpa saling menimpa pekerjaan masing-masing.

---

# 📚 Dasar Teori

**Instalasi Git**

Git adalah version control system — alat yang mencatat setiap perubahan yang kita buat pada file atau proyek. Tanpa Git, kita akan kesulitan melacak apa yang sudah diubah, siapa yang mengubahnya, dan kapan perubahan itu terjadi. Di tahap ini kita menginstall Git di komputer agar bisa mulai menggunakan semua fiturnya. Proses instalasinya tidak rumit, tetapi ada beberapa pilihan konfigurasi yang perlu dipahami supaya tidak salah langkah.

**Konfigurasi Git**

Setelah Git terinstall, hal pertama yang wajib dilakukan adalah mengatur identitas: nama dan email. Kenapa? Karena setiap kali kita melakukan commit (menyimpan perubahan ke Git), Git akan menyimpan informasi siapa yang membuat perubahan itu. Tanpa konfigurasi ini, commit tidak akan tercatat dengan benar. Konfigurasi ini cukup dilakukan sekali dan akan tersimpan di file `.gitconfig`.

**Pengelolaan Repository**

Repository (sering disingkat repo) adalah tempat penyimpanan untuk semua file dan riwayat perubahan dalam sebuah proyek. Satu repo biasanya digunakan untuk satu proyek tertentu. Repo bisa ada di komputer lokal maupun di GitHub, dan keduanya bisa disinkronkan. Di tahap ini kita belajar cara membuat repo, mengisinya dengan file, dan mengelola perubahan di dalamnya.

**Repository pada Account Sendiri**

Repo bisa dibuat di akun GitHub pribadi kita. Repo seperti ini biasanya untuk proyek pribadi atau pembelajaran. Kita bisa mengaturnya sebagai public (semua orang bisa melihat) atau private (hanya orang yang diberi akses). Prosesnya dimulai dari membuat repo di GitHub, lalu meng-clone-nya ke komputer lokal agar bisa dikerjakan secara offline, dan terakhir meng-push perubahan kembali ke GitHub.

**Repository pada Organisasi**

Selain di akun pribadi, repo juga bisa dibuat di dalam organisasi di GitHub. Organisasi berguna ketika sebuah proyek dikerjakan oleh beberapa orang dalam satu tim. Semua anggota organisasi bisa mengakses repo yang ada di dalamnya. Cara mengelola repo organisasi sebenarnya sama dengan repo pribadi — bedanya hanya pada siapa yang memiliki akses dan siapa yang bertanggung jawab atas repo tersebut.

**Kolaborasi**

Ini bagian yang paling menarik: bagaimana beberapa orang bisa bekerja dalam satu proyek tanpa saling mengganggu. Git punya mekanisme branching — setiap orang bisa membuat cabang sendiri untuk bekerja, lalu menggabungkannya kembali ke cabang utama setelah selesai. GitHub menambahkan fitur pull request, yaitu mekanisme untuk meminta pemilik repo meninjau dan menyetujui perubahan sebelum digabungkan. Dengan cara ini, kualitas kode tetap terjaga meski banyak orang berkontribusi.

---

# ⏩ PEMBAHASAN PRAKTIKUM

## PRAKTIK 1 - INSTALASI GIT

### 1. Download Git dari web resmi

   <img src="images/01_Install_Git.png" width="700">

Pembahasan :

Langkah pertama adalah mengunduh installer Git dari situs resminya di git-scm.com. Penting untuk mengambil installer dari sumber resmi agar mendapatkan versi yang terbaru dan aman. Di halaman download, pilih installer sesuai sistem operasi yang digunakan — dalam hal ini Windows. File yang diunduh biasanya berformat .exe dan ukurannya sekitar 50-60 MB.

---

### 2. Setelah download Git, double click pada file yang di-download. Akan dimunculkan lisensi. Klik install untuk lanjut.

   <img src="images/02_Install_Git.png" width="700">

Pembahasan :

Setelah file installer diunduh, double click untuk menjalankannya. Yang pertama muncul adalah halaman lisensi — ini adalah perjanjian penggunaan software. Lisensi Git adalah GPL (General Public License), yang berarti Git adalah software open source yang bebas digunakan. Klik **Next** untuk melanjutkan ke langkah berikutnya.

---

### 3. Setelah itu, pilih lokasi instalasi. Secara default akan terisi C:\Program Files\Git. Kemudian klik Next

   <img src="images/03_Install_Git.png" width="700">

Pembahasan :

Di langkah ini kita diminta memilih folder tempat Git akan diinstall. Secara default, installer menyarankan lokasi `C:\Program Files\Git`. Ini adalah lokasi standar untuk aplikasi di Windows, jadi tidak perlu diubah. Yang perlu diingat: setelah instalasi selesai, Git akan bisa diakses dari command prompt atau Git Bash dari direktori mana saja.

---

### 4. Pilih komponen. Tidak perlu diubah-ubah, sesuai dengan default saja. Klik pada Next

   <img src="images/04_Install_Git.png" width="700">

Pembahasan :

Halaman ini menampilkan komponen-komponen Git yang akan diinstall. Secara default, semua komponen penting sudah dicentang — seperti Git Bash, Git GUI, dan integrasi dengan Windows Explorer. Tidak ada yang perlu diubah di sini. Cukup klik **Next** dan lanjutkan.

---

### 5. Mengisi shortcut untuk menu Start. Gunakan default (Git)

   <img src="images/05_Install_Git.png" width="700">

Pembahasan :

Di sini kita diminta memberi nama shortcut untuk menu Start. Default-nya adalah "Git", yang sudah cukup jelas dan mudah dicari. Tidak perlu diubah — cukup klik **Next** saja.

---

### 6. Pilih editor yang akan digunakan bersama dengan Git

   <img src="images/06_Install_Git.png" width="700">

Pembahasan :

Git membutuhkan editor teks untuk menulis pesan commit atau menyelesaikan konflik saat merge. Di langkah ini kita memilih editor mana yang akan dipakai. Jika sudah menginstall Visual Studio Code atau Notepad++, bisa memilih salah satunya. Jika tidak yakin, pilih saja editor default (Vim) — nanti tetap bisa diubah lagi melalui konfigurasi Git.

---

### 7. Setiap melakukan inisialisasi repo Git, suatu nama branch akan diberikan. Default nama adalah master tetapi umumnya sekarang diganti dengan main. Ubahlah konfigurasi tersebut:

   <img src="images/07_Install_Git.png" width="700">

Pembahasan :

Branch adalah cabang dalam repo — setiap repo punya satu branch utama. Dulu, nama default branch utama adalah "master", tetapi sekarang industri beralih ke "main" sebagai standar baru. Di langkah ini kita mengubah pilihan dari "master" ke "main" agar repo yang nanti kita buat langsung menggunakan nama branch yang sesuai dengan kebiasaan saat ini.

---

### 8. Pada saat instalasi, Git menyediakan akses git melalui Bash maupun command prompt. Pilih pilihan kedua supaya bisa menggunakan dari dua antarmuka tersebut. Bash adalah shell di Linux. Dengan menggunakan bash di Windows, pekerjaan di command line Windows bisa dilakukan menggunakan bash - termasuk ekskusi dari Git.

   <img src="images/08_Install_Git.png" width="700">

Pembahasan :

Git bisa diakses melalui dua antarmuka di Windows: Command Prompt (cmd) dan Git Bash. Git Bash adalah shell yang meniru lingkungan Linux — perintah-perintah Linux bisa langsung dipakai di Windows. Dengan memilih opsi kedua, kita bisa menggunakan Git dari keduanya. Ini berguna karena beberapa perintah Git lebih mudah dijalankan di Git Bash, sementara yang lain cukup lewat Command Prompt biasa.

---

### 9. Pilih native Windows Secure Channel library HTTPS. Git menggunakan https untuk akes ke repo GitHub atau repo-repo lain (GitLab, Assembla).

   <img src="images/09_Install_Git.png" width="700">

Pembahasan :

Git berkomunikasi dengan repo remote (seperti GitHub) melalui protokol HTTPS. Di langkah ini kita memilih library yang akan digunakan untuk koneksi HTTPS tersebut. Pilihan "native Windows Secure Channel library" berarti Git akan menggunakan sistem keamanan bawaan Windows — ini pilihan yang paling stabil dan kompatibel untuk pengguna Windows.

---

### 10. Pilih pilihan pertama untuk konversi akhir baris (CR-LF).

   <img src="images/10_Install_Git.png" width="700">

Pembahasan :

Windows dan Linux menggunakan karakter berbeda untuk menandai akhir baris (line ending). Windows menggunakan CR+LF, sedangkan Linux hanya LF. Jika tidak dikonversi dengan benar, file yang diedit di Windows bisa terlihat berantakan saat dibuka di Linux, dan sebaliknya. Pilihan pertama memastikan Git secara otomatis mengkonversi line ending agar file tetap konsisten lintas platform.

---

### 11. Pilih MinTTY untuk terminal yang digunakan untuk mengakses Git Bash.

   <img src="images/11_Install_Git.png" width="700">

Pembahasan :

MinTTY adalah emulator terminal ringan yang digunakan untuk menjalankan Git Bash. Terminal ini mendukung fitur-fitur modern seperti resize window, copy-paste, dan tampilan yang lebih baik dibanding terminal bawaan Windows. Pilih MinTTY agar pengalaman menggunakan Git Bash lebih nyaman.

---

### 12. Tetapkan perilaku standar dari git pull. Pilih default saja yaitu Fast-forward or merge.

   <img src="images/12_Install_Git.png" width="700">

Pembahasan :

`git pull` adalah perintah untuk mengambil perubahan dari repo remote dan menggabungkannya ke branch lokal. Ada beberapa strategi penggabungan, tetapi default "Fast-forward or merge" adalah yang paling umum dan aman untuk pemula. Jangan diubah dulu — nanti di praktikum lanjutan kita akan mempelajari strategi-strategi ini lebih dalam.

---

### 13. Memilih credential helper.

   <img src="images/13_Install_Git.png" width="700">

Pembahasan :

Credential helper adalah komponen yang menyimpan kredensial login kita saat mengakses repo remote. Tanpa ini, kita akan diminta memasukkan username dan password setiap kali melakukan push atau pull. Dengan credential helper, kredensial disimpan secara aman sehingga kita tidak perlu login berulang kali. Pilih default (Git Credential Manager) — ini yang paling mudah dan aman untuk pemula.

---

### 14. Untuk opsi ekstra, pilih serta aktifkan file system caching.

   <img src="images/14_Install_Git.png" width="700">

Pembahasan :

File system caching adalah fitur yang membuat Git lebih cepat dalam membaca dan menulis file. Secara default, Git memeriksa setiap file satu per satu — dengan caching, proses ini dioptimalkan sehingga operasi Git (seperti `git status` atau `git add`) terasa lebih responsif, terutama di repo yang besar. Centang opsi ini untuk performa yang lebih baik.

---

### 15. Setelah itu proses instalasi akan dilakukan.

   <img src="images/15_Install_Git.png" width="700">

tunggu hingga proses intalasi selesai. Setelah proses selesai, lalu klik: **Finish**

   <img src="images/16_Install_Git.png" width="700">

Pembahasan :

Sekarang installer mulai menyalin file-file Git ke komputer. Proses ini biasanya memakan waktu 1-3 menit tergantung kecepatan komputer. Setelah selesai, klik **Finish** untuk menutup installer. Git sekarang sudah terinstall dan siap digunakan.

---

### 16. Mengecek Instalasi Git

   <img src="images/17_Install_Git.png" width="700">

Pembahasan :

Setelah instalasi selesai, kita perlu memastikan bahwa Git benar-benar terinstall dengan benar. Caranya mudah: buka Command Prompt atau Git Bash, lalu ketik perintah `git`. Jika Git terinstall dengan benar, akan muncul daftar perintah-perintah Git yang tersedia. Jika tidak, mungkin ada masalah pada PATH environment variable.

---

### 17. Mengecek Versi git

```
git --version
```

   <img src="images/18_Install_Git.png" width="700">

Pembahasan :

Perintah `git --version` digunakan untuk memeriksa versi Git yang terinstall. Jika muncul output seperti `git version 2.xx.x`, berarti instalasi berhasil. Versi yang muncul bisa berbeda-beda tergantung kapan Git diunduh — yang penting adalah perintah ini merespons tanpa error. Jika muncul pesan "command not found", berarti Git belum terinstall dengan benar atau PATH belum dikonfigurasi.

---

## PRAKTIK 2 - KONFIGURASI GIT

### 1. Konfigurasi Username

```
git config --global user.name "Nama Anda di GitHub"
```

<img src="images/01_Konfigurasi_Git.png" width="700">

Pembahasan :

Perintah ini mengatur nama yang akan tercantum di setiap commit yang kita buat. Gunakan nama yang sama dengan nama di akun GitHub agar mudah dikenali. Opsi `--global` berarti konfigurasi ini berlaku untuk semua repo di komputer ini — tidak perlu diatur ulang untuk setiap proyek baru.

---

### 2. Membuat Konfigurasi Email

```
git config --global user.email email@domain.tld
```

<img src="images/02_Konfigurasi_Git.png" width="700">

Pembahasan :

Sama seperti username, email juga akan tercantum di setiap commit. Gunakan email yang sama dengan email yang didaftarkan ke akun GitHub. Ini penting karena GitHub menggunakan email untuk mencocokkan commit dengan akun kita — jika email tidak cocok, commit tidak akan terhubung ke profil GitHub kita.

---

### 3. Melihat Konfigurasi

```
cat ~/.gitconfig
```

<img src="images/03_Konfigurasi_Git.png" width="700">

Pembahasan :

Perintah `cat ~/.gitconfig` menampilkan isi file konfigurasi Git. Di sini kita bisa melihat nama dan email yang sudah diatur sebelumnya. File `.gitconfig` tersimpan di folder home user dan berisi semua konfigurasi global Git.

---

```
git config --list
```

<img src="images/03_Konfigurasi_Git.png" width="700">

Pembahasan :

Perintah `git config --list` menampilkan semua konfigurasi Git yang aktif, termasuk yang bawaan dari sistem. Outputnya lebih lengkap daripada `cat ~/.gitconfig` karena mencakup konfigurasi dari berbagai sumber. Jika kita berada di dalam folder repo Git, outputnya akan menampilkan konfigurasi khusus repo tersebut juga.

---

## PRAKTIK 3 - MENGELOLA REPO SENDIRI

### 1. Klik tanda + pada bagian atas setelah login, pilih **_New repository_**

<img src="images/01_Repo_Sendiri.png" width="700">

Pembahasan :

Setelah login ke GitHub, kita bisa membuat repository baru dengan mengklik tanda **+** di pojok kanan atas halaman. Dari menu yang muncul, pilih **New repository**. Ini adalah langkah awal untuk membuat tempat penyimpanan proyek kita di GitHub.

---

### 2. Isikan nama, keterangan, serta lisensi.

<img src="images/02_Repo_Sendiri.png" width="700">

Pembahasan :

Di halaman ini kita mengisi detail repository: nama repo, deskripsi singkat, dan lisensi. Nama repo sebaiknya deskriptif dan mudah diingat. Lisensi menentukan bagaimana orang lain boleh menggunakan kode kita — untuk pembelajaran, bisa memilih MIT License atau tidak memilih lisensi sama sekali. Juga ada opsi untuk membuat repo private (hanya bisa diakses oleh kita) atau public (semua orang bisa melihat).

---

### 3. Hasil Pembuatan Repository

<img src="images/04_Repo_Sendiri.png" width="700">

Pembahasan :

Setelah semua isian lengkap, klik **Create repository**. GitHub akan langsung membuat repo dan menampilkan halaman repo tersebut. Jika kita memilih opsi default (tanpa README, .gitignore, atau LICENSE), repo akan kosong dan GitHub akan menampilkan petunjuk untuk mulai mengisi repo dari command line.

---

### 4. Clone Repo

Gunakan perintah

```
git clone <URL Link Repo>
```

Contoh :

<img src="images/05_Repo_Sendiri.png" width="700">

Pembahasan :

`git clone` adalah perintah untuk menduplikasi repo dari GitHub ke komputer lokal. URL repo bisa ditemukan di halaman repo GitHub — klik tombol **Code** lalu salin URL HTTPS. Setelah perintah ini dijalankan, akan muncul folder baru di komputer yang berisi salinan repo tersebut. Di dalam folder itu ada folder tersembunyi `.git` yang menyimpan semua riwayat perubahan.

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

Setelah clone selesai, kita perlu masuk ke folder repo untuk mulai bekerja. Perintah `cd` (change directory) digunakan untuk berpindah ke folder tersebut. Setelah masuk, semua perintah Git yang kita jalankan akan berlaku di repo ini. Untuk memastikan kita sudah di folder yang benar, bisa cek dengan perintah `ls` (Linux/Mac) atau `dir` (Windows).

---

### 6. Mengubah isi dengan Branching and Merging

<img src="images/07_Repo_Sendiri.png" width="700">

<img src="images/08_Repo_Sendiri.png" width="700">

Pembahasan :

Branching and merging adalah cara aman melakukan perubahan. Alih-alih langsung mengedit file di branch utama (main), kita membuat branch baru — semacam "cabang" terpisah — untuk menampung perubahan. Setelah perubahan selesai dan diuji, branch tersebut digabungkan kembali ke main melalui pull request. Cara ini lebih terstruktur dan memungkinkan orang lain meninjau perubahan sebelum akhirnya masuk ke branch utama. Di GitHub, proses ini dilakukan dengan membuat branch, push ke repo, lalu membuat pull request untuk menggabungkannya.

---

# 📝 Kesimpulan

Setelah mengikuti seluruh rangkaian praktikum ini, saya jadi paham bahwa Git dan GitHub bukan sekadar tools untuk menyimpan file — mereka adalah fondasi cara kerja pengembangan software modern. Git mencatat setiap perubahan secara terstruktur sehingga kita bisa melacak riwayat proyek, kembali ke versi sebelumnya jika ada kesalahan, dan bekerja tanpa takut merusak file yang sudah ada. GitHub menambahkan dimensi kolaborasi: repo bisa diakses dari mana saja, perubahan bisa ditinjau sebelum digabungkan, dan beberapa orang bisa bekerja dalam satu proyek tanpa saling menimpa.

Kesimpulannya, Git dan GitHub adalah keterampilan dasar yang wajib dimiliki siapa pun yang terjun ke pengembangan software. Praktikum ini memberikan fondasi yang kuat untuk memahami version control dan kolaborasi tim.

---

## 🗒️ Referensi

Materi praktikum mengacu pada dokumentasi Git dan GitHub serta materi petunjuk penggunaan Git dan GitHub dari repository NEO-X-School (https://github.com/NEO-X-School/notes/tree/main/petunjuk-git-github).
