# Praktikum Minggu 02 - Komunikasi Antar Proses pada Sistem Terdistribusi

**Mata Kuliah:** Praktikum Sistem Terdistribusi dan Terdesentralisasi
**Topik:** Komunikasi Antar Proses pada Sistem Terdistribusi

---

# 📚 Tujuan Praktikum

1. Memahami konsep proses pada sistem operasi dan cara sistem operasi mengelola proses pada satu node.
2. Menampilkan daftar proses yang berjalan pada sistem operasi Windows melalui Task Manager.
3. Menjalankan aplikasi, serta mematikan dan me-restart prosesnya menggunakan perintah pada CMD.
4. Memahami konsep komunikasi antar proses pada sistem terdistribusi dengan membuat server GraphQL menggunakan Python (Strawberry) dan client yang berkomunikasi dengannya.

---

# 📚 Dasar Teori

## Proses

Proses merupakan hasil dari eksekusi program atau aplikasi yang bersifat executable. Proses dikelola oleh sistem operasi dan terdiri atas executable code, data, resources, serta informasi tentang state (stack dan heap). Setiap aplikasi yang dijalankan akan menjadi sebuah proses.

## Proses pada Satu Node

Pada satu node, semua proses berada dalam kendali sistem operasi, mulai dari eksekusi menjadi proses, alokasi resources, pengelolaan proses, hingga komunikasi antar proses. Hal ini bersifat transparan terhadap pengguna, artinya pengguna tidak perlu melihatnya karena di latar belakang semuanya sudah dikelola oleh sistem operasi. Semua proses berjalan pada clock yang sama dan dapat menggunakan shared memory, sehingga tidak perlu dilakukan sinkronisasi dan semua proses akan terurut serta terkendali dengan baik.

## Komunikasi Antar Proses pada Sistem Terdistribusi

