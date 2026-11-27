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
