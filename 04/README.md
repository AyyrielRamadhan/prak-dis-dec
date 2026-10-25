# Praktikum Minggu 04 - Konsistensi dan Replikasi pada Sistem Terdistribusi

**Mata Kuliah:** Praktikum Sistem Terdistribusi dan Terdesentralisasi

**Topik:** Konsistensi dan Replikasi pada Sistem Terdistribusi

---

## 🎯 Tujuan Praktikum

1. Memahami konsep konsistensi dan replikasi data pada sistem terdistribusi.
2. Menjelaskan perbedaan replikasi sinkron dan asinkron serta model primary-replica dan master-master.
3. Mengonfigurasi streaming replication PostgreSQL 18 dengan satu primary dan satu replica menggunakan Docker Compose.
4. Menganalisis peran WAL, physical replication slot, dan `pg_basebackup -R` dalam proses sinkronisasi data.
5. Memverifikasi status replikasi melalui tabel diagnostik dan pengujian manipulasi data pada kedua node.
6. Menerapkan skenario High Availability dengan mempromosikan replica menjadi primary.
7. Mengonfigurasi cluster master-master Apache Ignite 3 dan membuktikan bahwa setiap node dapat membaca sekaligus menulis data.

---

## 📚 Dasar Teori

### Konsistensi dan Replikasi Data

<p align="justify">
Dalam sistem terdistribusi, menyimpan data di satu mesin berarti menaruh seluruh layanan pada satu titik gagal. Replikasi menjawab masalah itu dengan menjaga salinan data di beberapa node, sehingga layanan tetap bisa diakses ketika satu node bermasalah, pembacaan bisa dibagi ke beberapa node, dan data bisa diletakkan lebih dekat ke pengguna. Harga yang harus dibayar juga nyata: setiap salinan harus diperbarui, lalu muncul pertanyaan kapan sebuah salinan boleh dianggap sudah sama dengan yang lain. Pertanyaan terakhir itulah inti dari konsistensi.
</p>

<p align="justify">
Secara garis besar konsistensi berada pada sebuah spektrum. Konsistensi kuat menjamin setiap pembacaan melihat tulisan terakhir yang sudah selesai, sehingga sistem berperilaku seolah-olah hanya ada satu salinan data; jaminan ini mahal karena operasi tulis harus menunggu koordinasi antar node. Konsistensi eventual menerima bahwa salinan boleh tertinggal sesaat asalkan semuanya konvergen pada akhirnya; model ini murah dan cepat, tetapi pembaca bisa melihat data lama. Di antara keduanya ada model seperti konsistensi kausal dan read-your-writes yang mencoba mengambil sebagian jaminan yang paling dibutuhkan aplikasi. Teorema CAP merangkum dilemanya: ketika terjadi pemisahan jaringan, sistem harus memilih antara tetap konsisten atau tetap tersedia. Dalam praktik, pilihan itu tidak dibuat sekali untuk seluruh sistem, melainkan per operasi dan per kebutuhan.
</p>

### Replikasi Primary-Replica dan Streaming Replication

<p align="justify">
Model yang paling umum dipakai basis data relasional adalah primary-replica. Satu node ditunjuk sebagai primary dan menjadi satu-satunya tempat operasi tulis diterima, sementara satu atau lebih replica menerima perubahan darinya dan biasanya melayani pembacaan. Kesederhanaan model ini adalah keunggulannya: tidak ada konflik tulis karena hanya ada satu penulis, dan replica bisa ditambah kapan saja untuk menambah kapasitas baca. Replica juga menjadi calon pengganti kalau primary gagal.
</p>

<p align="justify">
Cara perubahan dikirim membedakan replikasi sinkron dan asinkron. Pada replikasi sinkron, primary menunggu konfirmasi dari replica sebelum menyatakan transaksi commit, sehingga kehilangan data saat failover bisa ditekan sampai nol; konsekuensinya latensi tulis naik dan ketersediaan primary ikut bergantung pada replica. Pada replikasi asinkron, primary langsung commit dan mengirim perubahan di belakang, sehingga tulis tetap cepat tetapi ada jendela kecil di mana transaksi terakhir belum sampai ke replica. Istilah streaming replication merujuk pada cara pengirimannya: perubahan dialirkan terus-menerus begitu terjadi, bukan dikirim sebagai snapshot berkala. PostgreSQL mengimplementasikannya dengan mengalirkan WAL dari proses pengirim di primary ke proses penerima di replica.
</p>

### WAL, LSN, dan Replication Slot

<p align="justify">
Write-Ahead Log atau WAL adalah catatan berurutan berisi setiap perubahan yang akan diterapkan pada data. Prinsipnya write-ahead: perubahan ditulis ke WAL lebih dulu, baru kemudian halaman data yang sebenarnya diperbarui. Aturan ini awalnya dibuat untuk pemulihan setelah crash, karena dengan memutar ulang WAL, basis data bisa kembali ke kondisi konsisten. Ternyata mekanisme yang sama bisa dipakai untuk replikasi: kalau replica menerima aliran WAL yang sama dan memutarnya ulang, hasil akhirnya identik dengan primary.
</p>

<p align="justify">
Setiap posisi di WAL diberi penanda Log Sequence Number atau LSN. Primary mencatat sejauh mana ia sudah mengirim, dan replica melaporkan sejauh mana ia sudah menulis, men-flush, dan memutar ulang; selisih antarposisi itulah lag replikasi. Agar primary tidak membuang WAL yang belum sempat dibaca replica, dibuat replication slot sebagai penanda sisi server. Slot menjamin WAL ditahan sampai replica mengonfirmasi, tetapi juga punya risiko: slot yang aktif tetapi replica-nya mati lama bisa membuat WAL menumpuk dan menghabiskan disk. Parameter <code>hot_standby_feedback</code> melengkapi mekanisme ini dengan memberi tahu primary tentang query yang sedang berjalan di replica, sehingga baris yang masih dibutuhkan tidak dibersihkan terlalu cepat.
</p>

### High Availability, Failover, dan Split-Brain

<p align="justify">
High Availability berbicara tentang seberapa cepat layanan bisa pulih setelah komponen gagal, biasanya diukur dengan RTO untuk lama downtime dan RPO untuk banyak data yang boleh hilang. Replikasi menyediakan datanya, tetapi belum otomatis menyediakan pemulihannya. Failover adalah proses memindahkan peran primary ke replica, dan proses ini bisa manual seperti menjalankan <code>pg_promote()</code>, atau otomatis dengan bantuan alat seperti Patroni atau repmgr yang memantau kesehatan node dan mengambil keputusan berdasarkan quorum.
</p>

<p align="justify">
Risiko terbesar dalam failover adalah split-brain, yaitu kondisi ketika dua node sama-sama menganggap dirinya primary dan menerima tulisan. Kalau dibiarkan, data di keduanya bercabang dan tidak ada cara sederhana untuk menggabungkannya kembali. Karena itu sistem yang serius memakai fencing untuk memastikan node lama benar-benar tidak bisa menulis, misalnya dengan mematikan mesinnya atau mencabut aksesnya ke storage. Pada praktikum ini, pencegahan itu dilakukan secara manual: primary lama dihentikan dan tidak dihidupkan kembali sebagai primary. Kesadaran akan batas inilah yang membedakan replikasi sederhana dari sistem High Availability yang benar-benar siap produksi.
</p>

### Apache Ignite dan Replikasi Master-Master

<p align="justify">
Apache Ignite 3 adalah basis data terdistribusi yang menyimpan data di memori sekaligus di disk. Data dipecah menjadi partisi berdasarkan affinity key, lalu setiap partisi ditempatkan pada node tertentu sesuai zona yang dipakai. Zona juga menentukan replication factor, yaitu berapa salinan yang disimpan; dengan replication factor lebih dari satu, satu partisi tetap bisa dibaca meskipun node pemiliknya mati. Dari sudut pandang aplikasi, semua node terlihat setara karena setiap node bisa menerima permintaan baca maupun tulis, dan node yang tidak memiliki partisi yang dituju akan meneruskannya ke node yang tepat.
</p>

<p align="justify">
Karena tidak ada satu primary tunggal, koordinasi dipindahkan ke lapisan lain. Metadata cluster, termasuk daftar node dan definisi zona, dikelola oleh cluster management group dengan mekanisme consensus, sehingga perubahan konfigurasi harus disetujui mayoritas node. Inilah sebabnya inisialisasi cluster menyebut <code>metastorage-group</code> dan memakai jumlah node ganjil. Model master-master memberi ketersediaan tulis yang lebih baik daripada primary-replica, tetapi menuntut penanganan konflik dan konsistensi yang lebih rumit. Pada dataset Chinook, kompleksitas itu dikelola dengan membagi zona: tabel besar didistribusikan, sedangkan tabel referensi kecil seperti MEDIATYPE dan GENRE digandakan penuh ke semua node agar pembacaannya murah.
</p>

### Docker sebagai Lingkungan Praktikum

<p align="justify">
Docker memaket aplikasi beserta dependensinya ke dalam image, lalu menjalankannya sebagai container yang terisolasi. Container punya filesystem, network, dan prosesnya sendiri, tetapi berbagi kernel dengan host, sehingga jauh lebih ringan daripada mesin virtual. Image bersifat immutable: sekali dibuat, isinya tidak berubah, dan setiap container baru selalu dimulai dari kondisi yang sama. Sifat ini yang membuat hasil praktikum bisa diulang dengan perilaku yang konsisten, sesuatu yang sulit dijamin kalau PostgreSQL dan Ignite dipasang langsung di sistem operasi.
</p>

