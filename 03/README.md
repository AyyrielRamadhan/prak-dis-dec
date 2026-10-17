# Praktikum Minggu 03 - Sinkronisasi pada Sistem Terdistribusi

**Mata Kuliah:** Praktikum Sistem Terdistribusi dan Terdesentralisasi
**Topik:** Sinkronisasi pada Sistem Terdistribusi

---

# 📚 Tujuan Praktikum

<p align="justify">1. Memahami cara kerja sinkronisasi waktu menggunakan protokol NTP melalui tools NetTime di Windows.</p>

<p align="justify">2. Memahami konsep Vector Clock untuk pengurutan event dalam sistem terdistribusi.</p>

<p align="justify">3. Memahami masalah yang muncul tanpa sinkronisasi: data race dan deadlock, serta cara mencegah dan menyelesaikannya.</p>

<p align="justify">4. Memahami algoritma Raft untuk mencapai konsensus dalam pemilihan leader pada sistem terdistribusi.</p>

---

# 📚 Dasar Teori

<p align="justify">Sinkronisasi adalah fondasi penting dalam sistem terdistribusi. Tanpa sinkronisasi, berbagai masalah bisa muncul mulai dari ketidakakuratan waktu hingga kehilangan data.</p>

<p align="justify"><em>Sinkronisasi Waktu</em> Dalam sistem terdistribusi, setiap node memiliki clock fisik yang berbeda dan tidak selalu akurat. Protokol NTP (Network Time Protocol) digunakan untuk menyinkronkan jam komputer dengan server waktu pusat. Algoritma Marzullo digunakan di dalam NTP untuk memilih sumber waktu yang paling akurat. Offset dan lag adalah dua metrik utama untuk mengukur perbedaan jam lokal dengan server.</p>

<p align="justify"><strong>Vector Clock.</strong> Vector Clock diperkenalkan oleh Leslie Lamport untuk menangkap hubungan sebab-akibat antar event dalam sistem terdistribusi tanpa bergantung pada clock fisik. Setiap proses menyimpan vektor berisi counter untuk setiap proses dalam sistem. Aturan: event lokal menambah counter sendiri, pengiriman pesan menambah counter lalu mengirim salinan, dan penerimaan pesan mengambil nilai maksimal tiap elemen sebelum menambah counter sendiri.</p>

<p align="justify"><strong>Data Race &amp; Deadlock.</strong> Data race terjadi ketika dua atau lebih thread mengakses data bersamaan, minimal satu menulis, tanpa mekanisme sinkronasi. Deadlock terjadi ketika dua atau lebih thread saling menunggu lock yang dipegang thread lain (circular wait). Kondisi yang harus dipenuhi untuk deadlock: mutual exclusion, hold and wait, no preemption, dan circular wait.</p>

<p align="justify"><strong>Algoritma Raft.</strong> Raft adalah algoritma konsensus yang memastikan semua node dalam sistem terdistribusi sepakat tentang satu nilai atau leader. Raft membagi waktu menjadi term, dengan satu leader per term. Jika leader gagal, node lain memulai pemilihan dengan election timeout acak untuk menghindari split-vote. Mayoritas suara (> 50%) diperlukan untuk memilih leader baru.</p>

---

# ⏩ PEMBAHASAN PRAKTIKUM

## PRAKTIK 1 - Sinkronisasi Waktu

### 1. Install NetTime (Windows)

<p align="justify">- Klik Next untuk melanjutkan instalasi.</p>

<img src="images/01_Install_NetTime.png" width="700">

#### Pembahasan

<p align="justify">Layar pertama yang muncul setelah menjalankan installer adalah layar sambutan. Di sini tidak ada konfigurasi apa pun, wizard hanya memberi tahu bahwa kita akan memasang NetTime dan menyarankan agar menutup aplikasi lain dulu supaya proses instalasi berjalan lancar. Cukup klik Next untuk melanjutkan ke langkah berikutnya.</p>

---

<p align="justify">- Gunakan lokasi instalasi default (C:\Program Files (x86)\NetTime), lalu klik Next.</p>

<img src="images/02_Install_NetTime.png" width="700">

#### Pembahasan

