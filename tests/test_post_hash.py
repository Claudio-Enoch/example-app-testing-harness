import pytest

import concurrent.futures


def test_create_hash(hash_api):
    body = {"password": "angry_monkey"}
    response = hash_api.post_hash(body=body)

    assert response.elapsed.seconds < 1, f"response time is not sub-second 'instant'"
    assert response.status_code == 200, f"response status code not 200"


@pytest.mark.parametrize("body, status_code",
                         [({}, 400),
                          ({"password": ""}, 200),
                          ({"password": None}, 400),
                          ({"wrong_key": "value"}, 400),
                          (None, 400)],
                         )
def test_malformed_hash_bodies(hash_api, body, status_code):
    response = hash_api.post_hash(body=body)
    print("TEXT: ",response.text)

    assert response.status_code == status_code, f"response status code not {status_code}"


def test_multiple_hash_requests(hash_api):
    body = {"password": "password"}
    r1 = hash_api.post_hash(body=body).json()
    r2 = hash_api.post_hash(body=body).json()
    assert r1 > 0, "response body is not an int greater than 0"
    assert r1 != r2, "hash ids are not unique"


def test_hash_error_response(hash_api):
    body = None
    response = hash_api.post_hash(body=body)

    assert response.text == "Malformed Input\n"


def test_concurrent_hash_requests(hash_api):
    body = {"password": "angry_monkey"}

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(hash_api.post_hash, body) for _ in range(3)]
        responses = [future.result() for future in futures]
    for response in responses:
        assert response.status_code == 200
