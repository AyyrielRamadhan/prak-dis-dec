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

Kemudian buat dan isi file graphql-server.py dengan source code:

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

Kemudian buat dan isi file graphql-client.py dengan source code:

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

### 2. gRPC

Selanjutnya, setup gRPC server dengan masuk ke folder gRPC server terlebih dahulu menggunakan perintah:

```bash
cd ~/Desktop/Praktik09/src/grpc/server
```

#### Pembahasan

---

Buat file requirements.txt untuk mendaftarkan library yang dibutuhkan (grpcio, grpcio-tools, dan sqlmodel) dengan perintah:

```bash
printf "grpcio\ngrpcio-tools\nsqlmodel\n" > requirements.txt
```

#### Pembahasan

---

Atur versi Python proyek menggunakan uv ke versi 3.14.5 dengan perintah:

```bash
uv python pin 3.14.5 --managed-python
```

<img src="images/16_Atur versi Python.png" width="700">

#### Pembahasan

---

Buat virtual environment baru di dalam direktori tersebut:

```bash
uv venv
```

<img src="images/17_Buat virtual environment.png" width="700">

#### Pembahasan

---

Aktifkan virtual environment yang sudah dibuat:

```bash
source .venv/Scripts/activate
```

Kemudian menginstall depensi yang terdaftar pada file requirements.txt:

```bash
uv pip install -r requirements.txt
```

<img src="images/18_Aktifkan virtual environment dan Install depensi.png" width="700">

#### Pembahasan

---

Buat file service.proto untuk mendefinisikan struktur pesan (SdmRequest dan SdmResponse) serta layanan RPC (SdmService) dengan perintah:

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

<img src="images/19_file service proto.png" width="700">

#### Pembahasan

---

Kompilasi file service.proto menggunakan grpc_tools.protoc untuk menghasilkan kode Python (stub dan message) dengan perintah:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto
```

<img src="images/20_Kompilasi file service proto.png" width="700">

#### Pembahasan

---

Hasilnya adalah 2 file yang dapat ditampilkan dengan perintah:

```bash
ls -la service_pb2*
```

<img src="images/21_Hasil Kompilasi.png" width="700">

#### Pembahasan

---

#### 2.1. gRPC Server

Untuk gRPC server ini, request akan dilakukan untuk meminta satu data berdasarkan id tertentu. Jika akan membuat response yang memungkinkan memberikan seluruh data, maka service proto harus menggunakan … repeated … sebagai berikut:

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

<img src="images/22_service proto menggunakan repeated.png" width="700">

#### Pembahasan

---

Source code untuk mengakses data di SQLite dan kemudian menserialisasikan hasilnya ke dalam protocol buffers untuk diakses oleh gRPC client adalah sebagai berikut:

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

atau bisa juga menggunakan perintah:

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

<img src="images/23_Source Code server gRPC.png" width="700">

#### Pembahasan

---

Jalankan dengan perintah:

```bash
python server.py
```

<img src="images/24_Menjalankan server gRCP.png" width="700">

#### Pembahasan

---

#### 2.2. gRCP Client

Source code untuk mengirimkan request untuk mengambil data SDM dengan id
tertentu adalah sebagai berikut:

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

<img src="images/25_Source Code Client gRPC.png" width="700">

#### Pembahasan

---

Pada source code tersebut, dilakukan pengiriman 2 requests: 1 untuk request dengan id yang benar-benar ada (1) dan 1 untuk request dengan id yang benar-benar tidak ada (10000). dapat dijalankan dengan perintah berikut:

```bash
python client.py
```

<img src="images/26_Menjalankan Client gRCP.png" width="700">

#### Pembahasan

---

Kemudian setelah output sudah sesuai matikan server dan client dengan perintah:

```bash
deactivate
```

<img src="images/27_Mematikan server gRCP.png" width="700">

<img src="images/28_Mematikan client gRCP.png" width="700">

#### Pembahasan

---

Kemudian struktur direktori akhir menjadi:

<img src="images/29_Struktur direktori akhir.png" width="700">

#### Pembahasan:

---

## 📜 Tugas

### 1.

---

## 📝 Kesimpulan

---

## 🗒️ Referensi