<p align="justify">
Docker Compose menambahkan kemampuan mendefinisikan beberapa container sekaligus dalam satu berkas YAML. Service di dalamnya otomatis mendapat jaringan bersama dan bisa saling memanggil dengan nama service sebagai hostname, misalnya replica menghubungi <code>postgres_primary</code> tanpa tahu IP-nya. Port yang dipublikasikan menghubungkan container ke host, sedangkan volume menjaga data tetap ada di luar siklus hidup container. Ada juga healthcheck yang membuat status container bermakna, dan <code>depends_on</code> yang mengatur urutan start. Perlu dipahami bahwa <code>depends_on</code> hanya menunggu container lain dimulai, bukan menunggu layanannya siap, sehingga aplikasi yang bergantung pada kesiapan layanan tetap perlu mekanisme tunggu sendiri seperti loop <code>until</code> pada praktikum ini.
</p>

---

## 🧪 Pembahasan Praktikum

### 4.1 Streaming Replication Menggunakan PostgreSQL 18

#### Prasyarat dan Instalasi Docker

1. Install Docker

<p align="center"><img src="images/01_Install_Docker.png" alt="Konfigurasi instalasi Docker Desktop dengan pilihan Per-user installation" width="700"></p>

<p align="center"><i>Gambar 4.1 — Layar konfigurasi instalasi Docker Desktop.</i></p>

#### Pembahasan

<p align="justify">
Tahap pertama praktikum ini adalah menyiapkan Docker Desktop di Windows. Di layar konfigurasi ada dua pilihan instalasi, dan yang dipilih adalah <i>Per-user installation</i> karena tidak menuntut hak administrator serta otomatis memakai backend WSL 2. Pilihan ini penting: container PostgreSQL yang nanti dijalankan adalah container Linux, jadi tanpa WSL 2 sebagai lapisan virtualisasinya container tidak akan bisa hidup. Opsi <i>Add shortcut to desktop</i> dibiarkan tercentang supaya aplikasinya mudah dibuka lagi, lalu instalasi dijalankan dengan menekan OK.
</p>

<p align="center"><img src="images/02_Install_Docker.png" alt="Proses ekstraksi berkas Docker Desktop" width="700"></p>

<p align="center"><i>Gambar 4.2 — Proses ekstraksi berkas saat instalasi Docker Desktop.</i></p>

#### Pembahasan

<p align="justify">
Setelah konfigurasi disetujui, installer mulai mengekstrak berkas-berkas Docker Desktop. Proses ini terlihat sederhana, hanya tulisan <i>Unpacking files...</i> dengan progress bar di bawah, tetapi justru di sini sebagian besar waktu instalasi dihabiskan karena yang disalin bukan hanya aplikasi GUI-nya, melainkan juga CLI, engine, dan komponen integrasi WSL. Karena itu jendela installer sebaiknya tidak ditutup sebelum progress bar penuh; kalau terhenti di tengah jalan, komponen yang belum selesai bisa tertinggal dan Docker sering gagal start.
</p>

<p align="center"><img src="images/03_Install_Docker.png" alt="Pesan Installation succeeded pada Docker Desktop" width="700"></p>

<p align="center"><i>Gambar 4.3 — Instalasi Docker Desktop dinyatakan berhasil.</i></p>

#### Pembahasan

<p align="justify">
Instalasi berakhir dengan pesan <i>Installation succeeded</i> dan tombol Close. Di titik ini penting untuk tidak langsung menyimpulkan bahwa Docker sudah siap dipakai, karena yang selesai baru proses pemasangan berkas. Engine Docker baru benar-benar berjalan setelah aplikasi Docker Desktop dibuka dan statusnya menunjukkan <i>Engine running</i>. Pengalaman yang cukup umum adalah terminal mengembalikan pesan error koneksi ke pipe Docker ketika perintah <code>docker</code> dijalankan terlalu cepat, dan solusinya memang hanya menunggu engine selesai boot, bukan menginstal ulang.
</p>

#### Pemeriksaan Versi dan Lingkungan

2. Cek versi Docker & Compose

**_Versi Docker_**

<p align="center"><img src="images/04_Cek_Versi_Docker.png" alt="Hasil perintah docker --version" width="700"></p>

<p align="center"><i>Gambar 4.4 — Versi Docker CLI yang terpasang.</i></p>

#### Pembahasan

<p align="justify">
Pemeriksaan pertama dilakukan dengan <code>docker --version</code>, dan hasilnya Docker version 29.9.2 build a82e528. Angka ini menunjukkan versi CLI yang terpasang, sekaligus memastikan perintah <code>docker</code> sudah dikenali oleh shell. Perlu dicatat bahwa versi CLI dan versi engine bisa berbeda, jadi angka ini belum cukup untuk membuktikan daemon benar-benar hidup; itu sebabnya masih perlu pemeriksaan berikutnya.
</p>

**_Versi Compose_**

<p align="center"><img src="images/05_Cek_Versi_Docker_Compose.png" alt="Hasil perintah docker compose version" width="700"></p>

<p align="center"><i>Gambar 4.5 — Versi Docker Compose yang terpasang.</i></p>

#### Pembahasan

<p align="justify">
Selanjutnya <code>docker compose version</code> menghasilkan Docker Compose version v5.6.1. Ini memastikan Compose tersedia sebagai plugin yang menempel pada CLI Docker, sehingga perintahnya ditulis <code>docker compose</code> dengan spasi, bukan <code>docker-compose</code> dengan tanda hubung seperti pada versi lama. Perbedaan ini bukan sekadar gaya penulisan: file <code>env.sh</code> yang disiapkan nanti memakai bentuk <code>docker compose</code>, jadi kalau yang terpasang hanya Compose versi lama, alias di dalamnya tidak akan jalan.
</p>

**_Cek info Docker_**

Gunakan perintah:

```bash
docker info
```

Contoh penggunaan:

```text
Ayyrieldev@cuyunivers>docker info
Client:
 Version:    29.9.2
 Context:    desktop-linux
 Debug Mode: false
 Plugins:
  agent: Docker AI Agent Runner (Docker Inc.)
    Version:  v1.152.0
    Path:     C:\Users\LENOVO\.docker\cli-plugins\docker-agent.exe
  ai: Docker AI Agent - Ask Gordon (Docker Inc.)
    Version:  v1.33.0
    Path:     C:\Users\LENOVO\.docker\cli-plugins\docker-ai.exe
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.38.1
    Path:     C:\Users\LENOVO\.docker\cli-plugins\docker-buildx.exe
  compose: Docker Compose (Docker Inc.)
    Version:  v5.6.1
    Path:     C:\Users\LENOVO\.docker\cli-plugins\docker-compose.exe
  debug: Get a shell into any image or container (Docker Inc.)
    Version:  0.0.47
    Path:     C:\Users\LENOVO\.docker\cli-plugins\docker-debug.exe
  desktop: Docker Desktop commands (Docker Inc.)
    Version:  4.96.2
    Path:     C:\Users\LENOVO\.docker\cli-plugins\docker-desktop.exe
  dhi: CLI for managing Docker Hardened Images (Docker Inc.)
    Version:  v0.0.9
    Path:     C:\Users\LENOVO\.docker\cli-plugins\docker-dhi.exe
  extension: Manages Docker extensions (Docker Inc.)
    Version:  v0.2.32
    Path:     C:\Users\LENOVO\.docker\cli-plugins\docker-extension.exe
  init: Creates Docker-related starter files (Docker Inc.)
    Version:  v1.4.0
    Path:     C:\Users\LENOVO\.docker\cli-plugins\docker-init.exe
  mcp: Docker MCP Plugin (Docker Inc.)
    Version:  v0.44.1
    Path:     C:\Users\LENOVO\.docker\cli-plugins\docker-mcp.exe
  model: Docker Model Runner (Docker Inc.)
    Version:  v1.2.6
    Path:     C:\Users\LENOVO\.docker\cli-plugins\docker-model.exe
  offload: Docker Offload (Docker Inc.)
    Version:  v0.7.16
    Path:     C:\Users\LENOVO\.docker\cli-plugins\docker-offload.exe
  pass: Docker Pass Secrets Manager Plugin (beta) (Docker Inc.)
    Version:  v0.3.2
    Path:     C:\Users\LENOVO\.docker\cli-plugins\docker-pass.exe
  sandbox: "docker sandbox" is deprecated, use Docker Sandboxes instead. (Docker Inc.)
    Version:  v0.13.0
    Path:     C:\Users\LENOVO\.docker\cli-plugins\docker-sandbox.exe
  scout: Docker Scout (Docker Inc.)
    Version:  v1.27.0
    Path:     C:\Users\LENOVO\.docker\cli-plugins\docker-scout.exe

Server:
 Containers: 0
  Running: 0
  Paused: 0
  Stopped: 0
 Images: 0
 Server Version: 29.9.2
 Storage Driver: overlayfs
  driver-type: io.containerd.snapshotter.v1
 Logging Driver: local
 Cgroup Driver: cgroupfs
 Cgroup Version: 2
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
  Log: awslogs fluentd gcplogs gelf journald json-file local splunk syslog
  CDI spec directories:
   /etc/cdi
   /var/run/cdi
  Discovered Devices:
   cdi: docker.com/gpu=webgpu
 Swarm: inactive
 Runtimes: io.containerd.runc.v2 nvidia runc
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: b7a25261e029d68978bbf290df0a62fc819b3c51
 runc version: v1.5.2-0-g29dd3dc2
 init version: de40ad0
 Security Options:
  seccomp
   Profile: builtin
  cgroupns
 Kernel Version: 6.18.33.2-microsoft-standard-WSL2
 Operating System: Docker Desktop
 OSType: linux
 Architecture: x86_64
 CPUs: 12
 Total Memory: 7.606GiB
 Name: docker-desktop
 ID: e91a3552-1c19-41d2-8504-94998f188362
 Docker Root Dir: /var/lib/docker
 Debug Mode: false
 HTTP Proxy: http.docker.internal:3128
 HTTPS Proxy: http.docker.internal:3128
 No Proxy: hubproxy.docker.internal
 Labels:
  com.docker.desktop.address=npipe://\\.\pipe\docker_cli
 Experimental: false
 Insecure Registries:
  hubproxy.docker.internal:5555
  127.0.0.0/8
  ::1/128
 Live Restore Enabled: false
 Firewall Backend: iptables
```

