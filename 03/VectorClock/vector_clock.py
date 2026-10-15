
class VectorClock:
    def __init__(self, num_processes, process_id):
        self.clocks = [0] * num_processes
        self.process_id = process_id

    def increment(self):
        """Menambah jam lokal proses."""
        self.clocks[self.process_id] += 1

    def send_message(self):
        """Mengirim salinan vector clock."""
        self.increment()
        return list(self.clocks)

    def receive_message(self, received_clocks):
        """Memperbarui vector clock saat menerima pesan."""
        for i in range(len(self.clocks)):
            self.clocks[i] = max(
                self.clocks[i], received_clocks[i]
            )
        self.increment()

    def __str__(self):
        return f"P{self.process_id}: {self.clocks}"

    def happens_before(self, other_vector_clock):
        """Memeriksa hubungan sebab-akibat."""
        if self.clocks == other_vector_clock.clocks:
            return False

        any_lt = False

        for i in range(len(self.clocks)):
            if self.clocks[i] > other_vector_clock.clocks[i]:
                return False

            if self.clocks[i] < other_vector_clock.clocks[i]:
                any_lt = True

        return any_lt

    def is_concurrent(self, other_vector_clock):
        """Memeriksa apakah dua vector clock bersamaan."""
        return not (
            self.happens_before(other_vector_clock)
            or other_vector_clock.happens_before(self)
        )