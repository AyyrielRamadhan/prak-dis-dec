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