#### Pembahasan

<p align="justify">
Perintah <code>docker info</code> dipakai untuk melihat kondisi engine secara menyeluruh, bukan hanya versinya. Output-nya terbagi dua: bagian Client yang menjelaskan CLI dan plugin yang terpasang, lalu bagian Server yang menjelaskan engine yang benar-benar berjalan. Dari bagian Server terlihat 0 container, storage driver overlayfs, cgroup v2, kernel WSL2 6.18.33.2, 12 CPU, dan memori sekitar 7,6 GiB. Angka-angka ini berguna sebagai batas realistis: dua container PostgreSQL dengan alokasi kecil masih nyaman, tetapi kalau nanti menjalankan tiga node Ignite yang masing-masing meminta 4 GB, memori sebesar itu justru menjadi kendala. Kalau bagian Server kosong atau error, berarti engine belum hidup dan seluruh langkah berikutnya pasti gagal.
</p>

#### Struktur Direktori dan File

File yang diperlukan adalah sebagai berikut:

```text
streaming-replication/
├── 00_init.sql
├── docker-compose.yaml
└── env.sh
1 directory, 3 files
```

<p align="center"><img src="images/06_File_Direktori.png" alt="Struktur direktori streaming-replication" width="700"></p>

<p align="center"><i>Gambar 4.6 — Struktur direktori dan berkas praktikum streaming replication.</i></p>

#### Pembahasan

<p align="justify">
Ada tiga berkas yang harus disiapkan di dalam folder <code>streaming-replication</code>. <code>00_init.sql</code> berisi perintah yang dijalankan sekali saat primary pertama kali dibuat, <code>docker-compose.yaml</code> mendefinisikan dua service PostgreSQL beserta konfigurasinya, dan <code>env.sh</code> menyimpan alias agar perintah panjang tidak perlu diketik ulang. Ketiganya dipisah karena perannya berbeda dan siklus hidupnya juga berbeda: SQL hanya dieksekusi saat inisialisasi, YAML dibaca setiap kali compose dijalankan, sedangkan <code>env.sh</code> hanya berlaku di sesi shell yang memuatnya. Nama folder juga bukan hal sepele, karena Compose memakai nama folder sebagai nama project, sehingga container yang muncul nanti bernama <code>streaming-replication-postgres_primary-1</code> dan <code>streaming-replication-postgres_replica-1</code>.
</p>

_File: 00_init.sql_

<p align="center"><img src="images/07_File_00_init_sql.png" alt="Isi berkas 00_init.sql" width="700"></p>

<p align="center"><i>Gambar 4.7 — Isi berkas 00_init.sql.</i></p>

#### Pembahasan

<p align="justify">
File <code>00_init.sql</code> isinya cuma dua baris, tapi perannya justru yang bikin replikasi ini bisa jalan. Baris pertama membuat user <code>replicator</code> dengan hak <code>REPLICATION</code>, jadi user ini memang disiapkan khusus untuk mengambil stream WAL dari primary, bukan untuk dipakai aplikasi sehari-hari. Baris kedua membuat physical replication slot bernama <code>replication_slot</code>, semacam "titipan posisi" WAL di sisi primary; dengan slot ini primary tidak akan membuang WAL yang belum sempat dibaca replica, sehingga kalau replica sempat mati ia bisa menyusul lagi tanpa <code>pg_basebackup</code> dari nol. Karena file ini diletakkan di <code>/docker-entrypoint-initdb.d</code>, PostgreSQL menjalankannya otomatis sekali saat volume data pertama kali dibuat — jadi kalau isinya diubah belakangan, perubahannya tidak akan berefek kecuali data lama dihapus dulu.
</p>

_File: docker-compose.yaml_

<p align="center"><img src="images/08_FIle_Docker-Compose_yaml.png" alt="Isi berkas docker-compose.yaml" width="700"></p>

<p align="center"><i>Gambar 4.8 — Isi berkas docker-compose.yaml.</i></p>

#### Pembahasan

<p align="justify">
File <code>docker-compose.yaml</code> adalah inti dari praktikum ini, dan penyusunannya sengaja memakai anchor <code>x-postgres-common</code> agar konfigurasi yang sama tidak ditulis dua kali. Bagian yang dipakai bersama adalah image <code>postgres:18.3-alpine3.23</code>, user <code>postgres</code>, <code>restart: always</code>, dan healthcheck <code>pg_isready</code>; healthcheck inilah yang nanti membuat status container tertulis <i>healthy</i>, bukan sekadar <i>Up</i>. Service primary memakai port 5432, mendefinisikan user <code>zuser</code>, database <code>zdb</code>, dan mengizinkan koneksi replikasi dari user <code>replicator</code> lewat <code>POSTGRES_HOST_AUTH_METHOD</code>. Parameter yang diberikan lewat <code>command</code> semuanya punya alasan: <code>wal_level=replica</code> wajib agar WAL memuat informasi yang dibutuhkan standby, <code>hot_standby=on</code> membuat replica bisa di-query, <code>max_wal_senders</code> dan <code>max_replication_slots</code> menyediakan cukup koneksi dan slot, sedangkan <code>hot_standby_feedback=on</code> mencegah query panjang di replica membuat baris yang dibutuhkannya terhapus di primary. Service replica memakai image yang sama tetapi peran yang berbeda: ia tidak menjalankan initdb, melainkan menunggu sampai <code>pg_basebackup</code> berhasil menyalin seluruh data primary dengan flag <code>-R</code> dan <code>-X stream</code>, baru kemudian menjalankan <code>postgres</code>. Flag <code>-R</code> itu yang menuliskan <code>standby.signal</code> dan <code>primary_conninfo</code> secara otomatis, sehingga replica tidak perlu dikonfigurasi manual. <code>depends_on</code> hanya menjamin urutan start, bukan kesiapan primary, dan itulah sebabnya perintah backup dibungkus loop <code>until</code>.
</p>

_File: env.sh_

<p align="center"><img src="images/09_File_env_sh.png" alt="Isi berkas env.sh" width="700"></p>

<p align="center"><i>Gambar 4.9 — Kumpulan alias pada berkas env.sh.</i></p>

#### Pembahasan

<p align="justify">
File <code>env.sh</code> berisi tujuh alias yang tugasnya mempersingkat perintah. <code>dcu</code> dan <code>dcd</code> mewakili <code>docker compose up -d</code> dan <code>down</code>, <code>dps</code> mewakili <code>docker ps</code>, sementara <code>der</code>, <code>dep</code>, <code>dlr</code>, dan <code>dlp</code> membungkus <code>docker exec</code> serta <code>docker logs</code> untuk container replica dan primary. Nama container ditulis lengkap dan mengikuti nama folder, jadi kalau foldernya diganti nama, isi alias ini juga harus disesuaikan; kalau tidak, perintah akan gagal karena container yang dituju tidak ditemukan. Berbeda dengan contoh di modul yang memakai <code>sudo</code>, versi yang dipakai di sini tidak memerlukannya karena Docker Desktop di Windows sudah berjalan dengan hak akses yang memadai.
</p>

#### Menjalankan Docker Compose

1. Masuk ke direktori streaming-replication terlebih dahulu karena saat ini posisi folder masih berada di folder 04.

```bash
cd 04\streaming-replication
```

Kemudian periksa direktori di streaming-replication:

<p align="center"><img src="images/10_Cek_Direktori.png" alt="Hasil pemeriksaan isi direktori dengan ls -la" width="700"></p>

<p align="center"><i>Gambar 4.10 — Pemeriksaan isi direktori streaming-replication.</i></p>

#### Pembahasan

<p align="justify">
Perintah <code>ls -la</code> dipakai untuk memeriksa isi direktori. Ketiga berkas terlihat lengkap: <code>00_init.sql</code> berukuran 146 byte, <code>docker-compose.yaml</code> 1424 byte, dan <code>env.sh</code> 328 byte. Pemeriksaan kecil ini sebenarnya penting karena banyak kegagalan compose berasal dari hal sepele seperti berkas yang tersimpan dengan ekstensi berbeda, berada di folder yang salah, atau <code>00_init.sql</code> yang kosong sehingga user replikasi tidak pernah dibuat. Melihat ukuran yang wajar sudah cukup untuk memastikan berkasnya benar-benar berisi, bukan file kosong.
</p>

