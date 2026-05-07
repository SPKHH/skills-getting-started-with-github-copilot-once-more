def test_root_redirects_to_static(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_map(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_successfully_adds_participant(client):
    email = "new.student@mergington.edu"

    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email in participants


def test_signup_fails_for_unknown_activity(client):
    response = client.post("/activities/Nonexistent Activity/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_fails_if_student_already_signed_up(client):
    response = client.post("/activities/Chess Club/signup", params={"email": "michael@mergington.edu"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_fails_if_activity_is_full(client):
    for idx in range(2, 11):
        email = f"student{idx}@mergington.edu"
        response = client.post("/activities/Tennis Club/signup", params={"email": email})
        assert response.status_code == 200

    response = client.post("/activities/Tennis Club/signup", params={"email": "overflow.student@mergington.edu"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_unregister_removes_participant(client):
    email = "olivia@mergington.edu"

    response = client.delete("/activities/Gym Class/participants", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Gym Class"

    activities_response = client.get("/activities")
    participants = activities_response.json()["Gym Class"]["participants"]
    assert email not in participants


def test_unregister_fails_for_unknown_activity(client):
    response = client.delete("/activities/Nonexistent Activity/participants", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_fails_for_missing_participant(client):
    response = client.delete("/activities/Chess Club/participants", params={"email": "missing@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
