# ratios: loc_comments=38:2 imports_exports=1:10 calls_definitions=20:10
# GPT/Claude generated; context, prompt Erin Spencer
import pytest

from pcea.kdf import _canonical_transcript, key_stream

# === CHECKS ===
# id: check_kdf_transcript_is_typed_canonical_integer_bytes
#   proves: kdf_transcript_is_typed_canonical_integer_bytes
#   call: self::test_canonical_transcript_is_stable_and_length_delimited
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
# === END CHECKS ===


def test_output_length():
    assert len(key_stream([42, 1, 2], 0, 0, 0, 10, 7)) == 10


def test_digits_in_range():
    for p in [2, 3, 7, 13, 241]:
        result = key_stream([999, 0, 1], 5, 3, 2, 50, p)
        assert all(0 <= d < p for d in result)


def test_deterministic():
    a = key_stream([7, 3, 11], 0, 1, 2, 20, 11)
    b = key_stream([7, 3, 11], 0, 1, 2, 20, 11)
    assert a == b


def test_different_contributors_give_different_stream():
    a = key_stream([0, 0, 0], 0, 0, 0, 32, 7)
    b = key_stream([1, 0, 0], 0, 0, 0, 32, 7)
    assert a != b


def test_zero_contributors_not_zero_stream():
    result = key_stream([0, 0, 0], 0, 0, 0, 32, 7)
    assert any(d != 0 for d in result)


def test_different_seed_idx_gives_different_stream():
    a = key_stream([42, 1, 2], 0, 3, 4, 32, 7)
    b = key_stream([42, 1, 2], 1, 3, 4, 32, 7)
    assert a != b


def test_different_circle_idx_gives_different_stream():
    a = key_stream([42, 1, 2], 0, 0, 4, 32, 7)
    b = key_stream([42, 1, 2], 0, 1, 4, 32, 7)
    assert a != b


def test_different_tensor_idx_gives_different_stream():
    a = key_stream([42, 1, 2], 0, 3, 0, 32, 7)
    b = key_stream([42, 1, 2], 0, 3, 1, 32, 7)
    assert a != b


def test_neighbor_contribution_matters():
    # Same own value, different neighbors
    a = key_stream([10, 0, 0], 0, 0, 0, 32, 7)
    b = key_stream([10, 5, 0], 0, 0, 0, 32, 7)
    assert a != b


def test_length_beyond_one_hash_block():
    result = key_stream([1, 2, 3], 0, 0, 0, 100, 5)
    assert len(result) == 100
    assert all(0 <= d < 5 for d in result)


def test_canonical_transcript_is_stable_and_length_delimited():
    args = ([1, -2, 3], 4, 5, 6, 32, 157, 0)
    first = _canonical_transcript(*args)
    assert first == _canonical_transcript(*args)
    assert first.hex() == (
        "504345412d4b44462d494e542d763100000000000000000300000000000000000101"
        "01000000000000000102000000000000000001030000000000000000010400000000"
        "00000000010500000000000000000106000000000000000001200000000000000000"
        "019d00000000000000000100"
    )
    assert key_stream([1, -2, 3], 4, 5, 6, 32, 157) == [
        89, 7, 31, 90, 86, 87, 141, 148, 152, 76, 42, 69, 32, 16, 135, 58,
        110, 24, 28, 23, 14, 44, 135, 56, 24, 130, 90, 152, 109, 128, 118, 156,
    ]
    assert first != _canonical_transcript([1, -2, 3], 4, 5, 6, 31, 157, 0)
    assert first != _canonical_transcript([1, -2, 3], 4, 5, 6, 32, 157, 1)


@pytest.mark.parametrize("invalid", [True, 1.0, "1", None])
def test_key_stream_rejects_non_exact_integer_contributors(invalid):
    with pytest.raises(ValueError, match="exact integer"):
        key_stream([invalid, 2, 3], 0, 0, 0, 8, 7)


@pytest.mark.parametrize("field_index", range(1, 7))
@pytest.mark.parametrize("invalid", [True, 1.0, "1", None])
def test_transcript_rejects_non_exact_integer_fields(field_index, invalid):
    args = [[1, 2, 3], 0, 0, 0, 8, 7, 0]
    args[field_index] = invalid
    with pytest.raises(ValueError):
        _canonical_transcript(*args)
# ratios: loc_comments=38:2 imports_exports=1:10 calls_definitions=20:10