2. Muat alias di file env.sh terlebih dahulu.

```bash
source env.sh
```

<p align="center"><img src="images/12_Muat_env_sh.png" alt="Memuat alias dengan source env.sh" width="700"></p>

<p align="center"><i>Gambar 4.11 — Memuat alias dari berkas env.sh.</i></p>

#### Pembahasan

<p align="justify">
Perintah <code>source env.sh</code> dijalankan agar alias di dalam file itu dimuat ke shell yang sedang aktif. Kalau file dijalankan dengan <code>./env.sh</code>, alias akan hilang begitu proses selesai karena pengaruhnya hanya berlaku di subshell; dengan <code>source</code>, isi file dibaca seolah-olah diketik langsung di terminal saat itu. Konsekuensinya, alias hanya hidup selama sesi terminal tersebut terbuka, sehingga kalau jendela ditutup atau terminal baru dibuka, <code>source env.sh</code> harus diulang dari dalam folder yang benar. Ini juga menjelaskan kenapa posisi direktori penting: <code>source</code> mencari file relatif terhadap folder tempat perintah dijalankan.
</p>

3. Jalankan Docker Compose.

```bash
docker compose up -d
```

<p align="center"><img src="images/11_Menjalankan_Docker.png" alt="Output docker compose up -d" width="700"></p>

<p align="center"><i>Gambar 4.12 — Menjalankan kedua container dengan docker compose up -d.</i></p>

atau menggunakan alias:

```bash
dcu
```

<p align="center"><img src="images/14_dcu.png" alt="Output alias dcu saat container sudah berjalan" width="700"></p>

<p align="center"><i>Gambar 4.13 — Menjalankan ulang lewat alias dcu.</i></p>

#### Pembahasan

<p align="justify">
Opsi <code>-d</code> membuat container berjalan di latar belakang sehingga terminal tidak terkunci oleh log. Output-nya memperlihatkan urutan kerja Compose: image <code>postgres:18.3-alpine3.23</code> diambil dari Docker Hub selama sekitar 33 detik, network <code>streaming-replication_default</code> dibuat, lalu kedua container dijalankan. Menariknya, percobaan berikutnya dengan alias <code>dcu</code> hanya menampilkan <i>Running</i> untuk kedua container, bukan <i>Created</i> lagi. Ini menunjukkan sifat idempoten Compose: kalau konfigurasi tidak berubah, container yang sudah ada tidak dibuat ulang, sehingga aman menjalankan perintah yang sama berkali-kali.
</p>

4. Periksa apakah kedua image PostgreSQL 18 di Alpine Linux tersebut telah berhasil diaktifkan.

```bash
dps
```

<p align="center"><img src="images/13_Cek_Status.png" alt="Status kedua container PostgreSQL healthy" width="700"></p>

<p align="center"><i>Gambar 4.14 — Status kedua container PostgreSQL setelah berjalan.</i></p>

Jika status healthy belum muncul, log container bisa ditelusuri:

```bash
dlr
```

<p align="center"><img src="images/15_dlr.png" alt="Log container replica" width="700"></p>

<p align="center"><i>Gambar 4.15 — Log container replica saat proses backup dan streaming.</i></p>

Atau bisa juga menggunakan:

```bash
docker logs streaming-replication-postgres_replica-1
```

Contoh penggunaan:

```text
$ docker logs streaming-replication-postgres_replica-1
pg_basebackup: error: connection to server at "postgres_primary" (172.18.0.2), port 5432 failed: Connection refused
        Is the server running on that host and accepting TCP/IP connections?
pg_basebackup failed. Retrying in 5 seconds ...
Backup done, starting replica...
2026-10-24 02:40:41.600 UTC [1] LOG:  starting PostgreSQL 18.3 on x86_64-pc-linux-musl, compiled by gcc (Alpine 15.2.0) 15.2.0, 64-bit
2026-10-24 02:40:41.601 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
2026-10-24 02:40:41.601 UTC [1] LOG:  listening on IPv6 address "::", port 5432
2026-10-24 02:40:41.611 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
2026-10-24 02:40:41.624 UTC [17] LOG:  database system was interrupted; last known up at 2026-10-24 02:40:40 UTC
2026-10-24 02:40:42.570 UTC [17] LOG:  starting backup recovery with redo LSN 0/2000028, checkpoint LSN 0/2000080, on timeline ID 1
2026-10-24 02:40:42.570 UTC [17] LOG:  entering standby mode
2026-10-24 02:40:42.581 UTC [17] LOG:  redo starts at 0/2000028
2026-10-24 02:40:42.585 UTC [17] LOG:  completed backup recovery with redo LSN 0/2000028 and end LSN 0/2000120
2026-10-24 02:40:42.586 UTC [17] LOG:  consistent recovery state reached at 0/2000120
2026-10-24 02:40:42.586 UTC [1] LOG:  database system is ready to accept read-only connections
2026-10-24 02:40:42.619 UTC [18] LOG:  started streaming WAL from primary at 0/3000000 on timeline 1
2026-10-24 02:45:56.725 UTC [15] LOG:  restartpoint starting: time
2026-10-24 02:46:01.014 UTC [15] LOG:  restartpoint complete: wrote 42 buffers (0.3%), wrote 2 SLRU buffers; 0 WAL file(s) added, 0 removed, 1 recycled; write=4.243 s, sync=0.022 s, total=4.290 s; sync files=10, longest=0.010 s, average=0.003 s; distance=16701 kB, estimate=16701 kB; lsn=0/304F5C0, redo lsn=0/304F530
2026-10-24 02:46:01.014 UTC [15] LOG:  recovery restart point at 0/304F530
2026-10-24 02:46:01.014 UTC [15] DETAIL:  Last completed transaction was at log time 2026-10-24 02:41:37.715678+00.
2026-10-24 03:11:48.981 UTC [18] LOG:  replication terminated by primary server
2026-10-24 03:11:48.981 UTC [18] DETAIL:  End of WAL reached on timeline 1 at 0/304F6E8.
2026-10-24 03:11:48.981 UTC [18] FATAL:  could not send end-of-streaming message to primary: server closed the connection unexpectedly
                This probably means the server terminated abnormally
                before or while processing the request.
        invalid socket
        no COPY in progress
2026-10-24 03:11:48.982 UTC [17] LOG:  invalid record length at 0/304F6E8: expected at least 24, got 0
2026-10-24 03:11:48.995 UTC [1321] FATAL:  streaming replication receiver "walreceiver" could not connect to the primary server: connection to server at "postgres_primary" (172.18.0.2), port 5432 failed: FATAL:  the database system is shutting down
2026-10-24 03:11:48.995 UTC [17] LOG:  waiting for WAL to become available at 0/304F700
2026-10-24 03:11:54.010 UTC [1322] LOG:  started streaming WAL from primary at 0/3000000 on timeline 1
2026-10-24 03:11:57.252 UTC [15] LOG:  restartpoint starting: time
2026-10-24 03:11:57.283 UTC [15] LOG:  restartpoint complete: wrote 0 buffers (0.0%), wrote 0 SLRU buffers; 0 WAL file(s) added, 0 removed, 0 recycled; write=0.003 s, sync=0.001 s, total=0.031 s, sync files=0, longest=0.000 s, average=0.000 s; distance=0 kB, estimate=15031 kB; lsn=0/304F670, redo lsn=0/304F670
2026-10-24 03:11:57.283 UTC [15] LOG:  recovery restart point at 0/304F670
2026-10-24 03:11:57.283 UTC [15] DETAIL:  Last completed transaction was at log time 2026-10-24 02:41:37.715678+00.
```

#### Pembahasan

<p align="justify">
Status yang ditampilkan adalah <code>Up 17 minutes (healthy)</code> untuk kedua container, port 5432 dan 5433 sudah dipublikasikan ke host, dan nama container sesuai nama folder. Status <i>healthy</i> itu berasal dari healthcheck <code>pg_isready</code>, jadi artinya PostgreSQL benar-benar menerima koneksi, bukan hanya proses container-nya hidup. Ketika status itu belum muncul, log replica dibaca dengan <code>dlr</code>, dan di sanalah proses sebenarnya terlihat. Baris pertama justru sebuah error: <code>pg_basebackup: error: connection to server at "postgres_primary" (172.18.0.2), port 5432 failed: Connection refused</code>. Ini bukan kegagalan permanen, melainkan akibat replica dijalankan lebih dulu daripada primary siap menerima koneksi; <code>depends_on</code> hanya menunggu container primary dibuat, bukan menunggu PostgreSQL selesai inisialisasi. Karena perintah backup dibungkus <code>until</code>, replica mencetak <code>pg_basebackup failed. Retrying in 5 seconds ...</code> lalu mencoba lagi sampai berhasil, dan itu terbukti dari baris <code>Backup done, starting replica...</code>. Setelah itu log memperlihatkan PostgreSQL 18.3 di replica menyala, masuk <code>entering standby mode</code>, mencapai <code>consistent recovery state</code>, dan membuka <code>read-only connections</code>; baris <code>started streaming WAL from primary at 0/3000000 on timeline 1</code> adalah tanda paling jelas bahwa replikasi sudah berjalan. Di bagian akhir log muncul <code>replication terminated by primary server</code> yang diikuti pesan <code>the database system is shutting down</code>, dan itu wajar karena primary memang dimatikan pada tahap High-Availability; replica lalu menulis <code>waiting for WAL to become available</code> dan mencoba menyambung kembali. Jadi satu log ini sebenarnya menceritakan seluruh siklus: gagal karena belum siap, menyusul, streaming normal, lalu terputus saat primary dimatikan.
</p>

