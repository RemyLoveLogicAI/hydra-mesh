# HYDRA-MESH v2.0-QUANTUM API Reference

Autonomous Multi-Agent Swarm Orchestration Engine for Apple Silicon M4 and Distributed Harnesses.

---

## 1. `hydra.auction` — Capability Dutch Auction Protocol

Replaces naive static task routing with algorithmic reverse bidding across satellite agents based on domain affinity, execution latency, and token cost.

### Classes

#### `CapabilityAuctionEngine`
Manages task bidding sessions and cryptographic lease generation.

```python
from hydra.auction import CapabilityAuctionEngine

engine = CapabilityAuctionEngine()
contract = engine.conduct_auction(
    task_description="Refactor Disimage IPC to POSIX Shared Memory",
    timeout_ms=100
)
print(contract.winning_agent, contract.lease_hash, contract.score)
```

- **Methods**:
  - `register_candidate(agent_id: str, name: str, affinity: float, latency_ms: float, cost_tokens: int)`
  - `conduct_auction(task_description: str, timeout_ms: int = 100) -> LeaseContract`
  - `verify_lease(lease_hash: str) -> bool`

#### `LeaseContract` (Dataclass)
- `task_id: str`: Unique SHA256 task identifier.
- `winning_agent: str`: Agent roster identifier (e.g. `agent-5e72212f`).
- `lease_hash: str`: Cryptographic HMAC lease signature.
- `score: float`: Combined auction fitness score ($\text{Affinity} \times \frac{1}{\text{Cost}} \times \frac{1}{\text{Latency}}$).
- `issued_at: float`: Unix timestamp of award.

---

## 2. `hydra.flight_recorder` — Merkle Flight Recorder

Cryptographic append-only binary Merkle tree logging every inter-agent turn, auction lease award, and operator directive with $O(\log N)$ inclusion verification.

### Classes

#### `FlightRecorder`
- **Methods**:
  - `record_event(event_type: str, payload: dict) -> str`: Appends event and returns event hash.
  - `compute_merkle_root() -> str`: Returns 32-byte hexadecimal Merkle root.
  - `verify_integrity() -> tuple[bool, int, str]`: Validates entire chain against tampering.
  - `export_audit_proof(event_index: int) -> list[str]`: Generates audit inclusion proof.

```python
from hydra.flight_recorder import FlightRecorder

recorder = FlightRecorder()
recorder.record_event("NODE_JOIN", {"agent": "Telegram Orchestrator"})
is_valid, count, root = recorder.verify_integrity()
assert is_valid is True
```

---

## 3. `hydra.consensus` — Triadic Dialectical Consensus

Structured deliberation protocol pitting a technical thesis against adversarial critique to produce an actionable synthesis resolution before high-risk execution.

### Classes

#### `TriadicConsensusEngine`
- **Methods**:
  - `deliberate(topic: str, context: dict = None) -> RFCRecord`: Executes Stage 1 (Thesis), Stage 2 (Antithesis), and Stage 3 (Synthesis).
  - `sign_rfc(record: RFCRecord) -> str`: Computes tamper-proof RFC hash.

```python
from hydra.consensus import TriadicConsensusEngine

consensus = TriadicConsensusEngine()
rfc = consensus.deliberate("RFC-002: Apple Silicon Metal Shader Acceleration")
print(rfc.status, rfc.synthesis, rfc.verification_hash)
```

---

## 4. `hydra.dreamer` — Nocturnal Synthesis Engine ("The Dreamer")

Idle-cycle genetic simulation engine running background counterfactual mutations to explore latent architectural performance optimizations.

### Functions & Classes
- `run_dream_cycle(iterations: int = 50) -> list[HypothesisMutation]`: Evaluates genetic permutations.
- `HypothesisMutation`:
  - `id: str`: Mutation identifier (e.g. `MUT-003`).
  - `title: str`: Hypothesis description.
  - `fitness_score: float`: Simulated gain percentage.
  - `proof_hash: str`: Reproducibility hash.

---

## 5. `hydra.disimage` — TrueColor Half-Block Rasterizer

Zero-dependency 24-bit ANSI terminal rasterizer utilizing Unicode half-block characters (`▀` / `▄`) to render TrueColor graphics directly inside terminal stdout at 482+ FPS.

### Functions
- `render_half_block(matrix_rgb: list[list[tuple]]) -> str`: Converts RGB buffer to ANSI escape string.
- `generate_swarm_svg(nodes: list[dict], width: int = 800, height: int = 400) -> str`: Vector diagram generator.
- `benchmark_rasterizer(frames: int = 100) -> dict`: Measures FPS and frame execution latency.

---

## 6. `hydra.daemon` & `hydra.telemetry` — Background Telemetry

- `get_m4_metrics() -> dict`: Reads Darwin ARM64 hardware stats, thermal pressure, and unified memory.
- `HydraDaemon.emit_heartbeat()`: Atomically writes state to `/Users/lovelogic/OpenBot/Shared/hydra_daemon_state.json`.

---

## 7. `hydra.mcp_server` & `hydra.mcp_gumroad` — MCP Tools

Exposes 12 typed JSON-RPC tools for Claude, Gemini, and OpenBot harnesses:
- `get_swarm_status`, `dispatch_task`, `audit_flight_log`, `export_topology_svg`
- `run_capability_auction`, `verify_merkle_flight_log`, `run_nocturnal_synthesis`
- `gumroad_list_products`, `gumroad_get_product`, `gumroad_create_product`, `gumroad_get_sales`, `gumroad_oauth_status`
