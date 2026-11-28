# Praktikum Minggu 09 - Arsitektur Microservices untuk Sistem Terdistribusi: GraphQL dan gRPC

<p align="justify"><strong>Mata Kuliah:</strong> Praktikum Sistem Terdistribusi dan Terdesentralisasi</p>

<p align="justify"><strong>Topik:</strong> Arsitektur Microservices untuk Sistem Terdistribusi: GraphQL dan gRPC</p>

---

## 🎯 Tujuan Praktikum

<ol>
  <li><p align="justify">Memahami posisi GraphQL dan gRPC sebagai alternatif REST ketika aplikasi dipecah menjadi layanan-layanan kecil.</p></li>
  <li><p align="justify">Memahami cara kerja GraphQL, mulai dari <em>schema</em>, <em>query</em>, hingga <em>resolver</em> yang mengambil data.</p></li>
  <li><p align="justify">Mampu membangun GraphQL server dengan Strawberry dan SQLModel, lalu mengujinya lewat GraphQL Explorer maupun client <code>gql</code>.</p></li>
  <li><p align="justify">Memahami peran Protocol Buffers dan proses kompilasi <code>.proto</code> menjadi <em>stub</em> yang dipakai server dan client.</p></li>
  <li><p align="justify">Mampu membangun gRPC server dan client untuk mengambil data berdasarkan id, termasuk menangani kasus data tidak ditemukan.</p></li>
  <li><p align="justify">Mampu menerapkan kedua pendekatan pada tabel SQLite buatan sendiri dan menilai kapan masing-masing lebih tepat dipakai.</p></li>
</ol>

---

## 📚 Dasar Teori

### Dari Monolit ke Microservices

<p align="justify">Aplikasi monolit menumpuk semua fitur dalam satu proses, sehingga satu bagian yang bermasalah bisa menyeret bagian lain. Arsitektur <em>microservices</em> memecahnya menjadi layanan kecil yang berjalan sendiri dan saling bicara lewat jaringan. Konsekuensinya, bentuk komunikasi antarlayanan harus disepakati lebih dulu. REST adalah pilihan paling umum karena memakai HTTP apa adanya, tetapi ia tidak selalu cocok: kadang client hanya butuh sebagian data, kadang justru butuh komunikasi yang lebih hemat. Di titik itulah GraphQL dan gRPC masuk sebagai alternatif, dan praktikum ini membangun keduanya di atas data yang sama agar perbedaannya terasa.</p>

### GraphQL

<p align="justify">GraphQL membalik cara berpikir tentang API. Kalau REST menyediakan banyak alamat dengan bentuk jawaban yang sudah ditentukan, GraphQL hanya punya satu alamat dan satu <em>schema</em>. Client mengirim <em>query</em> yang menyebut <em>field</em> apa saja dibutuhkan, lalu server mengembalikan persis itu. Bagian server yang tahu cara mengambil data disebut <em>resolver</em>; ia bisa membaca database, memanggil layanan lain, atau menghitung nilai. Karena <em>schema</em> bersifat terbaca mesin, alat seperti GraphQL Explorer bisa menampilkan daftar tipe dan <em>field</em> secara otomatis. GraphQL tidak menggantikan database; ia hanya mengatur bagaimana data itu diminta dan dikirim.</p>

### Strawberry dan SQLModel

<p align="justify">Strawberry adalah pustaka Python yang menyusun <em>schema</em> GraphQL dari <em>class</em> biasa. Dekorator <code>@strawberry.type</code> membuat <em>class</em> dikenali sebagai tipe GraphQL, sedangkan <code>strawberry.field(resolver=...)</code> menghubungkan sebuah <em>field</em> ke fungsi pengambil data. SQLModel melengkapinya dengan menggabungkan Pydantic untuk validasi dan SQLAlchemy untuk akses database. Karena keduanya berbasis anotasi tipe, satu <em>class</em> bisa berlaku sebagai model tabel sekaligus bentuk respons GraphQL. Dengan begitu tidak perlu menulis dua definisi yang isinya hampir sama.</p>

### gRPC dan Protocol Buffers

<p align="justify">gRPC memakai model <em>remote procedure call</em>: client memanggil fungsi di server seolah-olah fungsi itu lokal. Kontraknya ditulis dalam file <code>.proto</code> memakai Protocol Buffers, lalu dikompilasi menjadi <em>stub</em> untuk berbagai bahasa. Pesan dikirim dalam format biner di atas HTTP/2, sehingga lebih ringkas daripada JSON, tetapi tidak bisa dibaca langsung dengan mata. Konsekuensinya, perubahan kontrak harus diikuti kompilasi ulang di kedua sisi. Selama file <code>.proto</code> sama, client dan server tidak perlu tahu bahasa implementasi masing-masing.</p>

### Pola Komunikasi di Praktikum

<p align="justify">Semua layanan di praktikum ini berjalan di mesin yang sama, tetapi tetap berkomunikasi lewat jaringan. Server GraphQL mendengarkan port 8000 dan diakses lewat HTTP, sedangkan server gRPC mendengarkan port 50051 lewat <em>channel</em>. Urutannya penting: server harus hidup sebelum client dijalankan, dan kedua proses sebaiknya dibiarkan terbuka sampai pengujian selesai. Karena setiap folder punya <em>virtual environment</em> sendiri, perpindahan dari GraphQL ke gRPC juga menuntut venv baru. Pola ini sengaja dibuat berulang agar terlihat bahwa isolasi lingkungan adalah bagian dari arsitektur, bukan sekadar formalitas.</p>

---

## ⏩ Pembahasan Praktikum

### 0. Persyaratan

<p align="justify">Buat struktur direktori dengan perintah:</p>

```bash
mkdir -p src/graphql/server src/graphql/client src/grpc/server src/grpc/client
```

<p align="center">
  <img src="images/01_Struktur Direktori.png" width="700" alt="Struktur direktori GraphQL dan gRPC yang dibuat dalam satu perintah.">
  <br>
  <em>Gambar 1. Struktur direktori GraphQL dan gRPC yang dibuat dalam satu perintah.</em>
</p>

#### Pembahasan

<p align="justify">Struktur folder dipisah per protokol dan per peran, server maupun client, supaya tiap bagian punya dependensi sendiri. Kalau semuanya digabung, paket Strawberry dan gRPC akan bercampur dalam satu <em>environment</em> dan sulit diketahui mana yang benar-benar dipakai. Pemisahan ini juga membuat kesalahan konfigurasi lebih mudah dilacak: ketika client gagal, yang diperiksa cukup venv client.</p>

---

### 1. GraphQL

#### 1.1. GraphQL Server

<p align="justify">Buat file kosong yang dibutuhkan dengan perintah:</p>

```bash
touch src/graphql/server/{graphql-server.py,requirements.txt}
```

#### Pembahasan

<p align="justify">Dua berkas kosong dibuat lebih dulu: <code>graphql-server.py</code> untuk kode dan <code>requirements.txt</code> untuk daftar paket. Membuatnya di awal terasa sepele, tetapi memberi dua titik yang jelas: apa yang akan ditulis dan apa yang harus dipasang. Urutan ini juga memaksa dependensi ditentukan sebelum kode dijalankan.</p>

---

<p align="justify">Kemudian salin database dari pertemuan 8 ke folder GraphQL server dengan perintah:</p>

```bash
cp ../prak-dis-dec/08/src/departemen-sdm.db src/graphql/server/
```

#### Pembahasan

<p align="justify">Database <code>departemen-sdm.db</code> dari pertemuan 8 disalin ke folder server. Server hanya membaca berkas di direktorinya sendiri, jadi menaruhnya di tempat lain akan membuat <code>sqlite:///departemen-sdm.db</code> menunjuk ke file kosong. Menyalin juga menjaga data asli tetap utuh bila percobaan diulang.</p>

---

<p align="justify">Lalu setup GraphQL server, dengan masuk ke folder graphql server terlebih dahulu dengan perintah:</p>

```bash
cd ~/Desktop/Praktik09/src/graphql/server
```

#### Pembahasan

<p align="justify">Pindah ke folder server memastikan seluruh perintah berikutnya berjalan pada konteks yang benar. <code>uv venv</code> dan <code>uv pip install</code> membaca <code>requirements.txt</code> dari direktori aktif, bukan dari lokasi perintah diketik. Tanpa <code>cd</code>, venv bisa dibuat di folder yang salah.</p>

---

<p align="justify">Buat file requirements.txt untuk mendaftarkan library yang dibutuhkan (strawberry-graphql[cli] dan sqlmodel) dengan perintah:</p>

