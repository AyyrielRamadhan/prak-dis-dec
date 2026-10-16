
import time
from raft import RaftNode, State


def simulate_raft():
    node_ids = [1, 2, 3]

    nodes = [
        RaftNode(node_id, node_ids)
        for node_id in node_ids
    ]

    print("Simulasi Raft untuk Koordinasi Drone")
    print("Jumlah node:", len(nodes))

    # Menjalankan simulasi selama 20 langkah
    for step in range(20):
        time.sleep(0.5)

        print(f"\n--- Step {step + 1} ---")

        leaders = [
            node for node in nodes
            if node.state == State.LEADER
        ]

        if leaders:
            leader = leaders[0]
            
            for node in nodes:
                if node.id != leader.id:
                    node.on_heartbeat(leader.current_term)
                    
            if step % 5 == 0:
                leader.append_entry(
                    f"command-{step}"
                )

        for node in nodes:
            node.tick()

        for node in nodes:
            print(
                f"Node {node.id} | "
                f"State: {node.state.name} | "
                f"Term: {node.current_term} | "
                f"Log: {node.log}"
            )


if __name__ == "__main__":
    simulate_raft()