#### Pengujian Replikasi

Untuk melihat apakah replikasi ini telah berfungsi, kita bisa melihatnya dari tabel diagnostik PostgreSQL 18.3 maupun dengan melakukan percobaan manipulasi data tabel.

```bash
dep
```

<p align="center"><img src="images/16_dep.png" alt="Hasil query pg_stat_replication di primary" width="700"></p>

<p align="center"><i>Gambar 4.16 — Status replikasi pada tabel pg_stat_replication.</i></p>

<p align="center"><img src="images/17_dep.png" alt="Hasil query pg_replication_slots di primary" width="700"></p>

<p align="center"><i>Gambar 4.17 — Kondisi physical replication slot pada primary.</i></p>

#### Pembahasan

<p align="justify">
Perintah <code>dep</code> membuka shell container primary, lalu psql dijalankan dengan <code>psql -U zuser -d zdb</code>, dan <code>\x</code> diaktifkan agar hasil query panjang tampil vertikal. <code>SELECT * FROM pg_stat_replication</code> memperlihatkan satu baris dengan <code>state = streaming</code>, <code>application_name = walreceiver</code>, dan alamat <code>172.18.0.3</code> yang tidak lain adalah replica. Kolom <code>sent_lsn</code>, <code>write_lsn</code>, <code>flush_lsn</code>, dan <code>replay_lsn</code> semuanya bernilai sama, yaitu <code>0/304F638</code>, dan itu berarti tidak ada data yang tertinggal: primary sudah mengirim, replica sudah menulis, sudah men-flush, dan sudah memutar ulang semuanya. Kolom <code>sync_state = async</code> menegaskan bahwa replikasi ini asinkron, sehingga primary tidak menunggu konfirmasi replica sebelum menyatakan commit berhasil. <code>pg_replication_slots</code> kemudian menunjukkan slot <code>replication_slot</code> bertipe <code>physical</code> dengan <code>active = t</code>, <code>confirmed_flush_lsn = 0/304F638</code>, dan <code>wal_status = reserved</code>. Status <i>reserved</i> itu maksudnya WAL masih ditahan dan belum akan dihapus, persis seperti yang diharapkan dari sebuah slot.
</p>

Untuk melihat status pada server replica:

```bash
der
```

<p align="center"><img src="images/18_der.png" alt="Hasil query pg_is_in_recovery di replica" width="700"></p>

<p align="center"><i>Gambar 4.18 — Replica mengembalikan nilai true pada pg_is_in_recovery().</i></p>

#### Pembahasan

<p align="justify">
Psql di replica dibuka dengan cara yang sama seperti di primary. Query <code>SELECT pg_is_in_recovery()</code> mengembalikan <code>t</code>, dan satu huruf itu sudah cukup untuk memastikan node ini berperan sebagai standby yang sedang memutar ulang WAL. Konsekuensinya jelas: node ini bisa dibaca, tetapi menolak operasi tulis dengan pesan bahwa server berada dalam mode recovery. Sebelum ada tabel apa pun, pemeriksaan <code>\dt</code> belum banyak memberi informasi, tetapi justru di sinilah baseline-nya diambil supaya perubahan setelah manipulasi data di primary nanti bisa dibandingkan secara adil.
</p>

Untuk melihat efek replikasi, dibuat tabel dan diisi data di primary, lalu kondisinya dibandingkan dengan replica.

**Sebelum Pembuatan Tabel**

_Primary_

<p align="center"><img src="images/19_Primary_Sebelum_Pembuatan_Tabel.png" alt="Daftar tabel di primary sebelum pembuatan tabel" width="700"></p>

<p align="center"><i>Gambar 4.19 — Kondisi primary sebelum tabel dibuat.</i></p>

#### Pembahasan

<p align="justify">
Di primary, <code>dep</code> lalu <code>psql -U zuser -d zdb</code> dan <code>\dt</code> menghasilkan <code>Did not find any tables.</code> Kondisi kosong ini sengaja didokumentasikan sebagai titik awal. Tanpa baseline seperti ini, kemunculan tabel di replica nanti bisa saja dikira berasal dari proses lain, padahal satu-satunya sumber perubahan adalah perintah yang dijalankan di primary. Jadi pemeriksaan sekecil ini sebenarnya berfungsi sebagai kontrol di dalam percobaan.
</p>

_Replica_

<p align="center"><img src="images/20_Primary_Sebelum_Pembuatan_Tabel.png" alt="Daftar tabel di replica sebelum pembuatan tabel" width="700"></p>

<p align="center"><i>Gambar 4.20 — Kondisi replica sebelum tabel dibuat, sama dengan primary.</i></p>

#### Pembahasan

<p align="justify">
Pemeriksaan yang sama di replica juga menghasilkan <code>Did not find any tables.</code> Hasil yang identik ini bukan kebetulan, melainkan bukti pertama bahwa kedua node memang berbagi keadaan yang sama sejak awal: replica dibangun dari <code>pg_basebackup</code> atas primary, sehingga katalog, user, dan database-nya persis sama. Kalau di tahap ini hasilnya berbeda, berarti ada masalah pada proses backup atau replica sebenarnya membaca data direktori lain, dan percobaan replikasi tidak perlu dilanjutkan sebelum itu dibereskan.
</p>

**Memanipulasi Data Pada _Primary_**

<p align="center"><img src="images/21_Manipulasi_Data_Primary.png" alt="Pembuatan tabel dan insert data di primary" width="700"></p>

<p align="center"><i>Gambar 4.21 — Pembuatan tabel dan pengisian data di primary.</i></p>

#### Pembahasan

<p align="justify">
Manipulasi data dilakukan di primary: <code>CREATE TABLE testrep (first INT, second VARCHAR(15));</code> lalu <code>SELECT * FROM testrep;</code> yang masih kosong, dilanjutkan dua kali <code>INSERT</code> untuk baris <code>(21, 'Test pertama')</code> dan <code>(23, 'Test ke dua')</code>, dan diakhiri <code>SELECT</code> yang menampilkan dua baris tersebut. Perhatikan bahwa tidak ada <code>BEGIN</code> dan <code>COMMIT</code> yang ditulis, sehingga setiap perintah berjalan dalam transaksi implisit dan langsung di-commit. Ini penting untuk replikasi: WAL hanya memuat perubahan dari transaksi yang sudah commit, jadi kalau data dibiarkan dalam transaksi yang belum di-commit, replica tidak akan pernah menerimanya. Di primary sendiri hasilnya langsung terlihat karena pembacaan terjadi pada node yang sama yang menulis.
</p>

Secara otomatis, manipulasi data tersebut akan direplikasi ke server replica:

<p align="center"><img src="images/22_Manipulasi_Data_Primary.png" alt="Data hasil replikasi terlihat di replica" width="700"></p>

<p align="center"><i>Gambar 4.22 — Data yang sama muncul di replica tanpa insert manual.</i></p>

#### Pembahasan

<p align="justify">
Ketika dicek di replica, <code>\dt</code> yang pertama masih menjawab <code>Did not find any tables.</code>, tetapi <code>\dt</code> yang dijalankan beberapa saat kemudian sudah menampilkan tabel <code>testrep</code>, dan <code>SELECT * FROM testrep;</code> mengembalikan dua baris yang sama persis dengan primary. Perbedaan dua hasil <code>\dt</code> itu bukan kesalahan, melainkan demonstrasi paling jujur dari replikasi asinkron: primary sudah commit, tetapi replica butuh waktu sepersekian detik untuk menerima dan memutar ulang WAL-nya. Inilah yang dimaksud konsistensi eventual dalam praktik, dan justru karena jedanya terlihat, kita jadi paham bahwa "sudah sama" bukan berarti "sama pada milidetik yang sama". Yang perlu dicatat, tidak ada satu pun perintah tulis yang dijalankan di replica; semua data di sana berasal dari replay WAL.
</p>

#### High-Availability

**Primary server mati**

<p align="center"><img src="images/23_Primary_Server_Mati.png" alt="Menghentikan container primary" width="700"></p>

<p align="center"><i>Gambar 4.23 — Primary dihentikan untuk menguji skenario kegagalan.</i></p>

#### Pembahasan

<p align="justify">
Untuk menguji skenario kegagalan, primary dimatikan dengan <code>docker-compose stop postgres_primary</code> dan Compose melaporkan container <code>streaming-replication-postgres_primary-1</code> berhenti. Replica tidak ikut mati karena ia container terpisah, tetapi perannya sebagai standby langsung terasa: koneksi streaming terputus, dan dari log sebelumnya terlihat replica menulis <code>replication terminated by primary server</code> lalu <code>waiting for WAL to become available</code>. Dalam kondisi ini replica masih bisa melayani pembacaan data yang sudah ia miliki, tetapi tidak ada lagi node yang menerima tulisan, sehingga aplikasi yang butuh read-write praktis berhenti. Di sinilah terlihat bahwa replikasi saja belum cukup; tanpa mekanisme promosi, ketersediaan sistem belum benar-benar terjaga.
</p>

