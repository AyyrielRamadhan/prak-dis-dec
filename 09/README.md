# Praktikum Minggu 09 - Arsitektur Microservices untuk Sistem Terdistribusi: GraphQL dan gRPC

<p align="justify"><strong>Mata Kuliah:</strong> Praktikum Sistem Terdistribusi dan Terdesentralisasi</p>

<p align="justify"><strong>Topik:</strong> Arsitektur Microservices untuk Sistem Terdistribusi: GraphQL dan gRPC</p>

---

## 🎯 Tujuan Praktikum

---

## 📚 Dasar Teori

---

## ⏩ Pembahasan Praktikum

### 0. Persyaratan

Buat struktur direktori dengan perintah:

```bash
mkdir -p src/graphql/server src/graphql/client src/grpc/server src/grpc/client
```

<img src="images/01_Struktur Direktori.png" width="700">

#### Pembahasan

---

### 1. GraphQL

#### 1.1. GraphQL Server

Buat file kosong yang dibutuhkan dengan perintah:

```bash
touch src/graphql/server/{graphql-server.py,requirements.txt}
```

#### Pembahasan

---

Kemudian salin database dari pertemuan 8 ke folder GraphQL server dengan perintah:

```bash
cp ../prak-dis-dec/08/src/departemen-sdm.db src/graphql/server/
```

#### Pembahasan

---

Lalu setup GraphQL server, dengan masuk ke folder graphql server terlebih dahulu dengan perintah:

```bash
cd ~/Desktop/Praktik09/src/graphql/server
```

#### Pembahasan

---

Buat file requirements.txt untuk mendaftarkan library yang dibutuhkan (strawberry-graphql[cli] dan sqlmodel) dengan perintah:

```bash
printf "strawberry-graphql[cli]\nsqlmodel\n" > requirements.txt
```

#### Pembahasan

---

Atur versi Python proyek menggunakan uv ke versi 3.14.5:

```bash
uv python pin 3.14.5 --managed-python
```

<img src="images/02_Atur Versi Python.png" width="700">

#### Pembahasan

---

Buat virtual environment baru di dalam direktori tersebut:

```bash
uv venv
```

<img src="images/03_Buat virtual environment.png" width="700">

#### Pembahasan

---

Aktifkan virtual environment yang sudah dibuat dengan perintah:

```bash
source .venv/Scripts/activate
```

Lalu install seluruh dependensi yang terdaftar pada file requirements.txt:

```bash
uv pip install -r requirements.txt
```

<img src="images/04_Aktifkan Environment dan Install Depensi.png" width="700">

#### Pembahasan

---

Kemudian isi file graphql-server.py dengan source code:

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

<img src="images/05_Souce Code graphql-server.png" width="700">

#### Pembahasan

---

Menjalankan server Strawberry GraphQL untuk menguji skema yang telah dibuat dengan perintah:

```bash
strawberry dev graphql-server
```

<img src="images/06_Menjalankan server Strawberry GraphQL.png" width="700">

#### Pembahasan

---

Selanjutnya buka http://localhost:8000/graphql pada browser

<img src="images/07_Open GraphQL pada Browser.png" width="700">

Lalu ketikan query berikut pada kotak kiri:

```GraphQL
{
  sdms {
    id
    npp
    nama
  }
}
```

<img src="images/08_Hasil Query GraphQL.png" width="700">

#### Pembahasan

---

#### 1.2. GraphQL Client

Buat file kosong yang dibutuhkan dengan perintah:

```bash
touch src/graphql/client/{graphql-client.py,requirements.txt}
```

#### Pembahasan

---

Selanjutnya, setup GraphQL client dengan masuk ke folder client terlebih dahulu menggunakan perintah:

```bash
cd ~/Desktop/Praktik09/src/graphql/client
```

#### Pembahasan

---

Buat file requirements.txt untuk mendaftarkan library yang dibutuhkan (gql[aiohttp]) dengan perintah:

```bash
echo "gql[aiohttp]" > requirements.txt
```

#### Pembahasan

---

Atur versi Python proyek menggunakan uv ke versi 3.14.5 dengan perintah:

```bash
uv python pin 3.14.5 --managed-python
```

<img src="images/09_Atur versi Python.png" width="700">

#### Pembahasan

---

Buat virtual environment baru di dalam direktori client dengan perintah:

```bash
uv venv
```

<img src="images/10_Buat virtual environment baru di dalam direktori client.png" width="700">

#### Pembahasan

---

Aktifkan virtual environment yang sudah dibuat:

```bash
source .venv/Scripts/activate
```

Lalu install seluruh dependensi yang terdaftar pada file requirements.txt dengan perintah:

```bash
uv pip install -r requirements.txt
```

<img src="images/11_Aktifkan virtual environment dan install seluruh dependensi.png" width="700">

#### Pembahasan

---

Kemudian isi file graphql-client.py dengan source code:

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

<img src="images/12_Source Code graphql-client.png" width="700">

#### Pembahasan

---

Terakhir, pastikan server GraphQL (graphql-server) sudah berjalan, lalu jalankan skrip client untuk mengambil dan menampilkan data dari server dengan perintah:

```bash
python graphql-client.py
```

<img src="images/13_Menjalankan graphql-client.png" width="700">

#### Pembahasan

---

Setelah output data karyawan muncul, hentikan server dan client dengan menekan Ctrl + C untuk server, lalu ketik deactivate di server dan client.

<img src="images/14_Menghentikan GraphQL Server.png" width="700">

<img src="images/15_Menghentikan GraphQL Client.png" width="700">

#### Pembahasan

---

## 📜 Tugas

---

## 📝 Kesimpulan

---

## 🗒️ Referensi