<p align="justify">Di langkah ini kita memilih folder tujuan instalasi. Secara default, NetTime akan dipasang di C:\Program Files (x86)\NetTime dengan kebutuhan ruang kosong minimal 1,9 MB — sangat kecil. Karena tidak ada kebutuhan khusus, saya menggunakan pengaturan default ini dan melanjutkan dengan klik Next.</p>

---

<p align="justify">- Gunakan nama folder Start Menu default (NetTime), lalu klik Next.</p>

<img src="images/03_Install_NetTime.png" width="700">

#### Pembahasan

<p align="justify">Berikutnya, wizard menanyakan nama folder Start Menu untuk shortcut program. Default-nya sudah terisi "NetTime" dan tidak perlu diubah, jadi langsung klik Next. Langkah ini hanya menentukan di mana shortcut akan muncul di Start Menu, bukan pengaturan fungsional.</p>

---

<p align="justify">- Centang opsi "Install as Service (Recommended)" agar NetTime berjalan otomatis, lalu klik Next.</p>

<img src="images/04_Install_NetTime.png" width="700">

#### Pembahasan

<p align="justify">Di sini ada satu opsi tambahan: "Install as Service (Recommended)". Saya membiarkan opsi ini tercentang karena dengan didaftarkan sebagai Windows Service, NetTime dapat berjalan otomatis di belakang layar setiap komputer dinyalakan tanpa perlu dibuka manual. Setelah itu klik Next.</p>

---

<p align="justify">- Periksa ringkasan instalasi, lalu klik Install untuk memulai pemasangan.</p>

<img src="images/05_Install_NetTime.png" width="700">

#### Pembahasan

<p align="justify">Sebelum instalasi dimulai, wizard menampilkan ringkasan pilihan: lokasi folder instalasi, nama folder Start Menu, dan opsi Install as Service. Ini halaman konfirmasi terakhir — pastikan semuanya sudah sesuai, lalu klik Install untuk memulai proses pemasangan.</p>

---

<p align="justify">- Tunggu proses instalasi hingga selesai.</p>

<img src="images/06_Install_NetTime.png" width="700">

#### Pembahasan

<p align="justify">Proses instalasi berjalan sangat cepat karena ukuran program yang kecil. Bar hijau menunjukkan progres penyalinan file dan pendaftaran service ke Windows. Tidak ada konfigurasi tambahan di tahap ini — semuanya sudah ditentukan dari langkah-langkah sebelumnya.</p>

---

<p align="justify">- Centang "Start NetTime now", lalu klik Finish.</p>

<img src="images/07_Install_NetTime.png" width="700">

#### Pembahasan

<p align="justify">Instalasi selesai. Ada opsi "Start NetTime now" yang saya biarkan tercentang agar program langsung terbuka setelah klik Finish. Dengan begitu kita bisa langsung lanjut ke tahap konfigurasi dan sinkronisasi waktu tanpa harus mencarinya secara manual.</p>

---

### 2. Proses Sinkronisasi

<img src="images/08_Sinkronisasi_NetTime.png" width="700">

<img src="images/09_Sinkronisasi_NetTime.png" width="700">

#### Pembahasan

<p align="justify">Gambar pertama menunjukkan kondisi awal: "Last Attempt: No attempt yet", "Last Sync: No synchronization yet", dan service belum jalan (tombol Start masih aktif). Kita klik Start untuk mengaktifkan service. Pada gambar kedua, service sudah berjalan dan melakukan sinkronisasi ke server NTP 0.nettime.pool.ntp.org. Terlihat Last Sync terisi dan offset hanya +3ms dengan lag 5ms, yang berarti jam komputer sudah sangat akurat. Next Attempt sekitar 12 jam lagi, sehingga komputer akan menyesuaikan jam secara otomatis dan berkala melalui protokol NTP.</p>

---

## PRAKTIK 2 - Vector Clock

<p align="justify">- File vclocks.py — berisi class VectorClock dari modul yang dijalankan dalam simulasi 3 proses (P0, P1, P2) untuk memahami hubungan sebab-akibat antar event.</p>

<img src="images/10_vclocks_py.png" width="700">

#### Pembahasan