```bash
printf "strawberry-graphql[cli]\nsqlmodel\n" > requirements.txt
```

#### Pembahasan

<p align="justify">Isi <code>requirements.txt</code> hanya dua baris: <code>strawberry-graphql[cli]</code> dan <code>sqlmodel</code>. Ekstra <code>[cli]</code> penting karena perintah <code>strawberry dev</code> berasal dari paket tambahan itu, bukan dari pustaka intinya. SQLModel dipakai agar tabel SQLite bisa dibaca lewat <em>class</em> Python tanpa menulis SQL.</p>

---

<p align="justify">Atur versi Python proyek menggunakan uv ke versi 3.14.5:</p>

```bash
uv python pin 3.14.5 --managed-python
```

<p align="center">
  <img src="images/02_Atur Versi Python.png" width="700" alt="Python 3.14.5 dipin melalui uv pada folder GraphQL server.">
  <br>
  <em>Gambar 2. Python 3.14.5 dipin melalui uv pada folder GraphQL server.</em>
</p>

#### Pembahasan

<p align="justify">Pin 3.14.5 menulis satu baris ke <code>.python-version</code>. Efeknya baru terasa saat <code>uv venv</code> dijalankan: uv membaca berkas itu dan memakai interpreter yang sama. Kalau tidak dipin, versi yang dipakai bisa berbeda antar folder dan hasil praktikum sulit dibandingkan.</p>

---

<p align="justify">Buat virtual environment baru di dalam direktori tersebut:</p>

```bash
uv venv
```

<p align="center">
  <img src="images/03_Buat virtual environment.png" width="700" alt="Virtual environment dibuat di dalam folder GraphQL server.">
  <br>
  <em>Gambar 3. Virtual environment dibuat di dalam folder GraphQL server.</em>
</p>

#### Pembahasan

<p align="justify"><code>uv venv</code> membuat folder <code>.venv</code> berisi interpreter dan paket yang terisolasi. Isolasi inilah yang mencegah paket server GraphQL bertabrakan dengan paket gRPC nanti. Folder <code>.venv</code> tidak perlu di-commit karena bisa dibuat ulang dari <code>requirements.txt</code>.</p>

---

<p align="justify">Aktifkan virtual environment yang sudah dibuat dengan perintah:</p>

```bash
source .venv/Scripts/activate
```

<p align="justify">Lalu install seluruh dependensi yang terdaftar pada file requirements.txt:</p>

```bash
uv pip install -r requirements.txt
```

<p align="center">
  <img src="images/04_Aktifkan Environment dan Install Depensi.png" width="700" alt="Virtual environment aktif dan seluruh dependensi server terpasang.">
  <br>
  <em>Gambar 4. Virtual environment aktif dan seluruh dependensi server terpasang.</em>
</p>

#### Pembahasan

<p align="justify">Venv diaktifkan lalu dependensi dipasang. Tanda <code>(server)</code> pada prompt menandakan perintah <code>python</code> dan <code>pip</code> sekarang mengarah ke dalam <code>.venv</code>, bukan ke Python sistem. <code>uv pip install -r requirements.txt</code> membaca daftar tadi, sehingga pemasangan bisa diulang kapan saja.</p>

---

<p align="justify">Kemudian buat dan isi file graphql-server.py dengan source code:</p>

```python
import typing
import strawberry
from sqlmodel import Field, Session, SQLModel, create_engine, select

@strawberry.type
class Sdm(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    npp: str
    nama: str

engine = create_engine("sqlite:///departemen-sdm.db")

def get_sdms():
    with Session(engine) as session:
        statement = select(Sdm)
        results = session.exec(statement).all()
        return results

@strawberry.type
class Query:
    sdms: typing.List[Sdm] = strawberry.field(resolver=get_sdms)

schema = strawberry.Schema(query=Query)
```

<p align="center">
  <img src="images/05_Souce Code graphql-server.png" width="700" alt="Isi berkas graphql-server.py untuk tabel sdm.">
  <br>
  <em>Gambar 5. Isi berkas graphql-server.py untuk tabel sdm.</em>
</p>

#### Pembahasan

<p align="justify">Kode server mendefinisikan tiga hal sekaligus: model <code>Sdm</code>, resolver <code>get_sdms</code>, dan <code>Query</code>. Dekorator <code>@strawberry.type</code> membuat <em>class</em> biasa dikenali sebagai tipe GraphQL, sementara <code>strawberry.field(resolver=...)</code> menghubungkan <em>field</em> <code>sdms</code> ke fungsi pengambil data. Karena <code>Sdm</code> juga <code>SQLModel</code>, satu <em>class</em> itu berlaku sebagai model tabel sekaligus bentuk respons.</p>

---

<p align="justify">Menjalankan server Strawberry GraphQL untuk menguji skema yang telah dibuat dengan perintah:</p>

```bash
strawberry dev graphql-server
```

<p align="center">
  <img src="images/06_Menjalankan server Strawberry GraphQL.png" width="700" alt="Server Strawberry berjalan di http://0.0.0.0:8000/graphql.">
  <br>
  <em>Gambar 6. Server Strawberry berjalan di http://0.0.0.0:8000/graphql.</em>
</p>

#### Pembahasan

<p align="justify"><code>strawberry dev graphql-server</code> menjalankan server pengembangan dan menampilkan alamat <code>http://0.0.0.0:8000/graphql</code>. Mode dev berguna karena kode dimuat ulang saat berubah, sehingga server tidak perlu dimatikan setiap kali mengedit. Pesan <em>Running strawberry on ...</em> adalah tanda server siap menerima <em>query</em>.</p>

---

<p align="justify">Selanjutnya buka http://localhost:8000/graphql pada browser</p>

<p align="center">
  <img src="images/07_Open GraphQL pada Browser.png" width="700" alt="GraphQL Explorer dibuka melalui peramban.">
  <br>
  <em>Gambar 7. GraphQL Explorer dibuka melalui peramban.</em>
</p>

<p align="justify">Lalu ketikan query berikut pada kotak kiri:</p>

```GraphQL
{
  sdms {
    id
    npp
    nama
  }
}
```

<p align="center">
  <img src="images/08_Hasil Query GraphQL.png" width="700" alt="Hasil query sdms menampilkan tiga data karyawan.">
  <br>
  <em>Gambar 8. Hasil query sdms menampilkan tiga data karyawan.</em>
</p>

#### Pembahasan

<p align="justify">Di Explorer, <em>query</em> <code>{ sdms { id npp nama } }</code> mengembalikan tiga baris data. Yang diminta hanya tiga <em>field</em>, dan itulah yang dikirim balik tanpa kolom lain. Hasil ini membuktikan resolver <code>get_sdms</code> benar-benar membaca database, bukan mengembalikan data contoh.</p>

---

#### 1.2. GraphQL Client

<p align="justify">Buat file kosong yang dibutuhkan dengan perintah:</p>

```bash
touch src/graphql/client/{graphql-client.py,requirements.txt}
```

#### Pembahasan

<p align="justify">Berkas client disiapkan di folder terpisah dari server. Pemisahan ini mencerminkan peran yang berbeda: server menyediakan data, client mengonsumsinya lewat jaringan. Dengan folder sendiri, client bisa dijalankan di mesin lain tanpa membawa kode server.</p>

---

<p align="justify">Selanjutnya, setup GraphQL client dengan masuk ke folder client terlebih dahulu menggunakan perintah:</p>

```bash
cd ~/Desktop/Praktik09/src/graphql/client
```

#### Pembahasan

<p align="justify">Masuk ke folder client sebelum membuat venv. Alasannya sama seperti di server: <code>uv</code> bekerja relatif terhadap direktori aktif. Kalau langkah ini terlewat, venv client bisa tertukar dengan venv server yang masih aktif.</p>

---

<p align="justify">Buat file requirements.txt untuk mendaftarkan library yang dibutuhkan (gql[aiohttp]) dengan perintah:</p>

```bash
echo "gql[aiohttp]" > requirements.txt
```

#### Pembahasan

<p align="justify">Client hanya butuh <code>gql[aiohttp]</code>. Ekstra <code>aiohttp</code> menyediakan transport HTTP asinkron yang dipakai <code>AIOHTTPTransport</code>. Tanpa ekstra itu, <code>gql</code> tetap ada tetapi tidak bisa mengirim <em>request</em> lewat aiohttp.</p>

---

<p align="justify">Atur versi Python proyek menggunakan uv ke versi 3.14.5 dengan perintah:</p>

```bash
uv python pin 3.14.5 --managed-python
```

