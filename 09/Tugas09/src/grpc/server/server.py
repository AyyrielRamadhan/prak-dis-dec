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
