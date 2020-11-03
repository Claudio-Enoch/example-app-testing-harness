def test_base_get_stats(hash_api):
    response = hash_api.get_stats()
    total_requests, average_time = response.json()["TotalRequests"], response.json()["AverageTime"]
    body = {"password": "password"}
    new_hash_id = hash_api.post_hash(body=body).json()

    assert response.status_code == 200
    assert new_hash_id == total_requests + 1, "subsequent request did not increment total request"
    assert total_requests >= 0
    assert 0 < average_time < 5000, "average time in ms should be between 0 and 5 sec"
