# Praktikum Minggu 02 - Komunikasi Antar Proses pada Sistem Terdistribusi

**Mata Kuliah:** Praktikum Sistem Terdistribusi dan Terdesentralisasi
**Topik:** Komunikasi Antar Proses pada Sistem Terdistribusi

---

# 📚 Tujuan Praktikum

1. ...
2. ....
3. .....

---

# 📚 Dasar Teori

---

# ⏩ PEMBAHASAN PRAKTIKUM

## PRAKTIK 1 - PROSES PADA SATU NODE

### 1. Tampilkan berbagai proses yang ada pada Laptop-Windows

<img src="images/01_Tampilan_Proses.png" width="700">

#### Pembahasan

---

### 2. Jalankan salah satu aplikasi kemudian perlihatkan proses yang dimunculkan oleh aplikasi

Sebagai contoh menjalankan Notepad untuk percobaan:

<img src="images/02_Jalankan_Notepad.png" width="700">

Kemudian untuk melihat proses yang dimunculkan aplikasi tersebut dapat dilihat pada task manager, yaitu sebagai berikut :

<img src="images/04_Proses_Notepad.png" width="700">

<img src="images/03_Detail_Proses.png" width="700">

#### Pembahasan

---

### 3. Merestart dan Mematikan proses yang dimunculkan oleh aplikasi

1. Untuk mematikan proses dapat dilakukan melalui Task Manager:

<img src="images/05_Mematikan_Proses_Via_TaskManager.png" width="700">

#### Pembahasan

---

Kemudian dapat dilakukan juga melalu CMD:

Untuk melihat daftar proses yang sedang berjalan di Windows gunakan perintah:

```
tasklist
```

#### Pembahasan

---

Untuk mencari proses dari aplikasi gunakan perintah:

```
tasklist | findstr /i "Nama_Aplikasi"
```

Contoh :

```
tasklist | findstr /i notepad
```

<img src="images/06_Mematikan_Proses_Via_CMD.png" width="700">

#### Pembahasan

---

Untuk mematikan proses dapat menggunakan perintah

```
taskkill /IM nama_proses.exe /F
```

Contoh :

```
taskkill /IM notepad.exe /F
```

<img src="images/07_Mematikan_Proses_Via_CMD.png" width="700">

#### Pembahasan

---

Untuk memastikan proses berhenti. Gunakan Perintah:

```
tasklist | findstr /i "Nama_Aplikasi"
```

Contoh :

<img src="images/08_Memastikan_Proses_Berhenti.png" width="700">

#### Pembahasan

---

2. Merestart Proses

Untuk merestart proses dapat dilakukan dengan perintah

```
start "" notepad
```

<img src="images/09_Merestart_Proses.png" width="700">

<img src="images/10_Merestart_Proses.png" width="700">

#### Pembahasan

---

## PRAKTIK 2 - KOMUNIKASI ANTAR PROSES pada SISTEM TERDISTRIBUSI

### 1. Instalasi

Petunjuk lengkap instalasi ada di https://docs.astral.sh/uv/getting-started/installation/. Sesuaikan dengan sistem operasi yang digunakan. Berikut adalah contoh di Windows:

```
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

---

Setelah mengatur env variabel untuk uv ($PATH harus berisi - salah satunya - tempat uv di install) yaitu di (C:\Users\LENOVO\.local\bin), uv bisa dijalankan sebagai berikut:

```
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
          Display the uv version