<p align="center">
  <img src="images/09_Atur versi Python.png" width="700" alt="Pin Python 3.14.5 untuk folder GraphQL client.">
  <br>
  <em>Gambar 9. Pin Python 3.14.5 untuk folder GraphQL client.</em>
</p>

#### Pembahasan

<p align="justify">Versi Python client dipin ke 3.14.5 agar cocok dengan server. Kesamaan versi mengurangi kemungkinan perbedaan perilaku, terutama pada fitur bahasa seperti anotasi tipe <code>int | None</code>.</p>

---

<p align="justify">Buat virtual environment baru di dalam direktori client dengan perintah:</p>

```bash
uv venv
```

<p align="center">
  <img src="images/10_Buat virtual environment baru di dalam direktori client.png" width="700" alt="Virtual environment client dibuat terpisah dari server.">
  <br>
  <em>Gambar 10. Virtual environment client dibuat terpisah dari server.</em>
</p>

#### Pembahasan

<p align="justify">Venv client dibuat terpisah dari venv server, meski keduanya memakai Python yang sama. Pemisahan ini menjaga dependensi tetap minimal: client tidak perlu memasang Strawberry atau SQLModel karena tidak menyentuh database.</p>

---

<p align="justify">Aktifkan virtual environment yang sudah dibuat:</p>

```bash
source .venv/Scripts/activate
```

<p align="justify">Lalu install seluruh dependensi yang terdaftar pada file requirements.txt dengan perintah:</p>

```bash
uv pip install -r requirements.txt
```

<p align="center">
  <img src="images/11_Aktifkan virtual environment dan install seluruh dependensi.png" width="700" alt="Dependensi client gql[aiohttp] terpasang.">
  <br>
  <em>Gambar 11. Dependensi client gql[aiohttp] terpasang.</em>
</p>

#### Pembahasan

<p align="justify">Setelah venv aktif, <code>gql</code> dan <code>aiohttp</code> dipasang dari <code>requirements.txt</code>. Prompt berubah menjadi <code>(client)</code>, tanda bahwa lingkungan sudah berpindah. Mulai titik ini, <code>python graphql-client.py</code> akan memakai paket yang baru dipasang.</p>

---

<p align="justify">Kemudian buat dan isi file graphql-client.py dengan source code:</p>

```python
import asyncio
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

async def main():
    transport = AIOHTTPTransport(url="http://localhost:8000/graphql")
    client = Client(transport=transport)

    query = gql(
        """
        query getSdms {
            sdms {
                id
                npp
                nama
            }
        }
        """
    )

    async with client as session:
        result = await session.execute(query)
        print(result)

asyncio.run(main())
```

<p align="center">
  <img src="images/12_Source Code graphql-client.png" width="700" alt="Isi berkas graphql-client.py.">
  <br>
  <em>Gambar 12. Isi berkas graphql-client.py.</em>
</p>

#### Pembahasan

<p align="justify">Skrip client menyusun <em>query</em> yang sama seperti di Explorer, tetapi dikirim lewat kode. <code>AIOHTTPTransport</code> menunjuk ke <code>http://localhost:8000/graphql</code>, lalu <code>async with client as session</code> membuka koneksi dan mengeksekusi <em>query</em>. Karena semuanya asinkron, <code>asyncio.run(main())</code> diperlukan untuk memulai <em>event loop</em>.</p>

---

<p align="justify">Terakhir, pastikan server GraphQL (graphql-server) sudah berjalan, lalu jalankan skrip client untuk mengambil dan menampilkan data dari server dengan perintah:</p>

```bash
python graphql-client.py
```

<p align="center">
  <img src="images/13_Menjalankan graphql-client.png" width="700" alt="Client mencetak tiga data SDM yang diambil dari server.">
  <br>
  <em>Gambar 13. Client mencetak tiga data SDM yang diambil dari server.</em>
</p>

#### Pembahasan

<p align="justify">Output client berupa <em>dictionary</em> berisi tiga data SDM. Bentuknya lebih ringkas daripada JSON mentah karena <code>gql</code> mengubah respons menjadi struktur Python. Hasil ini menegaskan bahwa client dan server berbicara dengan <em>schema</em> yang sama.</p>

---

<p align="justify">Setelah output data karyawan muncul, hentikan server dan client dengan menekan Ctrl + C untuk server, lalu ketik deactivate di server dan client.</p>

<p align="center">
  <img src="images/14_Menghentikan GraphQL Server.png" width="700" alt="Server GraphQL dihentikan dengan Ctrl+C.">
  <br>
  <em>Gambar 14. Server GraphQL dihentikan dengan Ctrl+C.</em>
</p>

<p align="center">
  <img src="images/15_Menghentikan GraphQL Client.png" width="700" alt="Virtual environment client dinonaktifkan.">
  <br>
  <em>Gambar 15. Virtual environment client dinonaktifkan.</em>
</p>

#### Pembahasan

<p align="justify">Server dihentikan dengan Ctrl+C, lalu venv dinonaktifkan. Langkah ini terlihat administratif, tetapi mencegah venv server masih aktif saat berpindah ke folder gRPC. Kebiasaan menutup lingkungan dengan rapi menghindari kebingungan saat instalasi paket berikutnya.</p>

---

### 2. gRPC

<p align="justify">Selanjutnya, setup gRPC server dengan masuk ke folder gRPC server terlebih dahulu menggunakan perintah:</p>

```bash
cd ~/Desktop/Praktik09/src/grpc/server
```

#### Pembahasan

<p align="justify">Folder gRPC server disiapkan sebagai lingkungan baru. gRPC memakai paket yang berbeda dari GraphQL, jadi venv-nya juga harus berbeda. Dari sini alurnya berubah: bukan lagi <em>query</em>, melainkan kontrak <code>.proto</code> yang harus disepakati lebih dulu.</p>

---

<p align="justify">Buat file requirements.txt untuk mendaftarkan library yang dibutuhkan (grpcio, grpcio-tools, dan sqlmodel) dengan perintah:</p>

```bash
printf "grpcio\ngrpcio-tools\nsqlmodel\n" > requirements.txt
```

#### Pembahasan

<p align="justify">Tiga paket didaftarkan: <code>grpcio</code>, <code>grpcio-tools</code>, dan <code>sqlmodel</code>. <code>grpcio</code> adalah runtime-nya, sedangkan <code>grpcio-tools</code> menyediakan <code>protoc</code> untuk mengompilasi <code>.proto</code>. SQLModel tetap dipakai karena server perlu membaca SQLite.</p>

---

<p align="justify">Atur versi Python proyek menggunakan uv ke versi 3.14.5 dengan perintah:</p>

```bash
uv python pin 3.14.5 --managed-python
```

<p align="center">
  <img src="images/16_Atur versi Python.png" width="700" alt="Pin Python 3.14.5 untuk folder gRPC server.">
  <br>
  <em>Gambar 16. Pin Python 3.14.5 untuk folder gRPC server.</em>
</p>

#### Pembahasan

<p align="justify">Versi Python dipin lagi di folder ini. Pengulangan ini memang disengaja: setiap folder adalah proyek kecil yang berdiri sendiri, sehingga konfigurasinya tidak diwarisi dari folder lain.</p>

---

<p align="justify">Buat virtual environment baru di dalam direktori tersebut:</p>

```bash
uv venv
```

<p align="center">
  <img src="images/17_Buat virtual environment.png" width="700" alt="Virtual environment gRPC server dibuat.">
  <br>
  <em>Gambar 17. Virtual environment gRPC server dibuat.</em>
</p>

#### Pembahasan

<p align="justify">Venv gRPC server dibuat dan diisolasi dari venv GraphQL. Isolasi ini penting karena <code>grpcio</code> membawa komponen biner yang bisa bentrok dengan versi lain bila dicampur.</p>

---

<p align="justify">Aktifkan virtual environment yang sudah dibuat:</p>

```bash
source .venv/Scripts/activate
```

<p align="justify">Kemudian menginstall depensi yang terdaftar pada file requirements.txt:</p>

```bash
uv pip install -r requirements.txt
```

<p align="center">
  <img src="images/18_Aktifkan virtual environment dan Install depensi.png" width="700" alt="Dependensi grpcio, grpcio-tools, dan sqlmodel terpasang.">
  <br>
  <em>Gambar 18. Dependensi grpcio, grpcio-tools, dan sqlmodel terpasang.</em>
</p>

#### Pembahasan