<p align="justify">File vclocks.py berisi class VectorClock yang merupakan inti dari praktikum ini. Di dalamnya ada beberapa method kunci: increment() untuk menambah jam lokal proses, send_message() yang mengambil salinan vector clock saat mengirim pesan, dan receive_message() yang memperbarui jam dengan mengambil nilai maksimal antara jam lokal dan jam yang diterima lalu increment. Ada juga happens_before() untuk mengecek hubungan sebab-akibat dan is_concurrent() untuk mengecek apakah dua event terjadi bersamaan. Di bawah class tersebut langsung ada simulasi 3 proses (P0, P1, P2) yang saling berinteraksi.</p>

---

<p align="justify">- Jalankan Program</p>

<img src="images/11_Output_vclocks.png" width="700">

#### Pembahasan

<p align="justify">Keluaran menunjukkan bagaimana vector clock berevolusi. Semua proses mulai dari [0,0,0]. Setelah P0 event lokal, clock-nya jadi [1,0,0]. Saat P0 kirim pesan ke P1, P0 increment jadi [2,0,0] dan P1 mengadopsi nilai maksimal lalu increment sendiri jadi [2,1,0]. P2 melakukan event lokal jadi [0,0,1]. Terakhir, P1 kirim pesan ke P2 sehingga P2 jadi [2,2,2]. Pemeriksaan kausalitas di akhir: VC0 happens before VC1 bernilai True (semua elemen VC0 ≤ VC1), dan VC0 concurrent with VC2 bernilai False karena keduanya ternyata memiliki hubungan kausal melalui rantai pesan.</p>

---

<p align="justify">- Buat modul Python untuk class VectorClock</p>

Class: vector_clock.py

<img src="images/12_VectorClock_py.png" width="700">

#### Pembahasan

<p align="justify">Setelah memahami vclocks.py, saya membuat ulang kode tersebut menjadi modul sendiri di vector_clock.py. Logika dan method di dalamnya sama persis, hanya saja saya rapikan formatnya dan ganti docstring ke bahasa Indonesia. Karena sekarang menjadi modul terpisah, class VectorClock bisa di-import dan dipakai dari file lain tanpa perlu menyalin seluruh kode.</p>

---

<p align="justify">Class: main.py dan Output</p>

<img src="images/13_main_Vector_Clock.png" width="700">

<img src="images/14_Output_Vector_Clock.png" width="700">

#### Pembahasan

<p align="justify">Untuk membuktikan modulnya bekerja, saya membuat main.py yang meng-import VectorClock dan menjalankan simulasi yang sama seperti vclocks.py, lengkap dengan label tiap tahap supaya alurnya lebih jelas. Hasil keluarannya identik dengan program asli: dari [0,0,0] semua proses berkembang hingga [2,2,2], dan pemeriksaan kausalitas juga sama yaitu VC0 happens before VC1: True, VC1 happens before VC0: False, VC0 concurrent with VC2: False. Ini menunjukkan modul yang dibuat berfungsi benar.</p>

---

## PRAKTIK 3 - Problem Tanpa Sinkronisasi

<p align="justify">Class: multithreads-example.py</p>

<img src="images/15_multithreads-example_py.png" width="700">

#### Pembahasan

<p align="justify">Program multithreads-example.py sederhana: ada 5 thread (A sampai E), masing-masing mencetak 'starting', lalu sleep 5 detik untuk mensimulasikan tugas yang memakan waktu, dan terakhir mencetak 'finished'. Program ini mendemonstrasikan bahwa thread berjalan secara paralel, bukan satu per satu berurutan.</p>

---

<p align="justify">Jalankan program</p>

<img src="images/16_Jalankan_multithreads.png" width="700">

#### Pembahasan

<p align="justify">Keluarannya menarik, kelima 'Task starting' muncul dulu berurutan A-E, tapi urutan 'finished' acak (C, E, A, D, B), bukan berurutan seperti task yang dimulai. Keluaran program dapat berbeda karena thread berjalan secara konkuren dan urutan eksekusinya diatur oleh sistem operasi. Fungsi time.sleep(5) memberi jeda 5 detik pada setiap thread, sedangkan join() memastikan semua thread selesai sebelum program menampilkan pesan akhir.</p>

---