Use `uv help` for more details.
```

#### Pembahasan

---

### 2. Update

Update diperlukan jika menginginkan tetap menggunakan versi terbaru dari uv.

Gunakan Perintah:

```
uv self update
```

Contoh:

```
PS C:\WINDOWS\system32> uv self update
info: Checking for updates...
success: You're already on version v0.13.0 of uv (the latest version).
```

#### Pembahasan

---

### 3. Membuat Workspace

Buat Direktori terlebih dahulu

<img src="images/11_Membuat_Workspace-01.png" width="700">

#### Pembahasan

---

Kemudian masuk kedalam direktori

<img src="images/12_Masuk_Direktori.png" width="700">

#### Pembahasan

---

Lalu cek versi python yang ingin digunakan. Jika versi Python yang diinginkan belum ada, akan dilakukan download dan instalasi lebih dulu. Untuk cek versi python dapat dilakukan dengan cara:

<img src="images/13_Cek_Python_List.png" width="700">

#### Pembahasan

---

Pada direktori tersebut, akan dibuat file .python-version:

<img src="images/14_Membuat_Python-Version.png" width="700">

#### Pembahasan

---

### 4. Buat Environment

<img src="images/15_Membuat_Environment.png" width="700">

#### Pembahasan

---

Kemudian Mengaktifkan dengan perintah

```
.\.venv\Scripts\Activate
```

<img src="images/16_Mengaktifkan_Environment.png" width="700">

#### Pembahasan

---

Lalu jika ingin keluar dari env. Gunakan perintah:

```
deactivate
```

<img src="images/17_Deactivate.png" width="700">

#### Pembahasan

---

### 5. Mengelola Paket

Paket pertama yaitu pandas, untuk menginstall nya dapat menggunakan perintah

```
uv pip install pandas
```

<img src="images/18_Pandas_Packages.png" width="700">

#### Pembahasan

---

Paket kedua yaitu untuk GraphQL, menggunakan perintah

```
uv pip install "strawberry-graphql[cli]"
```

<img src="images/19_GraphQL_Packages.png" width="700">

#### Pembahasan

---

Lalu untuk melihat paket yang terpasang menggunakan perintah

```
uv pip list
```

<img src="images/20_Cek_paket_Terpasang.png" width="700">

#### Pembahasan

---

Untuk menyimpan daftar paket ke requirements.txt gunakan perintah

```
uv pip freeze > requirements.txt
```

#### Pembahasan

---

Kemudian untuk melihat isi file nya dapat menggunakan perintah

```
cat requirements.txt
```

<img src="images/21_Menyimpan_Daftar_Paket.png" width="700">

#### Pembahasan

---

### 5. Menjalankan source code yang sudah disediakan pada https://strawberry.rocks/docs

1. Mendefinisikan skema

Buat file bernama schema.py dengan isi sebagai berikut

```
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

---

2. Definisikan kumpulan data

Contoh fungsi yang mengembalikan beberapa buku

```
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

---

3. Mendefinisikan Resolver

Perbarui query pada program schema.py

```
@strawberry.type
class Query:
    books: typing.List[Book] = strawberry.field(resolver=get_books)
```

<img src="images/24_Mendefinisikan_Resolver.png" width="700">

#### Pembahasan

---

4. Buat skema dan jalankan

Untuk membuat skema, tambahkan kode berikut:

```
schema = strawberry.Schema(query=Query)
```

<img src="images/25_Membuat_Skema.png" width="700">

#### Pembahasan

---

Kemudian jalankan dengan perintah

```
strawberry dev schema
```

<img src="images/26_Jalankan_Skema.png" width="700">

Output yang dihasilkan adalah `Running strawberry on http://0.0.0.0:8000/graphql`

catatan: 0.0.0.0 bisa diganti dengan localhost atau 127.0.0.1

contoh:

```
http://localhost:8000/graphql atau http://127.0.0.1:8000/graphql
```

#### Pembahasan

---

Ketika link tersebut dibuka akan tampil

<img src="images/27_Tampilan_GraphQL.png" width="700">

#### Pembahasan

---

Tombol run berikut digunakan untuk menjalankan query

<img src="images/28_Tombol_Run.png" width="700">

#### Pembahasan

---

5. Pada tempat yang tersedia (di sisi kiri), tuliskan query berikut:

```
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

---

# ⏩ PEMBAHASAN TUGAS

1. Buat file bernama client.py

<img src="images/31_Tugas_Class_client.py.png" width="700">

#### Pembahasan

---

2. Isi file dengan kode berikut

```
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

---

3. Jalankan client.py

Gunakan perintah berikut untuk menjalankan client.py

```
python client.py
```

<img src="images/33_Output_Tugas_client.py.png" width="700">

#### Pembahasan

---

# 📝 Kesimpulan

---

## 🗒️ Referensi