Setelah kita mengetahui bahwa primary server dalam kondisi down, kita bisa mempromosikan replica menjadi primary dengan perintah <code>pg_promote()</code>:

<p align="center"><img src="images/24_Mempromosikan_replica_menjadi_primary.png" alt="Promosi replica menjadi primary dengan pg_promote" width="700"></p>

<p align="center"><i>Gambar 4.24 — Promosi replica menjadi primary dengan pg_promote().</i></p>

#### Pembahasan

<p align="justify">
Karena tidak ada failover otomatis, promosi dilakukan manual dari dalam replica. Query <code>SELECT pg_is_in_recovery();</code> masih <code>t</code>, lalu <code>SELECT pg_promote();</code> dijalankan dan mengembalikan <code>t</code> sebagai tanda perintah diterima, dan pemeriksaan berikutnya menunjukkan <code>pg_is_in_recovery()</code> sudah berubah menjadi <code>f</code>. Perubahan satu karakter itu bermakna besar: PostgreSQL berhenti memutar ulang WAL, menghapus penanda standby, dan membuka akses read-write, sehingga node yang tadinya hanya bisa dibaca sekarang bisa menerima tulisan. Namun promosi ini punya konsekuensi yang harus disadari. Karena replikasinya asinkron, ada kemungkinan transaksi terakhir di primary belum sampai ke replica, dan transaksi itu hilang. Selain itu, kalau primary lama nanti dihidupkan lagi dalam keadaan masih menganggap dirinya primary, akan ada dua primary yang sama-sama menerima tulisan dan data bisa bercabang; kondisi ini disebut split-brain dan penanganannya memerlukan <code>pg_rewind</code> atau pembangunan ulang replica, bukan sekadar menyalakan container.
</p>

**Untuk mematikan semua primary dan replika**

```bash
dcd
```

<p align="center"><img src="images/25_Mematikan_Primary_dan_Replika.png" alt="Mematikan seluruh container dengan docker compose down" width="700"></p>

<p align="center"><i>Gambar 4.25 — Seluruh container dan network dihapus dengan docker compose down.</i></p>

#### Pembahasan

<p align="justify">
Alias <code>dcd</code> menjalankan <code>docker compose down</code>, dan output-nya menunjukkan tiga resource dihapus: container replica, container primary, dan network <code>streaming-replication_default</code>. <code>dps</code> yang dijalankan setelahnya memang kosong, jadi tidak ada container yang tertinggal. Perbedaan <code>down</code> dan <code>stop</code> perlu dipahami: <code>stop</code> hanya menghentikan container sehingga masih bisa di-<code>start</code> lagi, sedangkan <code>down</code> menghapus container dan network-nya. Karena praktikum ini tidak mendefinisikan named volume, data PostgreSQL ikut hilang saat container dihapus, sehingga <code>docker compose up</code> berikutnya akan menjalankan initdb dan <code>pg_basebackup</code> dari awal. Untuk percobaan yang ingin datanya bertahan, volume harus ditambahkan secara eksplisit.
</p>

### 4.2 Replikasi Master-Master Menggunakan Apache Ignite 3

#### Struktur Direktori dan File

```text
src--ApacheIgnite/
├── sql/
│   ├── current_catalog.sql
│   ├── ee_and_cust.sql
│   ├── invoices.sql
│   ├── media_and_genre.sql
│   ├── schema.sql
│   └── tracks.sql
├── docker-compose.yaml
└── env.sh
```

<p align="center"><img src="images/26_Struktur_Direktori_ApacheIgnite.png" alt="Struktur direktori Apache Ignite" width="700"></p>

<p align="center"><i>Gambar 4.26 — Struktur direktori praktikum Apache Ignite.</i></p>

#### Pembahasan

<p align="justify">
Folder <code>src--ApacheIgnite</code> berisi <code>docker-compose.yaml</code>, <code>env.sh</code>, dan subfolder <code>sql</code> dengan enam berkas. Berkas SQL-nya bukan ditulis sendiri, melainkan diambil dari paket <code>sql.zip</code> pada dokumentasi quick start Apache Ignite 3, lalu diekstrak. Isinya mengikuti dataset contoh Chinook: <code>schema.sql</code> untuk membuat tabel, <code>current_catalog.sql</code>, <code>tracks.sql</code>, <code>media_and_genre.sql</code>, <code>ee_and_cust.sql</code>, dan <code>invoices.sql</code> untuk mengisi datanya. Folder <code>sql</code> sengaja dipisahkan karena nanti harus di-mount ke dalam container CLI; tanpa mount, perintah <code>sql --file=...</code> tidak akan menemukan berkasnya karena container tidak tahu isi filesystem host.
</p>

Untuk file <code>docker-compose.yaml</code> serta sekumpulan perintah SQL, semuanya diperoleh dari dokumentasi resmi Apache Ignite 3 pada <https://ignite.apache.org/docs/ignite3/latest/quick-start/explore-sql>.

Kemudian dibuat file bernama <code>env.sh</code> untuk keperluan shortcut dan diisi dengan perintah:

<p align="center"><img src="images/27_File_env_sh_Apache.png" alt="Isi berkas env.sh untuk Apache Ignite" width="700"></p>

<p align="center"><i>Gambar 4.27 — Alias yang dipakai pada praktikum Apache Ignite.</i></p>

#### Pembahasan

<p align="justify">
Isinya mirip <code>env.sh</code> pada praktik pertama, tetapi ada dua alias tambahan yang khusus untuk Ignite. <code>dclm</code> menjalankan CLI dengan folder <code>sql</code> di-mount ke <code>/opt/ignite/sql</code>, sedangkan <code>dcli</code> menjalankan CLI tanpa mount. Keduanya memakai <code>--network=host</code> supaya proses CLI yang hidup di dalam container bisa menjangkau <code>http://localhost:10300</code> di host. Pada <code>dclm</code> terdapat tambahan <code>MSYS_NO_PATHCONV=1</code> yang khas Git Bash di Windows: tanpa variabel itu, path <code>./sql:/opt/ignite/sql</code> bisa diterjemahkan ulang menjadi path Windows dan mount-nya gagal. Perbedaan kecil semacam ini biasanya baru ketahuan saat perintah error, jadi menuliskannya langsung di alias jauh lebih aman daripada mengandalkan ingatan.
</p>

#### Menjalankan Docker Compose

<p align="center"><img src="images/28_Menjalankan_docker_compose_apache.png" alt="Menjalankan cluster Ignite dengan docker compose" width="700"></p>

<p align="center"><i>Gambar 4.28 — Proses pengambilan image dan penyalakan tiga node.</i></p>

#### Pembahasan

<p align="justify">
Setelah <code>source env.sh</code>, <code>dcu</code> dijalankan dan Compose mengunduh image <code>apacheignite/ignite:3.1.0</code> selama sekitar 56 detik, membuat network <code>ignite3_default</code>, lalu menyalakan tiga container: <code>ignite3-node1-1</code>, <code>ignite3-node2-1</code>, dan <code>ignite3-node3-1</code>. Nama <i>ignite3</i> itu bukan berasal dari nama folder, melainkan dari baris <code>name: ignite3</code> di dalam file compose. Ketiga node memakai definisi yang sama lewat anchor <code>x-ignite-def</code>, dan yang membedakan hanya argumen <code>--node-name</code> serta port yang dipublikasikan. Konfigurasi tambahan diberikan sebagai <code>configs</code> yang menulis <code>/opt/ignite/etc/ignite-config.conf</code>, dan di dalamnya <code>nodeFinder.netClusterNodes</code> menyebut ketiga nama node pada port 3344 agar mereka bisa saling menemukan.
</p>

Setelah proses pull selesai dan docker-compose telah up, maka status container akan tampil sebagai berikut:

<p align="center"><img src="images/29_Cek_status_Docker_Apache.png" alt="Status tiga container Apache Ignite" width="700"></p>

<p align="center"><i>Gambar 4.29 — Status ketiga node Apache Ignite beserta port yang dipublikasikan.</i></p>

#### Pembahasan

<p align="justify">
<code>dps</code> menampilkan tiga container dengan image yang sama dan status <code>Up</code>, tanpa keterangan <i>healthy</i>. Ini bukan masalah, karena pada compose Ignite tidak didefinisikan healthcheck seperti pada PostgreSQL; Compose hanya tahu prosesnya masih hidup, bukan apakah node sudah siap menerima koneksi. Dari kolom PORTS terlihat pola yang akan dipakai terus: node1 membuka 10300 dan 10800, node2 membuka 10301 dan 10801, node3 membuka 10302 dan 10802. Port 10300-an adalah REST API untuk operasi administratif sekaligus target koneksi CLI, sedangkan 10800-an adalah port yang nanti dipakai aplikasi untuk terhubung. Pemetaan ini yang membuat tiga node di dalam satu network bisa diakses dari host lewat localhost dengan nomor berbeda.
</p>

Setiap container yang berjalan di dalam network Docker memiliki IP internal. Untuk mengecek IP dari masing-masing node:

```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <CONTAINER_ID_ATAU_NAMA>
```

Contoh:

```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ignite3-node1-1
```