<p align="justify">Ketiga paket dipasang ke dalam venv. Setelah proses selesai, perintah <code>python -m grpc_tools.protoc</code> bisa dipakai. Tanpa <code>grpcio-tools</code>, perintah itu akan gagal meski <code>grpcio</code> sudah ada.</p>

---

<p align="justify">Buat file service.proto untuk mendefinisikan struktur pesan (SdmRequest dan SdmResponse) serta layanan RPC (SdmService) dengan perintah:</p>

```bash
cat << 'EOF' > service.proto
syntax = "proto3";

package mydb;

message SdmRequest {
  int32 id = 1;
}

message SdmResponse {
  int32 id = 1;
  string npp = 2;
  string nama = 3;
}

service SdmService {
  rpc GetSdm (SdmRequest) returns (SdmResponse);
}
EOF
```

<p align="center">
  <img src="images/19_file service proto.png" width="700" alt="Berkas service.proto untuk SdmService.">
  <br>
  <em>Gambar 19. Berkas service.proto untuk SdmService.</em>
</p>

#### Pembahasan

<p align="justify"><code>service.proto</code> mendefinisikan pesan dan layanan: <code>SdmRequest</code> membawa <code>id</code>, <code>SdmResponse</code> membawa tiga <em>field</em>, dan <code>SdmService</code> memiliki satu RPC <code>GetSdm</code>. Berkas ini adalah kontrak; client dan server tidak perlu tahu bahasa implementasinya, cukup bentuk pesannya.</p>

---

<p align="justify">Kompilasi file service.proto menggunakan grpc_tools.protoc untuk menghasilkan kode Python (stub dan message) dengan perintah:</p>

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto
```

<p align="center">
  <img src="images/20_Kompilasi file service proto.png" width="700" alt="Kompilasi service.proto dengan grpc_tools.protoc.">
  <br>
  <em>Gambar 20. Kompilasi service.proto dengan grpc_tools.protoc.</em>
</p>

#### Pembahasan

<p align="justify">Kompilasi mengubah kontrak menjadi kode Python. Opsi <code>-I.</code> menambahkan direktori aktif sebagai jalur pencarian, sedangkan <code>--python_out</code> dan <code>--grpc_python_out</code> menentukan tempat hasilnya. Perintah ini menghasilkan dua berkas yang saling melengkapi.</p>

---

<p align="justify">Hasilnya adalah 2 file yang dapat ditampilkan dengan perintah:</p>

```bash
ls -la service_pb2*
```

<p align="center">
  <img src="images/21_Hasil Kompilasi.png" width="700" alt="Dua berkas hasil kompilasi, yaitu service_pb2.py dan service_pb2_grpc.py.">
  <br>
  <em>Gambar 21. Dua berkas hasil kompilasi, yaitu service_pb2.py dan service_pb2_grpc.py.</em>
</p>

#### Pembahasan

<p align="justify">Hasil kompilasi terdiri dari <code>service_pb2.py</code> untuk struktur pesan dan <code>service_pb2_grpc.py</code> untuk <em>stub</em> serta <em>base class servicer</em>. Keduanya tidak diedit manual karena akan tertimpa setiap kali <code>.proto</code> berubah. Perubahan harus dilakukan di <code>.proto</code>, lalu dikompilasi ulang.</p>

---

#### 2.1. gRPC Server

<p align="justify">Untuk gRPC server ini, request akan dilakukan untuk meminta satu data berdasarkan id tertentu. Jika akan membuat response yang memungkinkan memberikan seluruh data, maka service proto harus menggunakan … repeated … sebagai berikut:</p>

```
syntax = "proto3";
package mydb;

message EmptyRequest {}

message SdmMessage {
  int32 id = 1;
  string npp = 2;
  string nama = 3;
}

message SdmResponse {
  repeated SdmMessage records = 1;
}

service SdmService {
  rpc GetAllSdm (EmptyRequest) returns (SdmResponse);
}
```

<p align="center">
  <img src="images/22_service proto menggunakan repeated.png" width="700" alt="Varian service.proto dengan repeated untuk mengambil seluruh data.">
  <br>
  <em>Gambar 22. Varian service.proto dengan repeated untuk mengambil seluruh data.</em>
</p>

#### Pembahasan

<p align="justify">Varian dengan <code>repeated SdmMessage records</code> menunjukkan cara mengembalikan banyak baris. Kata kunci <code>repeated</code> membuat sebuah <em>field</em> menampung daftar, bukan satu nilai. Pola ini yang dipakai bila server perlu mengirim seluruh data, sementara praktikum memilih satu data per <em>request</em> agar alurnya lebih sederhana.</p>

---

<p align="justify">Source code untuk mengakses data di SQLite dan kemudian menserialisasikan hasilnya ke dalam protocol buffers untuk diakses oleh gRPC client adalah sebagai berikut:</p>

```python
import grpc
from concurrent import futures
from sqlmodel import Field, Session, SQLModel, create_engine, select

import service_pb2
import service_pb2_grpc

