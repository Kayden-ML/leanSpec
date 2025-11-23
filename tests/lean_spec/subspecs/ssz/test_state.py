from lean_spec.subspecs.containers import (
    SignedBlockWithAttestation,
)
from lean_spec.subspecs.containers.block.block import (
    BlockHeader,
    SignedBlockWithAttestation,
)
from lean_spec.subspecs.containers import (
    State,
)
from lean_spec.subspecs.containers.block.types import Attestations, BlockSignatures
from lean_spec.subspecs.containers.checkpoint import Checkpoint

from lean_spec.subspecs.containers.config import Config
from lean_spec.subspecs.containers.state.types import (
    HistoricalBlockHashes,
    JustificationRoots,
    JustificationValidators,
    JustifiedSlots,
    Validators,
)
from lean_spec.types import Bytes32, ValidatorIndex
from lean_spec.types.uint import Uint64


def test_encode_decode_state_roundtrip() -> None:
    block_header = BlockHeader(
        slot=0,
        proposer_index=ValidatorIndex(0),
        parent_root=Bytes32.zero(),
        state_root=Bytes32(b"state" + b"\x00" * 27),
        body_root=Bytes32(b"body" + b"\x00" * 28),
    )
    temp_finalized = Checkpoint(root=Bytes32(b"genesis" + b"\x00" * 25), slot=0)
    state = State(
        config=Config(genesis_time=Uint64(1000)),
        slot=0,
        latest_block_header=block_header,
        latest_justified=temp_finalized,
        latest_finalized=temp_finalized,
        historical_block_hashes=HistoricalBlockHashes(data=[]),
        justified_slots=JustifiedSlots(data=[]),
        justifications_roots=JustificationRoots(data=[]),
        justifications_validators=JustificationValidators(data=[]),
        validators=Validators(data=[]),
    )

    encode = state.encode_bytes()
    assert (
        encode.hex()
        == "e80300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007374617465000000000000000000000000000000000000000000000000000000626f64790000000000000000000000000000000000000000000000000000000067656e6573697300000000000000000000000000000000000000000000000000000000000000000067656e65736973000000000000000000000000000000000000000000000000000000000000000000e4000000e4000000e5000000e5000000e50000000101"
    )
    assert State.decode_bytes(encode) == state
