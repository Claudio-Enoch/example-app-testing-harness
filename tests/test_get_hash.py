import hashlib
import base64

import concurrent.futures

import pytest


def test_get_hash(hash_api):
    body = {"password": "angry_monkey"}
    hash_id = hash_api.post_hash(body=body).text
    response = hash_api.get_hash(_id=hash_id)

    sha512_password = hashlib.sha512(b"angry_monkey").hexdigest()
    base64_encoded = base64.b64encode(sha512_password.encode("ascii")).decode()

    assert response.status_code == 200
    assert response.elapsed.seconds <= 5, "hash computation took more than 5 seconds"
    # this assertion assumes there is no salt in the hash
    assert response.text == base64_encoded, "hash is not returning base64 encoded sha512 hashed password"


@pytest.mark.parametrize("bad_hash_id", [900, -5, 99999999999999999999999999999, "abc"])
def test_non_existent_hash_id(hash_api, bad_hash_id):
    response = hash_api.get_hash(_id=bad_hash_id)
    assert response.status_code == 400
    assert response.text == "Hash not found\n"


def test_unique_hashes_generated(hash_api):
    body = {"password": "angry_monkey"}
    r1_id = hash_api.post_hash(body=body).text
    r2_id = hash_api.post_hash(body=body).text
    r1_hash = hash_api.get_hash(_id=r1_id).text
    r2_hash = hash_api.get_hash(_id=r2_id).text

    assert r1_hash == r2_hash, f"hashes given the same password are different"


def test_concurrent_hash_requests(hash_api):
    body = {"password": "angry_monkey"}

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(hash_api.post_hash, body) for _ in range(3)]
        hash_ids = [future.result().json() for future in futures]
        futures = [executor.submit(hash_api.get_hash, hash_id) for hash_id in hash_ids]
        responses = [future.result() for future in futures]
        for response in responses:
            assert response.status_code == 200
            assert response.text is not None, "empty hash returned"
            assert response.elapsed.seconds <= 5, "call did not return is less than 5 seconds"
