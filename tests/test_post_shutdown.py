import time

import concurrent.futures

import pytest
import requests


@pytest.mark.second_to_last
def test_shutdown_with_open_requests(hash_api):
    body = {"password": "angry_monkey"}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # create hash requests
        workers = [executor.submit(hash_api.post_hash, body) for _ in range(4)]
        hash_ids = [worker.result().json() for worker in workers]
        workers = [executor.submit(hash_api.get_hash, hash_id) for hash_id in hash_ids]
        # wait .1 seconds before shut down (hash generations should continue for the next 4.9 seconds)
        time.sleep(.1)
        shutdown_response = hash_api.post_shutdown()
        responses = [worker.result() for worker in workers]

    for response in responses:
        assert response.status_code == 200
    assert shutdown_response.status_code == 200


@pytest.mark.last
def test_request_after_shutdown(hash_api):
    body = {"password": "angry_monkey"}
    try:
        hash_api.post_hash(body=body)
    except requests.exceptions.ConnectionError:
        pass
    else:
        raise AssertionError("connection made post service shutdown")