<p align="justify">- <strong>Data Race / Race Conditions</strong></p>

<p align="justify">Class: race-conditions-01.py</p>

<img src="images/17_race-conditions-01.png" width="700">

#### Pembahasan

<p align="justify">race-conditions-01.py mendemonstrasikan masalah data race. Ada saldo awal 100, lalu dua thread sama-sama mencoba menarik 80. Fungsi withdraw mengecek 'if balance >= amount', lalu ada jeda sleep(0,01) sebelum benar-benar mengurangi saldo. Jeda ini yang menjadi titik rawan. Selama thread pertama tidur, thread kedua bisa ikut masuk dan membaca saldo yang sama.</p>

---

<p align="justify">- Jalankan Program</p>

<img src="images/18_output_race-conditions-01.png" width="700">

#### Pembahasan

<p align="justify">Keluarannya membuktikan masalah race condition, saldo berakhir di -60, padahal seharusnya tidak mungkin negatif karena penarikan harus ditolak jika saldo tidak cukup. Yang terjadi adalah kedua thread sama-sama membaca saldo 100 sebelum ada yang mengurangi, sehingga keduanya lolos pengecekan dan sama-sama mengurangi 80. Hasilnya 100 - 80 - 80 = -60. Ini merupakan data race dimana dua thread menulis data bersamaan tanpa koordinasi.</p>

---

<p align="justify">- Visualisasi gambar dengan pensil/ballpoint, dan mengapa terjadi data race / race conditions</p>

<img src="images/32_Visualisasi.jpeg" width="700">

#### Pembahasan

<p align="justify">Visualisasi ini menguraikan penyebab race condition secara per timeline. Pada Thread 1, saldo dicek (100 >= 80, TRUE) lalu masuk sleep 0,01 detik. Saat Thread 1 masih tidur, Thread 2 juga membaca saldo yang masih 100 dan bernilai TRUE, karena Thread 1 belum sempat mengurangi. Setelah kedua thread bangun, keduanya mengurangi saldo, yang pertama 100 - 80 = 20, yang kedua 20 - 80 = -60. Hal ini terjadi karena pengecekan dan aksi pengurangan tidak dilakukan sebagai satu kesatuan yang terkunci (lock), sehingga dua thread mengakses dan memodifikasi variabel yang sama secara bersamaan tanpa sinkronisasi, sehingga hasilnya tidak sesuai dengan yang diharapkan.</p>

---

<p align="justify">- <strong>Supaya tidak terjadi race conditions</strong></p>

<p align="justify">Class: race-conditions-02.py</p>

<img src="images/19_race-conditions.png" width="700">

#### Pembahasan

<p align="justify">race-conditions-02.py adalah versi yang sudah diperbaiki. Caranya dengan menambahkan threading.Lock. Fungsi withdraw dibungkus dalam blok 'with counter_lock:', yang berarti hanya satu thread yang boleh masuk ke bagian pengecekan dan pengurangan saldo pada satu waktu. Thread lain harus menunggu sampai lock dilepas.</p>

---

<p align="justify">- Jalankan Program</p>

<img src="images/20_Output_race-conditions-02.png" width="700">

#### Pembahasan

<p align="justify">Hasilnya race condition hilang. Hanya satu thread yang berhasil menarik 80 dengan sisa saldo 20, sedangkan thread kedua ditolak karena saat gilirannya saldo tinggal 20 (kurang dari 80). Race condition tidak terjadi karena program menggunakan threading.Lock() untuk mengunci akses ke variabel balance. Dengan with counter_lock, hanya satu thread yang dapat menjalankan proses pengecekan saldo dan pengurangan saldo pada satu waktu. Thread lainnya harus menunggu sampai kunci dilepaskan. Dengan demikian, kedua thread tidak mengubah saldo secara bersamaan dan saldo tetap konsisten.</p>

---

<p align="justify">- <strong>Deadlock</strong></p>

<p align="justify">Class: deadlock-01.py</p>

<img src="images/21_deadlock-01.png" width="700">

#### Pembahasan