class Sdm(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    npp: str
    nama: str

engine = create_engine("sqlite:///departemen-sdm.db")

class SdmServiceServicer(service_pb2_grpc.SdmServiceServicer):
    def GetSdm(self, request, context):
        with Session(engine) as session:
            statement = select(Sdm).where(Sdm.id == request.id)
            results = session.exec(statement)
            sdm_result = results.first()

            if sdm_result is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return service_pb2.SdmResponse()

            return service_pb2.SdmResponse(
                id=sdm_result.id,
                npp=sdm_result.npp,
                nama=sdm_result.nama,
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_SdmServiceServicer_to_server(SdmServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Server started. Listening on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

```

<p align="justify">atau bisa juga menggunakan perintah:</p>

```bash
cat << 'EOF' > server.py
import grpc
from concurrent import futures
from sqlmodel import Field, Session, SQLModel, create_engine, select

import service_pb2
import service_pb2_grpc

class Sdm(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    npp: str
    nama: str

engine = create_engine("sqlite:///departemen-sdm.db")

class SdmServiceServicer(service_pb2_grpc.SdmServiceServicer):
    def GetSdm(self, request, context):
        with Session(engine) as session:
            statement = select(Sdm).where(Sdm.id == request.id)
            results = session.exec(statement)
            sdm_result = results.first()

            if sdm_result is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return service_pb2.SdmResponse()

            return service_pb2.SdmResponse(
                id=sdm_result.id,
                npp=sdm_result.npp,
                nama=sdm_result.nama,
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_SdmServiceServicer_to_server(SdmServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Server started. Listening on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
EOF
```

<p align="center">
  <img src="images/23_Source Code server gRPC.png" width="700" alt="Isi berkas server.py untuk gRPC.">
  <br>
  <em>Gambar 23. Isi berkas server.py untuk gRPC.</em>
</p>

#### Pembahasan

<p align="justify">Server mengimplementasikan <code>GetSdm</code> dengan mencari <code>Sdm.id</code> yang cocok. Jika tidak ada, server mengembalikan status <code>NOT_FOUND</code> dan pesan yang jelas, bukan respons kosong tanpa penjelasan. Di sisi jaringan, <code>add_insecure_port('[::]:50051')</code> membuka port tanpa TLS karena praktikum berjalan di mesin lokal.</p>

---

<p align="justify">Jalankan dengan perintah:</p>

```bash
python server.py
```

<p align="center">
  <img src="images/24_Menjalankan server gRCP.png" width="700" alt="Server gRPC menunggu permintaan di port 50051.">
  <br>
  <em>Gambar 24. Server gRPC menunggu permintaan di port 50051.</em>
</p>

#### Pembahasan

<p align="justify">Server dijalankan dan mencetak pesan bahwa ia mendengarkan di port 50051. Setelah itu proses berhenti di <code>wait_for_termination()</code>, menunggu <em>request</em> sampai dihentikan. Server harus tetap hidup di terminal ini saat client dijalankan.</p>

---

#### 2.2. gRCP Client

<p align="justify">Source code untuk mengirimkan request untuk mengambil data SDM dengan id tertentu adalah sebagai berikut:</p>

```python
import grpc
import service_pb2
import service_pb2_grpc

def run_client():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.SdmServiceStub(channel)

        request = service_pb2.SdmRequest(id=1)
        try:
            response = stub.GetSdm(request)
            print(f"Sdm Name: {response.nama}")
        except grpc.RpcError as e:
            print(f"Error: {e.code()} {e.details()}")

        try:
            request_not_found = service_pb2.SdmRequest(id=10000)
            response = stub.GetSdm(request_not_found)
            print(f"Sdm Name: {response.nama}")
        except grpc.RpcError as e:
            print(f"Error: {e.code()} {e.details()}")

if __name__ == '__main__':
    run_client()
```

<p align="center">
  <img src="images/25_Source Code Client gRPC.png" width="700" alt="Isi berkas client.py untuk gRPC.">
  <br>
  <em>Gambar 25. Isi berkas client.py untuk gRPC.</em>
</p>

#### Pembahasan

<p align="justify">Client membuat <em>channel</em> ke <code>localhost:50051</code>, lalu membungkusnya dengan <code>SdmServiceStub</code>. <em>Stub</em> inilah yang membuat pemanggilan RPC terasa seperti memanggil fungsi biasa. Dua <em>request</em> dikirim: id 1 untuk data yang ada dan id 10000 untuk menguji jalur error.</p>

---

<p align="justify">Pada source code tersebut, dilakukan pengiriman 2 requests: 1 untuk request dengan id yang benar-benar ada (1) dan 1 untuk request dengan id yang benar-benar tidak ada (10000). dapat dijalankan dengan perintah berikut:</p>

```bash
python client.py
```

<p align="center">
  <img src="images/26_Menjalankan Client gRCP.png" width="700" alt="Client mengambil id 1 dan menerima NOT_FOUND untuk id 10000.">
  <br>
  <em>Gambar 26. Client mengambil id 1 dan menerima NOT_FOUND untuk id 10000.</em>
</p>

#### Pembahasan

<p align="justify">Output menampilkan <code>Sdm Name: Karyawan 1</code>, lalu <code>StatusCode.NOT_FOUND User not found</code> untuk id 10000. Dua baris itu menunjukkan bahwa jalur sukses dan jalur gagal sama-sama tertangani. Tanpa <code>try/except</code>, error kedua akan menghentikan program sebelum pesannya terbaca.</p>

---

<p align="justify">Kemudian setelah output sudah sesuai matikan server dan client dengan perintah:</p>

```bash
deactivate
```

<p align="center">
  <img src="images/27_Mematikan server gRCP.png" width="700" alt="Server gRPC dihentikan.">
  <br>
  <em>Gambar 27. Server gRPC dihentikan.</em>
</p>

<p align="center">
  <img src="images/28_Mematikan client gRCP.png" width="700" alt="Virtual environment client gRPC dinonaktifkan.">
  <br>
  <em>Gambar 28. Virtual environment client gRPC dinonaktifkan.</em>
</p>

#### Pembahasan

<p align="justify">Server dan client dihentikan, lalu venv dinonaktifkan. Prompt kembali normal, tanda tidak ada lingkungan virtual yang aktif. Ini penting sebelum berpindah ke tugas, karena tugas memakai folder dan venv yang berbeda lagi.</p>

---

<p align="justify">Kemudian struktur direktori akhir menjadi:</p>

<p align="center">
  <img src="images/29_Struktur direktori akhir.png" width="700" alt="Struktur direktori Praktik09 setelah seluruh praktikum selesai.">
  <br>
  <em>Gambar 29. Struktur direktori Praktik09 setelah seluruh praktikum selesai.</em>
</p>

#### Pembahasan

<p align="justify">Struktur akhir memperlihatkan empat folder dengan isi yang khas: server punya database dan kode, client punya skrip pemanggil. Berkas hasil kompilasi muncul di kedua sisi karena keduanya butuh <em>stub</em> yang sama. Struktur ini menjadi cetak biru untuk bagian tugas.</p>

---

## 📜 Tugas

### 1. Dengan menggunakan file SQLite pada tugas kemarin (tabel yang mempunyai 1 primary key dan setidaknya berisi data dengan tipe INT, CHAR, VARCHAR BOOLEAN, dan FLOAT), buat GraphQL endpoint untuk tabel tersebut dan berikan contoh akses client untuk mengambil semua data.

#### Persiapan Struktur Folder & Salin Database

<p align="justify">Masuk ke folder terlebih dahulu:</p>

```bash
cd ~/Desktop/prak-dis-dec/09/Tugas09
```

<p align="center">
  <img src="images/30_Masuk ke folder terlebih dahulu.png" width="700" alt="Masuk ke direktori Tugas09.">
  <br>
  <em>Gambar 30. Masuk ke direktori Tugas09.</em>
</p>

#### Pembahasan

<p align="justify">Pekerjaan tugas dimulai di folder <code>Tugas09</code>, terpisah dari <code>Praktik09</code>. Pemisahan ini membuat hasil latihan dan hasil tugas tidak tercampur. Database yang dipakai juga berbeda: <code>inventaris.db</code>, bukan <code>departemen-sdm.db</code>.</p>

---

<p align="justify">Buat struktur direktori GraphQL</p>

```bash
mkdir -p src/graphql/server src/graphql/client src/grpc/server src/grpc/client
```

<p align="center">
  <img src="images/31_Buat struktur direktori GraphQL.png" width="700" alt="Struktur direktori tugas dibuat mengikuti pola praktikum.">
  <br>
  <em>Gambar 31. Struktur direktori tugas dibuat mengikuti pola praktikum.</em>
</p>

#### Pembahasan

<p align="justify">Struktur direktori disamakan dengan praktikum: GraphQL dan gRPC, masing-masing server dan client. Meniru struktur yang sudah dikenal mengurangi keputusan teknis yang tidak perlu. Dengan begitu perhatian bisa langsung ke isi tabel dan kode.</p>

---

<p align="justify">Buat file kosong yang dibutuhkan</p>

```bash
touch src/graphql/server/{graphql-server.py,requirements.txt}
touch src/graphql/client/{graphql-client.py,requirements.txt}
```

<p align="center">
  <img src="images/32_Buat file kosong yang dibutuhkan.png" width="700" alt="Berkas kosong untuk server dan client GraphQL tugas.">
  <br>
  <em>Gambar 32. Berkas kosong untuk server dan client GraphQL tugas.</em>
</p>

#### Pembahasan

<p align="justify">Berkas kosong untuk server dan client GraphQL dibuat dalam dua perintah. Memisahkan pembuatan berkas dari pengisian kode membuat kesalahan <em>path</em> lebih mudah terlihat. Kalau satu berkas tidak muncul, masalahnya ada di perintah, bukan di kode.</p>

---

<p align="justify">Salin inventaris.db dari pertemuan 08 ke folder server GraphQL (dan gRPC)</p>

```bash
cp ~/Desktop/prak-dis-dec/08/src/inventaris.db src/graphql/server/
cp ~/Desktop/prak-dis-dec/08/src/inventaris.db src/grpc/server/
```

<p align="center">
  <img src="images/33_Salin inventaris.db dari pertemuan 08 ke folder server GraphQL (dan gRPC).png" width="700" alt="inventaris.db disalin ke folder server GraphQL dan gRPC.">
  <br>
  <em>Gambar 33. inventaris.db disalin ke folder server GraphQL dan gRPC.</em>
</p>

#### Pembahasan

<p align="justify"><code>inventaris.db</code> disalin ke folder server GraphQL dan gRPC. Kedua server membaca database masing-masing, jadi keduanya perlu salinan sendiri. Ini juga menjaga agar pengujian GraphQL tidak mengubah data yang sedang dipakai gRPC.</p>

---

#### Setup & Jalankan GraphQL Server

<p align="justify">Masuk ke folder graphql server terlebih dahulu dengan perintah:</p>

```bash
cd ~/Desktop/prak-dis-dec/09/Tugas09/src/graphql/server
```

<p align="center">
  <img src="images/34_Masuk ke folder graphql server terlebih dahulu dengan perintah.png" width="700" alt="Masuk ke folder GraphQL server tugas.">
  <br>
  <em>Gambar 34. Masuk ke folder GraphQL server tugas.</em>
</p>

#### Pembahasan

<p align="justify">Folder GraphQL server dijadikan direktori kerja. Semua perintah <code>uv</code> berikutnya akan membuat venv dan membaca <code>requirements.txt</code> di sini. Lokasi ini juga yang dipakai <code>sqlite:///inventaris.db</code> untuk menemukan berkas database.</p>

---

<p align="justify">Buat file requirements.txt untuk mendaftarkan library yang dibutuhkan (strawberry-graphql[cli] dan sqlmodel) dengan perintah:</p>

```bash
printf "strawberry-graphql[cli]\nsqlmodel\n" > requirements.txt
```

<p align="center">
  <img src="images/35_Buat file requirements.png" width="700" alt="requirements.txt untuk server GraphQL tugas.">
  <br>
  <em>Gambar 35. requirements.txt untuk server GraphQL tugas.</em>
</p>

#### Pembahasan

<p align="justify">Dependensi server tugas sama dengan praktikum: Strawberry dan SQLModel. Tidak ada paket tambahan karena kebutuhan <em>endpoint</em> juga sama, hanya tabelnya yang berbeda. Kesamaan ini memperlihatkan bahwa pergantian data tidak harus mengubah perkakas.</p>

---

<p align="justify">Atur versi Python menggunakan uv ke versi 3.14.5:</p>

```bash
uv python pin 3.14.5 --managed-python
```

<p align="center">
  <img src="images/36_Atur versi Python.png" width="700" alt="Pin Python 3.14.5 untuk server GraphQL tugas.">
  <br>
  <em>Gambar 36. Pin Python 3.14.5 untuk server GraphQL tugas.</em>
</p>

#### Pembahasan

<p align="justify">Pin versi diulang di folder tugas supaya tidak bergantung pada konfigurasi folder lain. Dengan versi yang sama, perbedaan hasil lebih mungkin berasal dari kode daripada dari interpreter.</p>

---

<p align="justify">Buat virtual environment baru di dalam direktori tersebut:</p>

```bash
uv venv
```

<p align="center">
  <img src="images/37_Buat virtual environment.png" width="700" alt="Virtual environment server GraphQL tugas dibuat.">
  <br>
  <em>Gambar 37. Virtual environment server GraphQL tugas dibuat.</em>
</p>

#### Pembahasan

<p align="justify">Venv baru dibuat di folder server tugas. Meski isinya mirip venv praktikum, folder ini tetap berdiri sendiri. Venv tidak bisa dipinjam dari folder lain tanpa mengubah <em>path</em> interpreter secara manual.</p>

---

<p align="justify">Aktifkan virtual environment yang sudah dibuat dan menginstall seluruh dependensi yang terdaftar pada file requirements.txt::</p>

```bash
source .venv/Scripts/activate
```

<p align="justify">dan</p>

```bash
uv pip install -r requirements.txt
```

<p align="center">
  <img src="images/38_Mengaktifkan virtual environment dan install seluruh dependensi.png" width="700" alt="Dependensi server GraphQL tugas terpasang.">
  <br>
  <em>Gambar 38. Dependensi server GraphQL tugas terpasang.</em>
</p>

#### Pembahasan

<p align="justify">Dependensi server tugas dipasang, dan prompt kembali menunjukkan <code>(server)</code>. Setelah itu perintah <code>strawberry</code> tersedia, jadi server bisa langsung dijalankan begitu kodenya selesai.</p>

---

<p align="justify">Buat file graphql-server.py untuk mendefinisikan model tabel Produk, koneksi database SQLite inventaris.db, serta resolver dan skema query GraphQL:</p>

```bash
cat << 'EOF' > graphql-server.py
import typing
import strawberry
from sqlmodel import Field, Session, SQLModel, create_engine, select

@strawberry.type
class Produk(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    kode: str
    nama: str
    stok: int
    harga: float
    tersedia: bool

engine = create_engine("sqlite:///inventaris.db")

def get_produks():
    with Session(engine) as session:
        statement = select(Produk)
        results = session.exec(statement).all()
        return results

@strawberry.type
class Query:
    produks: typing.List[Produk] = strawberry.field(resolver=get_produks)

schema = strawberry.Schema(query=Query)
EOF
```

<p align="center">
  <img src="images/39_Buat file graphql server.png" width="700" alt="Berkas graphql-server.py untuk tabel produk.">
  <br>
  <em>Gambar 39. Berkas graphql-server.py untuk tabel produk.</em>
</p>

#### Pembahasan

<p align="justify">Model <code>Produk</code> memuat enam kolom: <code>id</code>, <code>kode</code>, <code>nama</code>, <code>stok</code>, <code>harga</code>, dan <code>tersedia</code>. Tipe Python-nya, yaitu <code>int</code>, <code>str</code>, <code>float</code>, dan <code>bool</code>, diterjemahkan menjadi tipe GraphQL yang sesuai. Resolver <code>get_produks</code> mengambil seluruh baris, sehingga <em>endpoint</em> ini menjawab kebutuhan tugas pertama.</p>

---

<p align="justify">Menjalankan server GraphQL dengan perintah:</p>

```bash
strawberry dev graphql-server
```

<p align="center">
  <img src="images/40_Menjalankan server graphql.png" width="700" alt="Server GraphQL tugas berjalan di port 8000.">
  <br>
  <em>Gambar 40. Server GraphQL tugas berjalan di port 8000.</em>
</p>

<p align="justify">kemudian buka http://localhost:8000/graphql di browser dan ketikkan query:</p>

```GraphQL
{
  produks
  {
    id
    kode
    nama
    stok
    harga
    tersedia
  }
}
```

<p align="center">
  <img src="images/41_Menjalankan server graphql di browser.png" width="700" alt="Query produks menampilkan lima data produk.">
  <br>
  <em>Gambar 41. Query produks menampilkan lima data produk.</em>
</p>

#### Pembahasan

<p align="justify">Server berjalan di port 8000, lalu <em>query</em> <code>produks</code> diminta lewat Explorer. Hasilnya lima produk dengan <em>field</em> lengkap, termasuk <code>tersedia: false</code> pada Webcam HD. Nilai boolean yang tampil sebagai <code>true</code> dan <code>false</code> menunjukkan konversi dari SQLite berjalan benar.</p>

---

#### Setup & Jalankan GraphQL Client

<p align="justify">Masuk ke folder client terlebih dahulu menggunakan perintah:</p>

```bash
cd ~/Desktop/prak-dis-dec/09/Tugas09/src/graphql/client
```

<p align="center">
  <img src="images/42_Masuk ke folder client .png" width="700" alt="Masuk ke folder GraphQL client tugas.">
  <br>
  <em>Gambar 42. Masuk ke folder GraphQL client tugas.</em>
</p>

#### Pembahasan

<p align="justify">Folder client GraphQL tugas disiapkan. Client ini nantinya mengirim <em>query</em> yang sama seperti di Explorer, tetapi dari skrip. Karena server masih berjalan, client bisa langsung diuji setelah venv-nya siap.</p>

---

<p align="justify">Buat file requirements.txt untuk mendaftarkan library yang dibutuhkan (gql[aiohttp]) dengan perintah:</p>

```bash
echo "gql[aiohttp]" > requirements.txt
```

<p align="center">
  <img src="images/43_Buat file requirements.txt.png" width="700" alt="requirements.txt untuk client GraphQL tugas.">
  <br>
  <em>Gambar 43. requirements.txt untuk client GraphQL tugas.</em>
</p>

#### Pembahasan

<p align="justify"><code>gql[aiohttp]</code> kembali dipakai. Tidak ada perubahan karena cara client berbicara dengan GraphQL tidak bergantung pada tabel apa yang ada di server.</p>

---

<p align="justify">Atur versi Python proyek menggunakan uv ke versi 3.14.5:</p>

```bash
uv python pin 3.14.5 --managed-python
```

<p align="center">
  <img src="images/44_Atur versi Python.png" width="700" alt="Pin Python untuk client GraphQL tugas.">
  <br>
  <em>Gambar 44. Pin Python untuk client GraphQL tugas.</em>
</p>

#### Pembahasan

<p align="justify">Versi Python client dipin agar sejalan dengan server. Langkah kecil ini menghindari kasus client berjalan di versi berbeda dan menghasilkan pesan error yang membingungkan.</p>

---

<p align="justify">Buat virtual environment baru di dalam direktori client:</p>

```bash
uv venv
```

<p align="center">
  <img src="images/45_Buat virtual environment.png" width="700" alt="Virtual environment client GraphQL tugas dibuat.">
  <br>
  <em>Gambar 45. Virtual environment client GraphQL tugas dibuat.</em>
</p>

#### Pembahasan

<p align="justify">Venv client dibuat terpisah. Isolasi ini menjaga client tetap ringan: hanya <code>gql</code> dan <code>aiohttp</code>, tanpa SQLModel atau Strawberry.</p>

---

<p align="justify">Aktifkan virtual environment yang sudah dibuat dan menginstall seluruh dependensi yang terdaftar pada file requirements.txt:</p>

```bash
source .venv/Scripts/activate
```

<p align="justify">dan</p>

```bash
uv pip install -r requirements.txt
```

<p align="center">
  <img src="images/46_Mengaktifkan Environment dan Intall Depensi.png" width="700" alt="Dependensi client GraphQL tugas terpasang.">
  <br>
  <em>Gambar 46. Dependensi client GraphQL tugas terpasang.</em>
</p>

#### Pembahasan

<p align="justify">Lingkungan client kini hanya berisi <code>gql</code> dan <code>aiohttp</code>. Dengan begitu skrip bisa dijalankan tanpa mengganggu venv server, dan dependensi yang tidak dipakai tidak ikut terpasang.</p>

---

<p align="justify">Buat file graphql-client.py untuk mengatur koneksi ke endpoint GraphQL (http://localhost:8000/graphql) dan mengeksekusi query getProduks secara asynchronous:</p>

```bash
cat << 'EOF' > graphql-client.py
import asyncio
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

async def main():
    transport = AIOHTTPTransport(url="http://localhost:8000/graphql")
    client = Client(transport=transport)

    query = gql(
        """
        query getProduks {
            produks {
                id
                kode
                nama
                stok
                harga
                tersedia
            }
        }
        """
    )

    async with client as session:
        result = await session.execute(query)
        print(result)

asyncio.run(main())
EOF
```

<p align="center">
  <img src="images/47_file graphql-client.png" width="700" alt="Berkas graphql-client.py untuk tabel produk.">
  <br>
  <em>Gambar 47. Berkas graphql-client.py untuk tabel produk.</em>
</p>

#### Pembahasan

<p align="justify"><em>Query</em> <code>getProduks</code> meminta keenam <em>field</em> produk. Karena GraphQL mengembalikan apa yang diminta, hasilnya bisa langsung dipakai untuk menampilkan tabel. <code>print(result)</code> menampilkan struktur <em>dictionary</em> yang dihasilkan <code>gql</code>.</p>

---

<p align="justify">Menjalankan Client untuk menampilkan data produk dari server:</p>

```bash
python graphql-client.py
```

<p align="center">
  <img src="images/48_Menjalankan Client GraphQL.png" width="700" alt="Client GraphQL mencetak lima data produk.">
  <br>
  <em>Gambar 48. Client GraphQL mencetak lima data produk.</em>
</p>

#### Pembahasan

<p align="justify">Output berisi lima produk lengkap dengan tipe datanya. Harga tampil sebagai <em>float</em> dan <code>tersedia</code> sebagai boolean, bukan string. Ini memperlihatkan bahwa <em>schema</em> GraphQL menjaga tipe data sampai ke client.</p>

---

### 2. Dengan menggunakan file SQLite pada tugas kemarin (tabel yang mempunyai 1 primary key dan setidaknya berisi data dengan tipe INT, CHAR, VARCHAR, BOOLEAN, dan FLOAT), buat service.proto untuk semua data tersebut, kompilasi, buat gRPC servernya dan kemudian berikan contoh gRPC client untuk mengambil salah satu data.

#### Prasyarat Setup, Kompilasi service.proto & Jalankan gRPC Server

<p align="justify">Masuk ke folder gRPC server di Tugas09</p>

```bash
cd ~/Desktop/prak-dis-dec/09/Tugas09/src/grpc/server
```

<p align="center">
  <img src="images/49_Masuk ke folder gRPC server di Tugas09.png" width="700" alt="Masuk ke folder gRPC server tugas.">
  <br>
  <em>Gambar 49. Masuk ke folder gRPC server tugas.</em>
</p>

#### Pembahasan

<p align="justify">Folder gRPC server tugas dijadikan direktori kerja. Di sinilah <code>.proto</code>, database, dan kode server akan berkumpul. Berbeda dari GraphQL, langkah pertama di sini adalah memastikan kontraknya benar.</p>

---

<p align="justify">Memastikan database inventaris.db tersedia di folder server:</p>

```bash
cp ~/Desktop/prak-dis-dec/08/src/inventaris.db .
```

<p align="center">
  <img src="images/50_Memastikan database inventaris.db.png" width="700" alt="inventaris.db dipastikan tersedia di folder server.">
  <br>
  <em>Gambar 50. inventaris.db dipastikan tersedia di folder server.</em>
</p>

#### Pembahasan

<p align="justify"><code>inventaris.db</code> dipastikan ada di folder server. Perintah salin diulang untuk berjaga-jaga bila berkas belum ikut terbawa. Tanpa database, server akan berjalan tetapi setiap permintaan berakhir <code>NOT_FOUND</code>.</p>

---

<p align="justify">Menyiapkan environment Python 3.14.5</p>

```bash
printf "grpcio\ngrpcio-tools\nsqlmodel\n" > requirements.txt
uv python pin 3.14.5 --managed-python
uv venv
source .venv/Scripts/activate
uv pip install -r requirements.txt
```

<p align="center">
  <img src="images/51_Menyiapkan environment Python 3.14.5.png" width="700" alt="Persiapan environment Python 3.14.5 untuk gRPC tugas.">
  <br>
  <em>Gambar 51. Persiapan environment Python 3.14.5 untuk gRPC tugas.</em>
</p>

#### Pembahasan

<p align="justify">Empat perintah disatukan: menulis <code>requirements.txt</code>, pin Python, membuat venv, dan memasang dependensi. Penggabungan ini masuk akal karena semuanya menyiapkan satu lingkungan yang sama. Setelah blok ini selesai, <code>grpc_tools</code> sudah bisa dipakai.</p>

---

<p align="justify">Buat service.proto untuk seluruh kolom tabel produk</p>

```bash
cat << 'EOF' > service.proto
syntax = "proto3";

package inventaris;

message ProdukRequest {
  int32 id = 1;
}

message ProdukResponse {
  int32 id = 1;
  string kode = 2;
  string nama = 3;
  int32 stok = 4;
  double harga = 5;
  bool tersedia = 6;
}

service ProdukService {
  rpc GetProduk (ProdukRequest) returns (ProdukResponse);
}
EOF
```

<p align="center">
  <img src="images/53_File service proto.png" width="700" alt="Berkas service.proto untuk ProdukService.">
  <br>
  <em>Gambar 52. Berkas service.proto untuk ProdukService.</em>
</p>

#### Pembahasan

<p align="justify"><code>service.proto</code> memetakan seluruh kolom produk: <code>int32</code> untuk id dan stok, <code>string</code> untuk kode dan nama, <code>double</code> untuk harga, serta <code>bool</code> untuk tersedia. Pemetaan ini penting karena Protocol Buffers menuntut tipe yang eksplisit. <code>ProdukService</code> hanya memiliki satu RPC, <code>GetProduk</code>, sesuai kebutuhan tugas.</p>

---

<p align="justify">Kompilasi service.proto menjadi stub Python</p>

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto
```

<p align="center">
  <img src="images/54_Kompilasi service proto.png" width="700" alt="Kompilasi service.proto menjadi stub Python.">
  <br>
  <em>Gambar 53. Kompilasi service.proto menjadi stub Python.</em>
</p>

#### Pembahasan

<p align="justify">Kompilasi menghasilkan <code>service_pb2.py</code> dan <code>service_pb2_grpc.py</code>. Kedua berkas ini menjadi jembatan antara kode Python dan format biner protobuf. Setelah kompilasi, server dan client bisa mengimpor <em>stub</em> yang sama.</p>

---

<p align="justify">Buat kode server.py untuk melayani query ke inventaris.db</p>

```bash
cat << 'EOF' > server.py
import grpc
from concurrent import futures
from sqlmodel import Field, Session, SQLModel, create_engine, select

import service_pb2
import service_pb2_grpc

class Produk(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    kode: str
    nama: str
    stok: int
    harga: float
    tersedia: bool

engine = create_engine("sqlite:///inventaris.db")

class ProdukServiceServicer(service_pb2_grpc.ProdukServiceServicer):
    def GetProduk(self, request, context):
        with Session(engine) as session:
            statement = select(Produk).where(Produk.id == request.id)
            produk_result = session.exec(statement).first()

            if produk_result is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Produk tidak ditemukan")
                return service_pb2.ProdukResponse()

            return service_pb2.ProdukResponse(
                id=produk_result.id,
                kode=produk_result.kode,
                nama=produk_result.nama,
                stok=produk_result.stok,
                harga=produk_result.harga,
                tersedia=produk_result.tersedia,
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_ProdukServiceServicer_to_server(ProdukServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Server Produk gRPC started. Listening on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
EOF
```

<p align="center">
  <img src="images/55_Kode server.png" width="700" alt="Berkas server.py untuk ProdukService.">
  <br>
  <em>Gambar 54. Berkas server.py untuk ProdukService.</em>
</p>

#### Pembahasan

<p align="justify"><em>Servicer</em> mencari produk berdasarkan <code>request.id</code> dan mengisi <code>ProdukResponse</code> <em>field</em> demi <em>field</em>. Jika produk tidak ada, server mengembalikan <code>NOT_FOUND</code> dengan pesan <code>Produk tidak ditemukan</code>. Pesan ini sengaja berbahasa Indonesia agar mudah dibaca saat pengujian.</p>

---

<p align="justify">Jalankan gRPC server</p>

```bash
python server.py
```

<p align="center">
  <img src="images/56_Jalankan gRPC server.png" width="700" alt="Server gRPC produk berjalan di port 50051.">
  <br>
  <em>Gambar 55. Server gRPC produk berjalan di port 50051.</em>
</p>

#### Pembahasan

<p align="justify">Server produk berjalan di port 50051 dan mencetak pesan kesiapan. Port ini sama dengan praktikum, jadi pastikan server gRPC sebelumnya sudah dimatikan. Dua server pada port yang sama akan gagal, dan pesannya biasanya kurang jelas.</p>

---

#### Prasyarat Setup, Kompilasi & Jalankan gRPC Client

<p align="justify">Masuk ke folder gRPC client</p>

```bash
cd ~/Desktop/prak-dis-dec/09/Tugas09/src/grpc/client
```

<p align="center">
  <img src="images/57_Masuk ke folder gRPC client.png" width="700" alt="Masuk ke folder gRPC client tugas.">
  <br>
  <em>Gambar 56. Masuk ke folder gRPC client tugas.</em>
</p>

#### Pembahasan

<p align="justify">Folder client gRPC tugas disiapkan. Client hanya butuh <em>stub</em> dan runtime gRPC, bukan SQLModel. Karena itu <code>requirements.txt</code>-nya lebih pendek daripada server.</p>

---

<p align="justify">Siapkan environment Python 3.14.5</p>

```bash
printf "grpcio\ngrpcio-tools\n" > requirements.txt
uv python pin 3.14.5 --managed-python
uv venv
source .venv/Scripts/activate
uv pip install -r requirements.txt
```

<p align="center">
  <img src="images/58_Siapkan environment Python 3.14.5.png" width="700" alt="Environment Python 3.14.5 untuk client gRPC tugas.">
  <br>
  <em>Gambar 57. Environment Python 3.14.5 untuk client gRPC tugas.</em>
</p>

#### Pembahasan

<p align="justify"><em>Environment</em> client dibuat dengan <code>grpcio</code> dan <code>grpcio-tools</code>. Paket kedua sebenarnya hanya diperlukan untuk kompilasi <code>.proto</code>, tetapi tetap dipasang agar langkah salin dan kompilasi bisa dilakukan di folder ini.</p>

---

<p align="justify">Salin service.proto dari server dan kompilasi</p>

```bash
cp ../server/service.proto .
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto
```

<p align="center">
  <img src="images/59_Salin service.proto dari server dan kompilasi.png" width="700" alt="service.proto disalin dari server lalu dikompilasi.">
  <br>
  <em>Gambar 58. service.proto disalin dari server lalu dikompilasi.</em>
</p>

#### Pembahasan

<p align="justify"><code>service.proto</code> disalin dari folder server lalu dikompilasi ulang. Kompilasi ulang memastikan <em>stub</em> di client benar-benar identik dengan yang dipakai server. Kalau versi <code>.proto</code> berbeda, pemanggilan RPC bisa gagal dengan pesan yang sulit dilacak.</p>

---

<p align="justify">Buat client.py untuk mengambil salah satu data produk berdasarkan id</p>

```bash
cat << 'EOF' > client.py
import grpc
import service_pb2
import service_pb2_grpc

def run_client():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.ProdukServiceStub(channel)

        # Mengambil salah satu data produk (id = 1)
        request = service_pb2.ProdukRequest(id=1)
        try:
            response = stub.GetProduk(request)
            print("Data Produk Ditemukan:")
            print(f"  ID       : {response.id}")
            print(f"  Kode     : {response.kode}")
            print(f"  Nama     : {response.nama}")
            print(f"  Stok     : {response.stok}")
            print(f"  Harga    : {response.harga}")
            print(f"  Tersedia : {response.tersedia}")
        except grpc.RpcError as e:
            print(f"Error: {e.code()} - {e.details()}")

        # Uji kasus jika id tidak ditemukan (id = 9999)
        try:
            request_not_found = service_pb2.ProdukRequest(id=9999)
            stub.GetProduk(request_not_found)
        except grpc.RpcError as e:
            print(f"\nUji Data Kosong -> Error: {e.code()} - {e.details()}")

if __name__ == '__main__':
    run_client()
EOF
```

<p align="center">
  <img src="images/60_File client.py.png" width="700" alt="Berkas client.py untuk mengambil satu produk.">
  <br>
  <em>Gambar 59. Berkas client.py untuk mengambil satu produk.</em>
</p>

#### Pembahasan

<p align="justify">Client membungkus <em>channel</em> dengan <code>ProdukServiceStub</code>, lalu meminta produk id 1. Setiap <em>field</em> respons dicetak berlabel agar mudah dibaca. <em>Request</em> kedua ke id 9999 sengaja tidak mencetak data, hanya menangkap error untuk menguji jalur kosong.</p>

---

<p align="justify">Jalankan client</p>

```bash
python client.py
```

<p align="center">
  <img src="images/61_Menjalankan Client gRPC.png" width="700" alt="Client menampilkan produk id 1 dan pesan NOT_FOUND untuk id 9999.">
  <br>
  <em>Gambar 60. Client menampilkan produk id 1 dan pesan NOT_FOUND untuk id 9999.</em>
</p>

#### Pembahasan

<p align="justify">Output menampilkan data Keyboard Mekanikal lengkap, lalu <code>StatusCode.NOT_FOUND - Produk tidak ditemukan</code> untuk id 9999. Perbedaan ini menunjukkan bahwa server membedakan data yang ada dan yang tidak ada. Dengan begitu tugas kedua terpenuhi: satu data berhasil diambil, dan kasus gagal tetap tertangani.</p>

---

## 📝 Kesimpulan

<ol>
  <li><p align="justify">GraphQL dan gRPC sama-sama memindahkan kesepakatan ke depan: GraphQL lewat <em>schema</em>, gRPC lewat berkas <code>.proto</code>.</p></li>
  <li><p align="justify">GraphQL lebih luwes bagi client yang ingin memilih <em>field</em>, sedangkan gRPC lebih tegas karena tipe dan bentuk pesan dikunci sejak kompilasi.</p></li>
  <li><p align="justify">Strawberry dan SQLModel memungkinkan satu <em>class</em> Python berperan sebagai model tabel sekaligus tipe GraphQL, sehingga kode tetap ringkas.</p></li>
  <li><p align="justify">Protocol Buffers menuntut pemetaan tipe yang eksplisit; kesalahan tipe baru terasa saat kompilasi atau ketika data dikirim.</p></li>
  <li><p align="justify">Pemisahan <em>virtual environment</em> per folder mencegah konflik dependensi dan membuat sumber masalah lebih mudah dilacak.</p></li>
  <li><p align="justify">Penanganan <code>NOT_FOUND</code> pada kedua pendekatan menunjukkan bahwa jalur gagal sama pentingnya dengan jalur sukses dalam layanan <em>microservices</em>.</p></li>
</ol>

---

## 🗒️ Referensi

<ol>
  <li><p align="justify">Modul 9 - Arsitektur Microservices untuk Sistem Terdistribusi: GraphQL dan gRPC, Praktikum Sistem Terdistribusi dan Terdesentralisasi, Universitas Teknologi Digital Indonesia.</p></li>
  <li><p align="justify">Dokumentasi GraphQL. <a href="https://graphql.org/learn/">https://graphql.org/learn/</a></p></li>
  <li><p align="justify">Dokumentasi Strawberry. <a href="https://strawberry.rocks/docs">https://strawberry.rocks/docs</a></p></li>
  <li><p align="justify">Dokumentasi gql. <a href="https://github.com/graphql-python/gql">https://github.com/graphql-python/gql</a></p></li>
  <li><p align="justify">Dokumentasi gRPC. <a href="https://grpc.io/docs/">https://grpc.io/docs/</a></p></li>
  <li><p align="justify">Dokumentasi Protocol Buffers. <a href="https://protobuf.dev/">https://protobuf.dev/</a></p></li>
  <li><p align="justify">Dokumentasi SQLModel. <a href="https://sqlmodel.tiangolo.com/">https://sqlmodel.tiangolo.com/</a></p></li>
  <li><p align="justify">Dokumentasi uv. <a href="https://docs.astral.sh/uv/">https://docs.astral.sh/uv/</a></p></li>
</ol>