Hal ini berbeda dengan pengelolaan proses pada lebih dari satu node di sistem terdistribusi. Antar node tidak berada pada clock yang sama dan tidak memungkinkan penggunaan shared memory, karena setiap node mengelola memory sendiri dan tidak dimungkinkan mengakses shared memory node lain karena alasan keamanan. Dengan demikian, harus ada cara khusus untuk komunikasi antar proses yang berada pada node yang berbeda. Salah satu cara yang dapat digunakan adalah GraphQL. Dengan GraphQL, dibuat server yang melayani query dari client dengan menggunakan spesifikasi GraphQL, sehingga terjadi komunikasi antar proses di client (yang meminta layanan) dengan server (yang melayani permintaan layanan). Peranti pengembangan di kedua sisi tersebut bisa berbeda. Pada praktikum ini, digunakan Python dengan paket Strawberry (https://strawberry.rocks/) untuk membuat server.

## Perintah Windows yang Digunakan

| Perintah                          | Fungsi                                         |
| --------------------------------- | ---------------------------------------------- |
| `tasklist`                        | Menampilkan daftar proses yang sedang berjalan |
| `tasklist \| findstr /i "nama"`   | Mencari proses tertentu berdasarkan nama       |
| `taskkill /IM nama_proses.exe /F` | Mematikan proses secara paksa                  |
| `start "" notepad`                | Menjalankan kembali proses aplikasi            |

---

# ⏩ PEMBAHASAN PRAKTIKUM

## PRAKTIK 1 - PROSES PADA SATU NODE

### 1. Tampilkan berbagai proses yang ada pada Laptop-Windows

<img src="images/01_Tampilan_Proses.png" width="700">

#### Pembahasan

<p align="justify">Ketika Task Manager dibuka, akan terlihat banyak proses yang sedang berjalan di laptop, dan sebenarnya setiap proses itu mewakili satu program yang sedang dieksekusi, baik aplikasi yang kita buka sendiri maupun yang berjalan di latar belakang untuk mendukung sistem. Di sana kita bisa melihat nama proses, PID, serta seberapa banyak CPU dan memori yang dipakai, dan yang penting untuk dipahami adalah semuanya ini diatur oleh sistem operasi secara otomatis, jadi kita sebagai pengguna tidak perlu repot mengurusnya satu per satu.</p>

---

### 2. Jalankan salah satu aplikasi kemudian perlihatkan proses yang dimunculkan oleh aplikasi

Sebagai contoh menjalankan Notepad untuk percobaan:

<img src="images/02_Jalankan_Notepad.png" width="700">

Kemudian untuk melihat proses yang dimunculkan aplikasi tersebut dapat dilihat pada task manager, yaitu sebagai berikut :

<img src="images/04_Proses_Notepad.png" width="700">

<img src="images/03_Detail_Proses.png" width="700">

#### Pembahasan

<p align="justify">Setelah Notepad dijalankan, proses baru bernama notepad.exe muncul di Task Manager, yang artinya aplikasi yang tadinya hanyalah sebuah file program sekarang sedang dieksekusi oleh sistem operasi dan berubah menjadi sebuah proses. Kalau kita lihat ke bagian Details, informasi yang ditampilkan lebih lengkap, misalnya PID dan statusnya, sehingga kita bisa membedakan proses Notepad dengan proses lain yang sedang berjalan.</p>

---

### 3. Merestart dan Mematikan proses yang dimunculkan oleh aplikasi

#### Mematikan Proses

Untuk mematikan proses dapat dilakukan melalui Task Manager:

<img src="images/05_Mematikan_Proses_Via_TaskManager.png" width="700">

#### Pembahasan

<p align="justify">Proses Notepad bisa dimatikan langsung dari Task Manager dengan klik kanan lalu memilih End task, yang sebenarnya sama saja dengan memberi tahu sistem operasi untuk menghentikan proses tersebut. Yang perlu diperhatikan, cara ini mematikan prosesnya, bukan sekadar menutup jendela aplikasinya, jadi benar-benar berhenti di level proses.</p>

---

Kemudian dapat dilakukan juga melalui CMD:

Untuk melihat daftar proses yang sedang berjalan di Windows gunakan perintah:

```powershell
tasklist
```

#### Pembahasan

<p align="justify">Melihat daftar proses lewat CMD bisa dilakukan dengan perintah tasklist, dan hasilnya kurang lebih sama dengan apa yang ditampilkan Task Manager, hanya saja dalam bentuk teks di terminal. Ini berguna karena kadang kita sedang bekerja di CMD dan tidak perlu membuka Task Manager hanya untuk sekadar melihat proses apa saja yang sedang berjalan.</p>

---

Untuk mencari proses dari aplikasi gunakan perintah:

```powershell
tasklist | findstr /i "Nama_Aplikasi"
```

Contoh :

```powershell
tasklist | findstr /i notepad
```

<img src="images/06_Mematikan_Proses_Via_CMD.png" width="700">

#### Pembahasan

<p align="justify">Karena daftar proses dari tasklist biasanya sangat panjang, hasilnya bisa disaring dengan findstr supaya hanya proses yang kita cari yang muncul, misalnya notepad. Tanda /i di belakang findstr membuat pencarian tidak memperbedakan huruf besar dan kecil, jadi penulisan nama proses tidak harus persis sama.</p>

---

Untuk mematikan proses dapat menggunakan perintah

```powershell
taskkill /IM nama_proses.exe /F
```

Contoh :

```powershell
taskkill /IM notepad.exe /F
```

<img src="images/07_Mematikan_Proses_Via_CMD.png" width="700">

#### Pembahasan

<p align="justify">Untuk mematikan prosesnya, digunakan perintah taskkill /IM notepad.exe /F, di mana /IM berarti kita menunjuk proses berdasarkan nama file executablenya dan /F memaksa proses agar berhenti meskipun sedang dalam keadaan tidak merespons. Setelah perintah dijalankan, jendela Notepad langsung tertutup dan prosesnya menghilang dari daftar proses.</p>

---

Untuk memastikan proses berhenti. Gunakan Perintah:

```powershell
tasklist | findstr /i "Nama_Aplikasi"
```

Contoh :

<img src="images/08_Memastikan_Proses_Berhenti.png" width="700">

#### Pembahasan

<p align="justify">Sebagai langkah terakhir, kita bisa memastikan sekali lagi bahwa prosesnya sudah benar-benar berhenti dengan menjalankan tasklist | findstr /i notepad. Kali ini tidak ada hasil yang keluar, yang menandakan proses notepad.exe sudah tidak lagi berjalan di sistem.</p>

---

#### Merestart Proses

Untuk merestart proses dapat dilakukan dengan perintah

```powershell
start "" notepad
```

<img src="images/09_Merestart_Proses.png" width="700">

<img src="images/10_Merestart_Proses.png" width="700">

#### Pembahasan

<p align="justify">Setelah prosesnya dimatikan, Notepad bisa dijalankan kembali dengan perintah start "" notepad di CMD. Tanda "" di sini diperlukan karena perintah start menangkap argumen pertama sebagai judul jendela, jadi tanpa tanda kosong itu justru akan membuat jendela baru yang tidak kita maksud. Begitu perintah dijalankan, proses notepad.exe muncul lagi di Task Manager, yang artinya aplikasinya sudah berjalan normal kembali.</p>

---

## PRAKTIK 2 - KOMUNIKASI ANTAR PROSES pada SISTEM TERDISTRIBUSI

### 1. Instalasi

Petunjuk lengkap instalasi ada di https://docs.astral.sh/uv/getting-started/installation/. Sesuaikan dengan sistem operasi yang digunakan. Berikut adalah contoh di Windows:

```powershell
PS C:\WINDOWS\system32> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
downloading uv 0.13.0 (x86_64-pc-windows-msvc)
installing to C:\Users\LENOVO\.local\bin
  uv.exe
  uvx.exe
  uvw.exe
everything's installed!

To add C:\Users\LENOVO\.local\bin to your PATH, either restart your shell or run:

    set Path=C:\Users\LENOVO\.local\bin;%Path%   (cmd)
    $env:Path = "C:\Users\LENOVO\.local\bin;$env:Path"   (powershell)
PS C:\WINDOWS\system32> $env:Path = "C:\Users\LENOVO\.local\bin;$env:Path"
PS C:\WINDOWS\system32> uv
An extremely fast Python package manager.
```

#### Pembahasan

<p align="justify">Sebelum mulai membuat server GraphQL, kita butuh uv, yaitu package manager untuk Python yang dikenal sangat cepat, dan cara memasangnya di Windows cukup dengan menjalankan satu perintah di PowerShell, yaitu powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex", yang secara otomatis mengunduh dan memasang uv ke folder C:\Users\LENOVO\.local\bin. Setelah terpasang, folder tersebut perlu ditambahkan ke PATH supaya perintah uv bisa dikenali di mana saja, dan begitu dijalankan lagi, uv sudah siap digunakan.</p>

---

Setelah mengatur env variabel untuk uv ($PATH harus berisi - salah satunya - tempat uv di install) yaitu di (C:\Users\LENOVO\.local\bin), uv bisa dijalankan sebagai berikut:

```powershell
PS C:\WINDOWS\system32> uv
An extremely fast Python package manager.

Usage: uv.exe [OPTIONS] <COMMAND>

Commands:
  auth       Manage authentication
  run        Run a command or script
  init       Create a new project
  add        Add dependencies to the project
  remove     Remove dependencies from the project
  version    Read or update the project's version
  sync       Update the project's environment
  lock       Update the project's lockfile
  export     Export the project's lockfile to an alternate format
  tree       Display the project's dependency tree
  format     Format Python code in the project
  check      Run checks on the project
  audit      Audit the project's dependencies
  tool       Run and install commands provided by Python packages
  python     Manage Python versions and installations
  pip        Manage Python packages with a pip-compatible interface
  venv       Create a virtual environment
  build      Build Python packages into source distributions and wheels
  publish    Upload distributions to an index
  workspace  Inspect uv workspaces
  cache      Manage uv's cache
  self       Manage the uv executable
  help       Display documentation for a command

Cache options:
  -n, --no-cache               Avoid reading from or writing to the cache, instead using a temporary directory for the
                                duration of the operation [env: UV_NO_CACHE=]
      --cache-dir <CACHE_DIR>  Path to the cache directory [env: UV_CACHE_DIR=]

Python options:
      --managed-python       Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
      --no-managed-python    Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
      --no-python-downloads  Disable automatic downloads of Python. [env: "UV_PYTHON_DOWNLOADS=never"]

Global options:
  -q, --quiet...
          Use quiet output
  -v, --verbose...
          Use verbose output
      --color <COLOR_CHOICE>
          Control the use of color in output [possible values: auto, always, never]
      --system-certs
          Whether to load TLS certificates from the platform's native certificate store [env: UV_SYSTEM_CERTS=]
      --offline
          Disable network access [env: UV_OFFLINE=]
      --allow-insecure-host <ALLOW_INSECURE_HOST>
          Allow insecure connections to a host [env: UV_INSECURE_HOST=]
      --no-progress
          Hide all progress outputs [env: UV_NO_PROGRESS=]
      --directory <DIRECTORY>
          Change to the given directory prior to running the command [env: UV_WORKING_DIR=]
      --project <PROJECT>
          Discover a project in the given directory [env: UV_PROJECT=]
      --config-file <CONFIG_FILE>
          The path to a `uv.toml` file to use for configuration [env: UV_CONFIG_FILE=]
      --no-config
          Avoid discovering configuration files (`pyproject.toml`, `uv.toml`) [env: UV_NO_CONFIG=]
  -h, --help
          Display the concise help for this command
  -V, --version
          Display the version of uv

Use `uv help` for more details.
```

#### Pembahasan

<p align="justify">Begitu perintah uv diketik, langsung muncul daftar perintah yang bisa dipakai, dan dari situ terlihat bahwa uv bukan hanya untuk menginstall paket, tapi juga bisa mengatur versi Python, membuat virtual environment, sampai mengelola cache. Untuk praktikum ini, yang paling sering dipakai adalah perintah pip, venv, dan python, karena ketiganya menjadi dasar untuk menyiapkan tempat bekerja dan memasang library yang dibutuhkan.</p>

---

### 2. Update

Update diperlukan jika menginginkan tetap menggunakan versi terbaru dari uv.

Gunakan Perintah:

```powershell
uv self update
```

Contoh:

```powershell
PS C:\WINDOWS\system32> uv self update
info: Checking for updates...
success: You're already on version v0.13.0 of uv (the latest version).
```

#### Pembahasan

<p align="justify">Sebelum mulai bekerja, ada baiknya uv diperbarui dulu dengan perintah uv self update supaya kita memakai versi terbaru yang biasanya sudah membawa perbaikan bug dan fitur baru. Pada contoh di atas, ternyata versi yang terpasang sudah yang terbaru, jadi tidak ada yang diunduh, dan kita bisa langsung lanjut ke langkah berikutnya.</p>

---

### 3. Membuat Workspace

Buat Direktori terlebih dahulu

<img src="images/11_Membuat_Workspace-01.png" width="700">

#### Pembahasan

<p align="justify">Langkah pertama adalah membuat direktori kerja yang akan dijadikan tempat seluruh file praktikum disimpan. Membuat direktori terpisah itu penting supaya file-file proyek tidak tercampur dengan file lain, dan kalau nanti ingin dipindahkan atau dihapus, semuanya sudah rapi dalam satu folder.</p>

---

Kemudian masuk kedalam direktori

<img src="images/12_Masuk_Direktori.png" width="700">

#### Pembahasan

<p align="justify">Setelah direktori dibuat, kita masuk ke dalamnya dengan perintah cd supaya semua perintah berikutnya dijalankan di dalam folder kerja itu. Kalau tidak masuk dulu ke direktori tersebut, file dan environment yang dibuat bisa saja tersimpan di tempat lain dan jadi sulit ditemukan.</p>

---

Lalu cek versi python yang ingin digunakan. Jika versi Python yang diinginkan belum ada, akan dilakukan download dan instalasi lebih dulu. Untuk cek versi python dapat dilakukan dengan cara:

<img src="images/13_Cek_Python_List.png" width="700">

#### Pembahasan

<p align="justify">Di dalam direktori kerja, kita bisa memeriksa versi Python apa saja yang tersedia di sistem dengan perintah uv python list. Kalau versi yang diinginkan belum ada, uv akan mengunduh dan memasangnya sendiri secara otomatis, jadi kita tidak perlu repot menginstal Python secara manual.</p>

---

Pada direktori tersebut, akan dibuat file .python-version:

<img src="images/14_Membuat_Python-Version.png" width="700">

#### Pembahasan

<p align="justify">Agar proyek ini selalu memakai versi Python yang sama, dibuatlah file .python-version yang isinya menyebutkan versi Python yang dipakai. Dengan begitu, setiap kali bekerja di direktori ini, uv otomatis memakai versi yang sudah ditentukan dan tidak akan tertukar dengan Python versi lain yang terpasang di sistem.</p>

---

### 4. Buat Environment

<img src="images/15_Membuat_Environment.png" width="700">

#### Pembahasan

<p align="justify">Selanjutnya dibuat environment virtual dengan uv venv, yang berfungsi sebagai wadah terisolasi khusus untuk proyek ini. Dengan environment sendiri, paket-paket yang diinstal tidak akan bercampur dengan paket proyek lain atau Python sistem, jadi kalau nanti ada perbedaan versi library, tidak akan saling mengganggu.</p>

---

Kemudian Mengaktifkan dengan perintah

```powershell
.\.venv\Scripts\Activate
```

<img src="images/16_Mengaktifkan_Environment.png" width="700">

#### Pembahasan

<p align="justify">Setelah environment dibuat, kita mengaktifkannya dengan menjalankan skrip Activate di dalam folder .venv. Begitu aktif, akan muncul tanda (.venv) di awal baris perintah, yang artinya semua perintah Python dan instalasi paket dari sekarang akan berjalan di dalam environment ini, bukan di Python sistem.</p>

---

Lalu jika ingin keluar dari env. Gunakan perintah:

```powershell
deactivate
```

<img src="images/17_Deactivate.png" width="700">

#### Pembahasan

<p align="justify">Kalau sudah selesai bekerja, environment bisa ditinggal dengan perintah deactivate, dan tanda (.venv) di baris perintah akan menghilang, yang artinya kita kembali ke Python sistem. Cara ini lebih rapi daripada sekadar menutup terminal, karena environment benar-benar dilepas dan tidak meninggalkan pengaruh ke sesi berikutnya.</p>

---

### 5. Mengelola Paket

Paket pertama yaitu pandas, untuk menginstall nya dapat menggunakan perintah

```powershell
uv pip install pandas
```

<img src="images/18_Pandas_Packages.png" width="700">

#### Pembahasan

<p align="justify">Paket pertama yang dipasang adalah pandas, yaitu library Python yang dipakai untuk mengolah data, dan cara memasangnya cukup dengan uv pip install pandas. Perintah ini mencari paket di internet, mengunduhnya, lalu memasangnya ke environment yang sedang aktif, semuanya otomatis tanpa perlu langkah tambahan.</p>

---

Paket kedua yaitu untuk GraphQL, menggunakan perintah

```powershell
uv pip install "strawberry-graphql[cli]"
```

<img src="images/19_GraphQL_Packages.png" width="700">

#### Pembahasan

<p align="justify">Paket kedua adalah strawberry-graphql dengan tambahan [cli], yang berarti selain library-nya, perintah baris strawberry ikut terpasang sehingga server bisa langsung dijalankan dari terminal. Pasangannya terlihat cukup banyak karena strawberry membawa beberapa dependensi lain yang dibutuhkannya, seperti graphql-core dan uvicorn, dan semuanya diurus otomatis oleh uv.</p>

---

Lalu untuk melihat paket yang terpasang menggunakan perintah

```powershell
uv pip list
```

<img src="images/20_Cek_paket_Terpasang.png" width="700">

#### Pembahasan

<p align="justify">Untuk memastikan semuanya sudah terpasang dengan benar, daftar paket di environment bisa dilihat dengan uv pip list. Dari outputnya terlihat pandas dan strawberry-graphql beserta versinya sudah ada, dan di situ juga terlihat paket-paket dependensi yang ikut terpasang sebelumnya.</p>

---

Untuk menyimpan daftar paket ke requirements.txt gunakan perintah

```powershell
uv pip freeze > requirements.txt
```

#### Pembahasan

<p align="justify">Agar daftar paket ini bisa dipakai lagi di lain waktu, isinya disimpan ke file requirements.txt dengan uv pip freeze yang ditujukan ke file tersebut. File ini nantinya berguna kalau proyek ingin dijalankan di komputer atau environment lain, karena semua paket bisa dipasang ulang hanya dengan membaca daftar di file ini.</p>

---

Kemudian untuk melihat isi file nya dapat menggunakan perintah

```powershell
cat requirements.txt
```

<img src="images/21_Menyimpan_Daftar_Paket.png" width="700">

#### Pembahasan

<p align="justify">Terakhir, isi file requirements.txt bisa dicek dengan cat, dan di dalamnya terlihat daftar paket beserta versi persisnya, misalnya pandas dan strawberry-graphql. Mencantumkan versi itu penting supaya kalau dipasang ulang di tempat lain, hasilnya sama persis dan tidak berubah karena versi baru yang mungkin tidak kompatibel.</p>

---

### 6. Menjalankan source code yang sudah disediakan pada https://strawberry.rocks/docs

1. Mendefinisikan skema

Buat file bernama schema.py dengan isi sebagai berikut

```python
import typing
import strawberry


@strawberry.type
class Book:
    title: str
    author: str


@strawberry.type
class Query:
    books: typing.List[Book]
```

<img src="images/22_Membuat_File_schema.py.png" width="700">

#### Pembahasan

<p align="justify">Server GraphQL dimulai dengan membuat file schema.py, dan di dalamnya didefinisikan tipe Book yang punya dua field, yaitu title dan author, serta tipe Query yang menyediakan field books berupa daftar Book. Definisi ini menjadi bentuk data yang nantinya bisa diminta oleh client, dan strawberry membaca dekorator @strawberry.type untuk mengubah kelas Python biasa menjadi tipe GraphQL.</p>

---

2. Definisikan kumpulan data

Contoh fungsi yang mengembalikan beberapa buku

```python
def get_books():
    return [
        Book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
        ),
    ]
```

<img src="images/23_Mendefinisikan_Kumpulan_Data.png" width="700">

#### Pembahasan

<p align="justify">Karena server butuh data untuk dilayani, dibuatlah fungsi get_books yang mengembalikan daftar buku, dalam hal ini satu buku berjudul The Great Gatsby karya F. Scott Fitzgerald. Fungsi ini nantinya akan dihubungkan ke field books, jadi setiap kali ada yang meminta data buku, server cukup memanggil fungsi ini.</p>

---

3. Mendefinisikan Resolver

Perbarui query pada program schema.py

```python
@strawberry.type
class Query:
    books: typing.List[Book] = strawberry.field(resolver=get_books)
```

<img src="images/24_Mendefinisikan_Resolver.png" width="700">

#### Pembahasan

<p align="justify">Agar field books benar-benar mengembalikan data, field tersebut dihubungkan ke fungsi get_books lewat strawberry.field(resolver=get_books). Tanpa resolver ini, field books hanya akan bernilai kosong karena server tidak tahu harus mengambil data dari mana, dan setelah dihubungkan, setiap permintaan ke field books akan otomatis menjalankan fungsi tersebut.</p>

---

4. Buat skema dan jalankan

Untuk membuat skema, tambahkan kode berikut:

```python
schema = strawberry.Schema(query=Query)
```

<img src="images/25_Membuat_Skema.png" width="700">

#### Pembahasan

<p align="justify">Setelah tipe dan resolver siap, semuanya dirangkai menjadi satu skema dengan strawberry.Schema(query=Query). Skema inilah yang menjadi pintu masuk server GraphQL, karena di dalamnya terdaftar semua query yang bisa diminta client, dan tanpa baris ini server tidak punya gambaran apa pun tentang data yang bisa dilayani.</p>

---

Kemudian jalankan dengan perintah

```powershell
strawberry dev schema
```

<img src="images/26_Jalankan_Skema.png" width="700">

Output yang dihasilkan adalah `Running strawberry on http://0.0.0.0:8000/graphql`

catatan: 0.0.0.0 bisa diganti dengan localhost atau 127.0.0.1

contoh:

```text
http://localhost:8000/graphql atau http://127.0.0.1:8000/graphql
```

#### Pembahasan

<p align="justify">Server dijalankan dengan perintah strawberry dev schema, dan begitu muncul tulisan Running strawberry on http://0.0.0.0:8000/graphql, artinya server sudah aktif dan siap menerima permintaan di port 8000. Alamat 0.0.0.0 bisa diganti dengan localhost atau 127.0.0.1, yang ketiganya merujuk ke komputer yang sama, hanya penulisannya saja yang berbeda.</p>

---

Ketika link tersebut dibuka akan tampil

<img src="images/27_Tampilan_GraphQL.png" width="700">

#### Pembahasan

<p align="justify">Saat link tersebut dibuka di browser, muncul UI bawaan strawberry yang tampilannya seperti editor, dengan bagian kiri untuk menulis query dan bagian kanan untuk menampilkan hasilnya. UI ini praktis untuk mencoba-coba query langsung tanpa harus membuat client terlebih dahulu.</p>

---

Tombol run berikut digunakan untuk menjalankan query

<img src="images/28_Tombol_Run.png" width="700">

#### Pembahasan

<p align="justify">Setelah query ditulis di sisi kiri, tombol run di bagian atas dipakai untuk mengirimkannya ke server. Begitu tombol ditekan, server menjalankan query dan hasilnya langsung muncul di sisi kanan, dan dari situ kita bisa tahu apakah query yang ditulis sudah benar atau belum.</p>

---

5. Pada tempat yang tersedia (di sisi kiri), tuliskan query berikut:

```graphql
{
  books {
    title
    author
  }
}
```

<img src="images/29_Query_GraphQL.png" width="700">

Ketika dijalankan dengan mengklik tombol run. Output yang keluar:

<img src="images/30_Output_Run.png" width="700">

Untuk mematikan server dapat dilakukan dengan cara menekan <CTRL+C> pada shell untuk menjalankan strawberry.

#### Pembahasan

<p align="justify">Query yang diminta cukup sederhana, yaitu meminta field books beserta title dan author-nya, dan setelah tombol run diklik, hasilnya muncul di sisi kanan berupa data buku The Great Gatsby karya F. Scott Fitzgerald, persis seperti yang dikembalikan fungsi get_books. Ini membuktikan bahwa alurnya sudah jalan: client mengirim query, server menjalankan resolver, dan hasilnya dikembalikan ke client. Untuk menghentikan server, cukup menekan Ctrl+C di tempat perintah strawberry dijalankan.</p>

---

# ⏩ PEMBAHASAN TUGAS

1. Buat file bernama client.py

<img src="images/31_Tugas_Class_client.py.png" width="700">

#### Pembahasan

<p align="justify">Tugas berikutnya adalah membuat client, dan file yang dibuat diberi nama client.py. Client ini nantinya berperan sebagai pihak yang meminta data ke server GraphQL yang tadi sudah dibuat, jadi posisinya berbeda dengan server, dan justru dari perbedaan inilah terlihat bagaimana komunikasi antar proses bekerja.</p>

---

2. Isi file dengan kode berikut

```python
import requests

url = "http://localhost:8000/graphql"

query = """
{
  books {
    title
    author
  }
}
"""

try:
  response = requests.post(url, json={"query": query})

  if response.status_code == 200:
    data = response.json()
    books = data.get("data", {}).get("books", [])

    print("=== DATA DARI GRAPHQL SERVER ===")
    for book in books:
      print(f"- Judul : {book.get('title')}")
      print(f"- Penulis: {book.get('author')}")
    print("--------------------------------")
  else:
    print(f"Gagal terhubung. Status code: {response.status_code}")

except Exception as e:
  print(f"Terjadi kesalahan: {e}")
```

<img src="images/32_Tugas_Isi_Kode_client.py.png" width="700">

#### Pembahasan

<p align="justify">Di dalam client.py, digunakan library requests untuk mengirim permintaan HTTP POST ke alamat server http://localhost:8000/graphql dengan membawa query yang ingin dijalankan. Kalau server merespons dengan status code 200, artinya permintaan berhasil diterima, dan data buku di dalam response JSON kemudian diambil lewat path data.books lalu ditampilkan satu per satu ke layar, sedangkan kalau gagal terhubung atau terjadi error, pesannya juga ditampilkan supaya kita tahu apa yang salah.</p>

---

3. Jalankan client.py

Gunakan perintah berikut untuk menjalankan client.py

```powershell
python client.py
```

<img src="images/33_Output_Tugas_client.py.png" width="700">

#### Pembahasan

<p align="justify">Setelah server GraphQL masih berjalan, client.py dijalankan dengan python client.py, dan di layar muncul daftar buku yang berhasil diambil dari server, lengkap dengan judul dan penulisnya. Output ini membuktikan bahwa dua proses yang berbeda, yaitu client dan server, berhasil berkomunikasi dan bertukar data.</p>

---

# 📝 Kesimpulan

1. Pada satu node, proses dikelola sepenuhnya oleh sistem operasi secara transparan, dan proses dapat dilihat, dimatikan dengan taskkill, serta di-restart dengan perintah start melalui CMD.
2. Pada sistem terdistribusi, komunikasi antar proses antar node memerlukan mekanisme khusus karena perbedaan clock dan tidak adanya shared memory, dan salah satu cara yang bisa digunakan adalah GraphQL.
3. Server GraphQL berhasil dibuat dengan Python menggunakan paket Strawberry dan dapat diakses melalui playground pada http://localhost:8000/graphql.
4. Client yang dibuat dalam client.py berhasil berkomunikasi dengan server GraphQL dan menampilkan data buku yang diminta melalui query.

---

## 🗒️ Referensi

- https://strawberry.rocks/docs
- https://docs.astral.sh/uv/getting-started/installation/
- https://github.com/NEO-X-School/notes/blob/main/uv/00.md