<p align="justify">Program deadlock-01.py mendemonstrasikan deadlock. Dibuat dua lock: lock_a dan lock_b. Thread 1 mengunci A dulu, sleep 1 detik, lalu minta B. Sebaliknya, Thread 2 mengunci B dulu, sleep 1 detik, lalu minta A. Pola penguncian yang berlawanan ini memang disengaja untuk memancing deadlock.</p>

---

<p align="justify">- Jalankan program</p>

<img src="images/22_output_deadlock-01.png" width="700">

#### Pembahasan

<p align="justify">Keluaran menunjukkan gejala khas deadlock. Thread 1 berhasil mengunci A lalu menunggu B, sementara Thread 2 berhasil mengunci B lalu menunggu A. Setelah dua baris output itu, program total berhenti — tidak ada 'Locked both' yang muncul. Program harus dihentikan manual (exit code 1 setelah 75 detik) karena tidak akan pernah selesai sendiri.</p>

---

<p align="justify">- Visualisasi gambar dengan pensil/ballpoint, dan mengapa terjadi deadlock</p>

<img src="images/33_Visualisasi.jpeg" width="700">

#### Pembahasan

<p align="justify">Visualisasi ini memperlihatkan deadlock sebagai siklus menunggu. Awalnya kedua lock bebas. Thread 1 mengunci A, lalu saat menunggu B, Thread 2 mengunci B. Karena masing-masing sudah memegang lock yang dibutuhkan lawannya, terbentuk siklus Thread 1 menunggu B yang dipegang Thread 2, sementara Thread 2 menunggu A yang dipegang Thread 1, keduanya saling menunggu lock yang sedang dipegang thread lain. Kondisi ini disebut circular wait salah satu syarat deadlock. Tidak ada yang mau melepas dulu, akhirnya keduanya mandek atau berhenti menunggu selamanya.</p>

---

<p align="justify">- <strong>Supaya deadlock tersebut tidak terjadi</strong></p>

<p align="justify">Class: deadlock-02.py</p>

<img src="images/23_Deadlock_02.png" width="700">

#### Pembahasan

<p align="justify">deadlock-02.py memperbaiki deadlock dengan dua pendekatan. Pertama, lock diambil menggunakan acquire dengan timeout 5 detik, jadi thread tidak akan menunggu selamanya jika lock tidak tersedia. Kedua, yang lebih penting, lock dilepas (release) lebih dahulu sebelum mencoba mengunci lock berikutnya, sehingga tidak terjadi kuncian saling menggantung.</p>

---

<p align="justify">- Jalankan program</p>

<img src="images/24_output_Deadlock.png" width="700">

#### Pembahasan

<p align="justify">Hasilnya program selesai secara normal dan mencetak 'Execution Finished'. Thread 1 mengunci A lalu melepasnya, Thread 2 mengunci B lalu melepasnya, baru masing-masing lanjut ke lock berikutnya. Dengan tidak ada lock yang dipegang saat menunggu lock lain, circular wait tidak terjadi, dan deadlock tidak terjadi.</p>

---

## PRAKTIK 4 - Algoritma Raft

<p align="justify">Class: raft.py</p>

<img src="images/25.raft_py.png" width="700">
<img src="images/26_raft_py_Lanjutan.png" width="700">

#### Pembahasan

<p align="justify">raft.py mengimplementasikan simulasi algoritma Raft untuk mencapai konsensus dalam sistem terdistribusi. Setiap node punya tiga kemungkinan state, yaitu FOLLOWER, CANDIDATE, dan LEADER. Jika follower tidak mendapat heartbeat dalam batas waktu acak (election_timeout 1-2 detik), ia menaikkan term, menjadi candidate, lalu meminta suara. Jika mendapat suara mayoritas, ia menjadi leader. Leader kemudian mengirim heartbeat berkala untuk menjaga stabilitas dan mencatat log perintah. Simulasi menggunakan 3 node dengan 20 langkah.</p>

---

<p align="justify">- Jalankan program</p>

<img src="images/27_Output_raft_py.png" width="700">
<img src="images/28_Output_raft_py.png" width="700">

#### Pembahasan

