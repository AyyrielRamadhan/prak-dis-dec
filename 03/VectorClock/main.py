from vector_clock import VectorClock

# Membuat tiga proses
vc0 = VectorClock(num_processes=3, process_id=0)
vc1 = VectorClock(num_processes=3, process_id=1)
vc2 = VectorClock(num_processes=3, process_id=2)

print("=== Vector Clock Awal ===")
print(vc0)
print(vc1)
print(vc2)

# Proses 0 melakukan event lokal
print("\n=== Proses 0 melakukan event lokal ===")
vc0.increment()
print(vc0)

# Proses 0 mengirim pesan ke proses 1
print("\n=== Proses 0 mengirim pesan ke Proses 1 ===")
message_from_p0 = vc0.send_message()
vc1.receive_message(message_from_p0)
print(vc0)
print(vc1)

# Proses 2 melakukan event lokal
print("\n=== Proses 2 melakukan event lokal ===")
vc2.increment()
print(vc2)

# Proses 1 mengirim pesan ke proses 2
print("\n=== Proses 1 mengirim pesan ke Proses 2 ===")
message_from_p1 = vc1.send_message()
vc2.receive_message(message_from_p1)
print(vc1)
print(vc2)

# Memeriksa hubungan sebab-akibat
print("\n=== Pemeriksaan Kausalitas ===")
print(
    f"VC0 happens before VC1: "
    f"{vc0.happens_before(vc1)}"
)
print(
    f"VC1 happens before VC0: "
    f"{vc1.happens_before(vc0)}"
)
print(
    f"VC0 is concurrent with VC2: "
    f"{vc0.is_concurrent(vc2)}"
)