<p align="center"><img src="images/30_Cek_Alamat_IP.png" alt="Alamat IP internal ketiga node" width="700"></p>

<p align="center"><i>Gambar 4.30 — Alamat IP internal masing-masing node.</i></p>

#### Pembahasan

<p align="justify">
Hasilnya node1 <code>172.18.0.3</code>, node2 <code>172.18.0.2</code>, dan node3 <code>172.18.0.4</code>, semuanya berada di network <code>ignite3_default</code>. Informasi ini berguna untuk memastikan ketiga node benar-benar satu network dan bisa saling berkomunikasi, tetapi untuk pemakaian sehari-hari nama service seperti <code>node1</code> atau <code>node2</code> lebih praktis karena Docker menyediakan DNS internal yang menerjemahkan nama itu ke IP yang sesuai. Perlu diingat IP container bisa berubah setiap kali network dibuat ulang, jadi alamat ini jangan di-hardcode di aplikasi.
</p>

#### Inisialisasi Cluster

Jalankan Apache Ignite CLI (atau gunakan alias <code>dcli</code>):

```bash
docker run --rm -it --network=host -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 apacheignite/ignite:3.1.0 cli
```

<p align="center"><img src="images/31_Masuk_ApacheIgnite.png" alt="Apache Ignite CLI terhubung ke node default" width="700"></p>

<p align="center"><i>Gambar 4.31 — Masuk ke Apache Ignite CLI dan terhubung ke node1.</i></p>

#### Pembahasan

<p align="justify">
Karena memakai <code>--network=host</code>, proses CLI berbagi network dengan host sehingga <code>localhost:10300</code> bisa dijangkau. Saat pertama dibuka, CLI menampilkan banner Apache Ignite 3 versi 3.1.0 lalu bertanya apakah ingin terhubung ke node default <code>http://localhost:10300</code>. Jawaban <code>Y</code> membuat prompt berubah menjadi <code>[node1]</code>, yang menandakan CLI sudah terhubung ke node1 dan siap menerima perintah administratif. Sebelum cluster diinisialisasi, CLI bahkan memberi tahu bahwa cluster belum diinisialisasi, dan petunjuk itu yang menjadi langkah berikutnya.
</p>

Lalu inisialisasi cluster dengan perintah:

```bash
cluster init --name=ignite3 --metastorage-group=node1,node2,node3
```

<p align="center"><img src="images/32_Menginisialisasi_Cluster.png" alt="Inisialisasi cluster Apache Ignite" width="700"></p>

<p align="center"><i>Gambar 4.32 — Inisialisasi cluster berhasil dijalankan.</i></p>

#### Pembahasan

<p align="justify">
Perintah ini membentuk cluster dengan nama <code>ignite3</code> dan menentukan node mana yang menyimpan metadata cluster. Ketiga node sengaja dipilih semua karena metadata itu dikelola dengan mekanisme consensus; dengan jumlah ganjil, pemilihan pemimpin tetap bisa dilakukan meskipun satu node bermasalah. Perintah ini hanya boleh dijalankan sekali, dan hasilnya <code>Cluster was initialized successfully</code>. Kalau perintah yang sama diulang, sistem akan menolak karena cluster sudah terbentuk.
</p>

Kemudian cek status cluster dengan perintah:

```bash
cluster status
```

<p align="center"><img src="images/33_Verifikasi_Status_Cluster.png" alt="Status cluster Apache Ignite" width="700"></p>

<p align="center"><i>Gambar 4.33 — Verifikasi status cluster melalui CLI.</i></p>

#### Pembahasan

<p align="justify">
Output-nya cukup padat: <code>[name: ignite3, nodes: 3, status: active, cmgNodes: [node1, node2, node3], msNodes: [node1, node2, node3]]</code>. Status <i>active</i> berarti cluster sudah siap melayani, <code>nodes: 3</code> memastikan tidak ada node yang gagal bergabung, dan <code>cmgNodes</code> menunjukkan ketiga node tergabung dalam cluster management group. Informasi ini yang membedakan cluster sehat dari kumpulan container yang kebetulan hidup: tiga container bisa saja berjalan tanpa saling mengenali, dan <code>cluster status</code> adalah cara cepat untuk memastikan mereka benar-benar satu cluster.
</p>

Kemudian, jika ingin masuk lagi ke CLI dengan perintah yang sama, maka tidak memerlukan inisialisasi lagi.

<p align="center"><img src="images/34_Menjalankan_ApacheIgnite.png" alt="Masuk kembali ke CLI tanpa inisialisasi ulang" width="700"></p>

<p align="center"><i>Gambar 4.34 — Masuk kembali ke CLI tanpa perlu inisialisasi ulang.</i></p>

#### Pembahasan

<p align="justify">
CLI tetap menanyakan koneksi ke node default, dan setelah dijawab <code>Y</code> prompt <code>[node1]</code> langsung muncul tanpa pesan bahwa cluster belum diinisialisasi. Artinya informasi cluster tersimpan di metastorage dan dibaca ulang oleh CLI, bukan disimpan di memori sesi CLI. Namun ada catatan penting: karena compose ini tidak memakai volume permanen, metadata itu hanya bertahan selama container hidup. Begitu <code>down</code> dijalankan dan container dihapus, cluster harus diinisialisasi lagi dari awal.
</p>

#### Eksekusi Perintah SQL

**Memuat dan Mengeksekusi File Skema SQL**

```bash
sql --file=/opt/ignite/sql/schema.sql
```

<p align="center"><img src="images/35_Perintah_SQL.png" alt="Eksekusi schema.sql melalui CLI" width="700"></p>

<p align="center"><i>Gambar 4.35 — Eksekusi berkas schema.sql dari dalam CLI.</i></p>

#### Pembahasan

<p align="justify">
Perintah ini mengeksekusi berkas skema langsung dari dalam CLI tanpa harus masuk ke mode SQL interaktif. Output-nya sederhana, hanya <code>Updated 0 rows.</code> yang berulang, dan itu wajar karena isi <code>schema.sql</code> mayoritas perintah DDL seperti <code>CREATE TABLE</code> yang tidak mengubah baris data. Angka nol di sini jangan dibaca sebagai kegagalan; yang perlu dipastikan justru tidak ada pesan error di antara baris-baris itu. Cara ini lebih praktis daripada menyalin isi berkas ke prompt, terutama karena skemanya cukup panjang dan rawan salah ketik.
</p>

Masuk ke mode SQL dengan perintah:

```bash
sql
```

kemudian gunakan perintah:

```sql
SELECT * FROM system.tables WHERE schema = 'PUBLIC';
```

<p align="center"><img src="images/36_Perintah_SQL_Table.png" alt="Daftar tabel pada schema PUBLIC" width="700"></p>

<p align="center"><i>Gambar 4.36 — Daftar tabel pada schema PUBLIC di node1.</i></p>

<p align="center"><img src="images/37_Perintah_Menjalankan_SQL.png" alt="Eksekusi seluruh berkas SQL data" width="700"></p>

<p align="center"><i>Gambar 4.37 — Eksekusi berkas SQL pengisi data pada cluster.</i></p>

#### Pembahasan

<p align="justify">
Hasilnya sebelas tabel: ALBUM, PLAYLISTTRACK, TRACK, CUSTOMER, MEDIATYPE, PLAYLIST, ARTIST, INVOICELINE, EMPLOYEE, GENRE, dan INVOICE. Yang menarik justru kolom <code>ZONE_NAME</code>: sebagian besar tabel berada di zone <code>CHINOOK</code>, tetapi MEDIATYPE dan GENRE berada di <code>CHINOOKREPLICATED</code>. Di Ignite, zone menentukan bagaimana data disebar dan digandakan; zone <code>CHINOOK</code> memakai distribusi berdasarkan primary key sehingga tiap partisi dimiliki node tertentu, sedangkan <code>CHINOOKREPLICATED</code> menggandakan seluruh isi tabel ke semua node. Pemisahan ini masuk akal karena MEDIATYPE dan GENRE adalah data referensi yang kecil dan sering dibaca bersama tabel lain, sehingga menyalinnya ke semua node lebih menguntungkan daripada mendistribusikannya. Berkas SQL pengisi data lainnya kemudian dieksekusi dengan pola yang sama, dan jumlah baris yang dilaporkan pada gambar berikut menjadi penanda bahwa datanya benar-benar masuk: <code>current_catalog.sql</code> mengubah 275 dan 347 baris, <code>media_and_genre.sql</code> 25 dan 5 baris, <code>tracks.sql</code> 1000, 1000, 1000, dan 503 baris, <code>ee_and_cust.sql</code> 8 dan 59 baris, sedangkan <code>invoices.sql</code> berisi beberapa perintah yang masing-masing mengubah 412, 240, 18, 715, dan beberapa blok 1000 baris.
</p>

#### Verifikasi Propagasi Data

Untuk memeriksa apakah perubahan pada <http://localhost:10300> tersebut telah dipropagasi ke node-node lainnya, kita bisa memeriksa dengan melakukan koneksi ke node lainnya. Berikut adalah node di <http://localhost:10301>:

```bash
connect http://localhost:10301
```

<p align="center"><img src="images/38_Pindah_Koneksi.png" alt="Berpindah koneksi CLI ke node2" width="700"></p>

<p align="center"><i>Gambar 4.38 — Berpindah koneksi CLI ke node2 pada port 10301.</i></p>

#### Pembahasan