<p align="justify">Di awal simulasi (step 1-2), semua node masih FOLLOWER dengan term 0 karena belum ada timeout. Di step 3 terjadi pemilihan, dimana menarik bahwa Node 1 dan Node 2 sama-sama terpilih leader di term yang sama (split-vote). Namun sistem langsung memperbaiki diri di step 4, saat Node 1 menerima heartbeat dari Node 2, ia mundur menjadi follower. Sejak itu Node 2 menetap sebagai leader tunggal, mengirim heartbeat, dan mencatat log perintah sampai simulasi selesai. Ini menunjukkan bagaimana Raft tetap mencapai konsensus meski sempat terjadi benturan.</p>

---

<p align="justify">- Visualisasi sederhana Algoritma Raft</p>

<img src="images/34_Visualisasi.jpeg" width="700">

#### Pembahasan

<p align="justify">Visualisasi membagi simulasi Raft menjadi empat fase. Pertama, kondisi awal di mana semua node berstatus follower dengan term 0 dan masing-masing menghitung timer acak. Kedua, benturan atau split-vote di step 3 di mana Node 1 dan Node 2 sama-sama menjadi leader di term 1. Ketiga, pemulihan menuju leader tunggal, yaitu Node 1 kembali jadi follower dan Node 2 sah menjadi koordinator. Keempat, fase operasi dan stabilitas di mana Node 2 aktif mengirim heartbeat dan mencatat log perintah hingga akhir simulasi.</p>

---

<p align="justify">- Membuat program tersebut menjadi modul Python dan simulasinya menggunakan modul Python tersebut</p>

<p align="justify">Dari praktik sebelumnya, ditambahkan file: main.py pada folder Algoritma Raft.</p>

<p align="justify">File: main.py</p>

<img src="images/29_contoh_simulai_raft_py.png" width="700">

#### Pembahasan

<p align="justify">Agar bisa dipakai ulang, saya mengubah program simulasi menjadi modul dengan membuat main.py yang meng-import RaftNode dan State dari raft.py. Di main.py, fungsi simulasi ditulis ulang dengan tampilan yang lebih rapi dan mencetak isi log lengkap setiap node. Jadi raft.py berisi logika class-nya, sedangkan main.py hanya menjalankan simulasi tanpa perlu menyalin ulang kode.</p>

---

<p align="justify">- Jalankan program</p>

<img src="images/30_Output_Simulasi.png" width="700">
<img src="images/31_Output_Simulasi.png" width="700">

#### Pembahasan

<p align="justify">Keluaran menunjukkan hasil yang serupa dengan simulasi asli, dengan sedikit perbedaan karena pemilihan leader menggunakan timeout acak. Kali ini Node 1 yang menjadi leader (berbeda dengan run sebelumnya yang menghasilkan Node 2). Perbedaan ini justru membuktikan bahwa algoritma berjalan sebagaimana mestinya, setiap run bisa menghasilkan leader berbeda tergantung siapa timeout-nya lebih dulu. Leader kemudian mengirim heartbeat dan mencatat log perintah (command-5, command-10, command-15) hingga step 20. Modul bekerja dengan benar.</p>

---

# 📝 Kesimpulan

<p align="justify">Dari praktikum ini dapat disimpulkan bahwa sinkronisasi adalah hal yang krusial dalam sistem terdistribusi. Sinkronisasi waktu menggunakan NTP memastikan jam komputer akurat dengan offset hanya beberapa milidetik. Vector Clock memberikan cara untuk memahami urutan event dan hubungan sebab-akibat tanpa bergantung pada clock fisik. Masalah data race dan deadlock dapat dihindari dengan menggunakan lock (mutual exclusion) dan menghindari circular wait. Algoritma Raft menyediakan mekanisme konsensus yang sederhana namun efektif untuk memilih leader dan menjaga konsistensi sistem.</p>

---

## 🗒️ Referensi

<p align="justify">1. NetTime — https://www.timesynctool.com/</p>

<p align="justify">2. Chrony — https://chrony-project.org/</p>

<p align="justify">3. Simulate Distributed Consensus with the Raft Protocol (C# Corner) — https://www.c-sharpcorner.com/article/simulate-distributed-consensus-with-the-raft-protocol-simplified-using-python/</p>

<p align="justify">4. Lamport, L. (1978). "Time, Clocks, and the Ordering of Events in a Distributed System." <em>Communications of the ACM</em>, 21(7), 558–565.</p>