<p align="justify">
CLI memberi peringatan bahwa saat ini masih terhubung ke 10300 dan menanyakan apakah ingin pindah; jawaban <code>Y</code> membuat prompt berubah menjadi <code>[node2]</code>. Perpindahan ini hanya mengganti node tujuan koneksi, bukan membuat cluster baru, sehingga yang akan terlihat di node2 adalah cluster yang sama dari sudut pandang berbeda. Langkah ini penting karena membaca data dari node yang sama tempat data ditulis tidak membuktikan apa pun tentang replikasi.
</p>

Kemudian cek propagasi tabel:

```sql
SELECT * FROM system.tables WHERE schema = 'PUBLIC';
```

<p align="center"><img src="images/39_Cek_Propagasi_Table.png" alt="Daftar tabel yang sama di node2" width="700"></p>

<p align="center"><i>Gambar 4.39 — Daftar tabel di node2 identik dengan node1.</i></p>

#### Pembahasan

<p align="justify">
Query yang sama di node2 mengembalikan daftar yang sama persis, lengkap dengan <code>ZONE_NAME</code> dan <code>TABLE_ID</code> yang identik. Kesamaan metadata ini menunjukkan bahwa definisi tabel tidak disimpan terpisah di tiap node, melainkan dikelola sebagai bagian dari cluster dan disebarkan lewat mekanisme consensus. Jadi sebelum sampai ke data, lapisan skema sudah lebih dulu konsisten di ketiga node. Kalau daftar tabelnya berbeda, bisa dipastikan ada node yang tidak benar-benar bergabung ke cluster, dan itu biasanya terlihat lebih awal pada <code>cluster status</code>.
</p>

Contoh query untuk analytics:

```sql
SELECT
    CAST(EXTRACT(YEAR FROM i.InvoiceDate) AS VARCHAR) || '-' ||
    CASE
        WHEN EXTRACT(MONTH FROM i.InvoiceDate) < 10
        THEN '0' || CAST(EXTRACT(MONTH FROM i.InvoiceDate) AS VARCHAR)
        ELSE CAST(EXTRACT(MONTH FROM i.InvoiceDate) AS VARCHAR)
    END AS YearMonth,
    COUNT(DISTINCT i.InvoiceId) AS InvoiceCount,
    COUNT(DISTINCT i.CustomerId) AS CustomerCount,
    SUM(i.Total) AS MonthlyRevenue,
    AVG(i.Total) AS AverageOrderValue
FROM
    Invoice i
GROUP BY
    EXTRACT(YEAR FROM i.InvoiceDate), EXTRACT(MONTH FROM i.InvoiceDate)
ORDER BY
    YearMonth DESC;
```

<p align="center"><img src="images/40_Analitik_Table.png" alt="Hasil query analitik di node2 bagian pertama" width="700"></p>

<p align="center"><i>Gambar 4.40 — Hasil query analitik di node2, bagian pertama.</i></p>

<p align="center"><img src="images/41_Analitik_Table.png" alt="Hasil query analitik di node2 bagian kedua" width="700"></p>

<p align="center"><i>Gambar 4.41 — Hasil query analitik di node2, bagian kedua.</i></p>

#### Pembahasan

<p align="justify">
Query itu membentuk <code>YearMonth</code> dari <code>EXTRACT</code> tahun dan bulan yang disambung dengan tanda hubung, memberi nol di depan untuk bulan satu digit, lalu menghitung <code>COUNT(DISTINCT InvoiceId)</code>, <code>COUNT(DISTINCT CustomerId)</code>, <code>SUM(Total)</code>, dan <code>AVG(Total)</code> sebelum dikelompokkan per tahun dan bulan serta diurutkan menurun. Hasilnya mencakup rentang 2020-01 sampai 2024-12 dengan 6–7 invoice per bulan. Angka <code>MonthlyRevenue</code> yang sebagian besar 37,62 dan <code>AverageOrderValue</code> sekitar 5,37 terlihat mencurigakan kalau dibaca sekilas, tetapi itu memang karakter data contoh yang nilainya kecil dan berulang; beberapa bulan seperti 2023-05 dan 2022-06 punya nilai berbeda karena jumlah dan komposisi invoice-nya berbeda. Yang penting bukan besar angkanya, melainkan bahwa query yang sama bisa dijalankan di node mana pun.
</p>

Mari memeriksa <http://localhost:10302>:

<p align="center"><img src="images/42_Memeriksa_analitik.png" alt="Hasil query analitik di node3 bagian pertama" width="700"></p>

<p align="center"><i>Gambar 4.42 — Hasil query analitik di node3, bagian pertama.</i></p>

<p align="center"><img src="images/43_Memeriksa_analitik.png" alt="Hasil query analitik di node3 bagian kedua" width="700"></p>

<p align="center"><i>Gambar 4.43 — Hasil query analitik di node3, bagian kedua.</i></p>

#### Pembahasan

<p align="justify">
Hasil query di node3 sama dengan node2 hingga digit desimal. Dengan tiga node yang memberi jawaban identik, klaim master-master menjadi masuk akal: tidak ada satu node pun yang diperlakukan sebagai cadangan pasif, karena semuanya melayani pembacaan dan semuanya bisa menerima penulisan. Perlu dicatat bahwa kesamaan ini bukan karena ada satu primary yang menyalin ke dua node lain, melainkan karena data memang didistribusikan dan direplikasi di tingkat partisi oleh Ignite sendiri. Itu sebabnya hasilnya konsisten meskipun koneksi datang dari node yang berbeda.
</p>

#### Menghentikan Cluster

Matikan semua node:

```bash
dcd
```

<p align="center"><img src="images/44_Mematikan_Semua_Node.png" alt="Mematikan seluruh node Apache Ignite" width="700"></p>

<p align="center"><i>Gambar 4.44 — Seluruh node dan network Ignite dihentikan dan dihapus.</i></p>

#### Pembahasan

<p align="justify">
Alias <code>dcd</code> menjalankan <code>docker compose down</code> dan output-nya menunjukkan empat resource dihapus: tiga container node dan network <code>ignite3_default</code>. Sama seperti pada PostgreSQL, tidak ada volume permanen yang didefinisikan, sehingga seluruh data dan metadata cluster ikut hilang. Konsekuensinya, saat praktikum dijalankan lagi, <code>cluster init</code> harus diulang dan semua berkas SQL dieksekusi kembali. Ini bukan kekurangan, melainkan konsekuensi dari pilihan desain untuk lingkungan praktikum yang bersih setiap kali dijalankan; kalau data ingin bertahan, volume harus ditambahkan pada masing-masing node.
</p>

---

## 📝 Kesimpulan

<p align="justify">
Dari dua praktik ini terlihat bahwa replikasi bukan satu konsep tunggal, melainkan sekumpulan pilihan dengan konsekuensi masing-masing. Pada PostgreSQL, streaming replication berhasil menyinkronkan primary ke replica lewat WAL: replica terbukti read-only, otomatis mengikuti perubahan, dan dapat dipromosikan menjadi primary saat primary dimatikan. Namun promosi itu manual, replikasinya asinkron, dan tidak ada mekanisme yang mencegah split-brain, sehingga sistem ini baru menyediakan bahan untuk High Availability, belum High Availability yang sesungguhnya. Apache Ignite menunjukkan model yang berbeda: ketiga node setara, semuanya bisa membaca dan menulis, dan perubahan pada satu node terlihat di node lain tanpa perlu promosi apa pun. Perbandingannya cukup jelas — model primary-replica lebih sederhana dan mudah dipahami, tetapi bergantung pada satu titik tulis, sedangkan model master-master lebih tahan terhadap kegagalan satu node dengan harga konfigurasi dan koordinasi yang lebih rumit. Pilihan di antara keduanya tidak ditentukan oleh mana yang lebih modern, melainkan oleh kebutuhan aplikasi: seberapa besar toleransi terhadap kehilangan data, seberapa besar kebutuhan penulisan, dan seberapa siap tim merawat kompleksitasnya.
</p>

---

## 🗒️ Referensi

- PostgreSQL Global Development Group. (2025). _PostgreSQL 18 Documentation — High Availability, Load Balancing, and Replication_. <https://www.postgresql.org/docs/18/high-availability.html>
- PostgreSQL Global Development Group. (2025). _PostgreSQL 18 Documentation — Write-Ahead Logging (WAL) dan pg_basebackup_. <https://www.postgresql.org/docs/18/wal.html>
- Apache Software Foundation. (2025). _Apache Ignite 3 Documentation — Quick Start dan Explore SQL_. <https://ignite.apache.org/docs/ignite3/latest/quick-start/explore-sql>
- Eremeykin. _How to Setup Single Primary PostgreSQL Replication with Docker Compose_. Medium. <https://medium.com/@eremeykin/how-to-setup-single-primary-postgresql-replication-with-docker-compose-98c48f233bbf>
- Docker Inc. (2025). _Docker Documentation — Install Docker Engine dan Docker Compose_. <https://docs.docker.com/>
- Özsu, M. T., & Valduriez, P. (2020). _Principles of Distributed Database Systems_ (4th ed.). Springer.
- Tanenbaum, A. S., & van Steen, M. (2023). _Distributed Systems_ (4th ed.). Maarten van Steen.
- Kleppmann, M. (2017). _Designing Data-Intensive Applications_. O'Reilly Media.
