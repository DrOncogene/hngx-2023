import os

from fastapi.testclient import TestClient
import pytest

from api.main import app


MODE = os.getenv("MODE")
if MODE != 'test':
    os.remove('./db.sqlite3')
    pytest.exit("Please set MODE environment variable to 'test' to run tests")

client = TestClient(app)


@pytest.fixture(scope='class')
def create_person_fixture(request):
    """delete db"""
    # test data
    test_mail = "test@mail.com"
    test_name = "test"
    data = {
        "name": test_name,
        "email": test_mail
    }

    post_resp = client.post("/api", json=data)
    person = post_resp.json()

    setattr(request.cls, 'person', person)

    yield

    client.delete(f'/api/{person.get("id")}')


class TestCreate:
    """test create person"""

    # test data
    test_mail = "test@mail.com"
    test_name = "test"
    data = {
        "name": test_name,
        "email": test_mail
    }

    def test_json_required(self):
        """json is required"""
        response = client.post("/api", content="sample data")
        res_data = response.json()['detail'][0]

        assert response.status_code == 422
        assert res_data['msg'] == 'JSON decode error'

    def test_name_is_required(self):
        """name is required"""
        response = client.post("/api", json={"email": self.test_mail})
        res_data = response.json()['detail'][0]

        assert response.status_code == 422
        assert res_data['msg'] == 'Field required'

    def test_email_is_required(self):
        """name is required"""
        response = client.post("/api", json={"name": self.test_name})
        res_data = response.json()['detail'][0]

        assert response.status_code == 422
        assert res_data['msg'] == 'Field required'

    def test_create_person(self):
        """creates a person resource"""
        response = client.post("/api", json=self.data)
        resource = response.json()

        assert response.status_code == 201
        assert resource.get("name") == self.data["name"]
        assert resource.get("email") == self.data["email"]
        assert type(resource.get("id")) is str

        # teardown
        client.delete(f'/api/{resource.get("id")}')


@pytest.mark.usefixtures("create_person_fixture")
class TestRead:
    """test read"""

    # Note: the fixture creates a person resource
    # and sets it as a class attribute

    def test_get_person_invalid_id_or_name(self):
        """get a person resource by id"""

        resp = client.get(f'/api/invalid_id')

        assert resp.status_code == 404

    def test_get_person_by_id(self):
        """get a person resource by id"""

        url_with_id = f'/api/{self.person.get("id")}'

        read_resp = client.get(url_with_id)
        person = read_resp.json()

        assert read_resp.status_code == 200
        assert person.get("name") == self.person.get("name")
        assert person.get("email") == self.person.get("email")
        assert person.get("id") == self.person.get("id")

    def test_get_person_by_name(self):
        """get a person resource by id"""

        url_with_name = f'/api/{self.person.get("name")}'

        read_resp = client.get(url_with_name)
        person = read_resp.json()

        assert read_resp.status_code == 200
        assert person.get("name") == self.person.get("name")
        assert person.get("email") == self.person.get("email")
        assert person.get("id") == self.person.get("id")


@pytest.mark.usefixtures("create_person_fixture")
class TestUpdate:
    """test update endpoint"""

    new_name = "test2"
    new_email = "test2@mail.com"
    new_data = {
        "name": new_name,
        "email": new_email
    }

    # Note: the fixture creates a person resource
    # and sets it as a class attribute

    def test_update_person_invalid_id_or_name(self):
        """get a person resource by id"""

        resp = client.put(f'/api/invalid_id', json={"name": "new_name"})

        assert resp.status_code == 404

    def test_update_id_not_updatable(self):
        """id is not updateable"""

        url_with_id = f'/api/{self.person.get("id")}'

        read_resp = client.put(url_with_id, json={"id": "new_id"})
        person = read_resp.json()

        assert read_resp.status_code == 200

        # id still the same
        assert person.get("id") == self.person.get("id")

    def test_update_person_by_id(self):
        """get a person resource by id"""

        url_with_id = f'/api/{self.person.get("id")}'

        update_resp = client.put(url_with_id, json=self.new_data)
        person = update_resp.json()

        assert update_resp.status_code == 200
        assert person.get("name") == self.new_name
        assert person.get("email") == self.new_email
        assert person.get("id") == self.person.get("id")

    def test_update_person_by_name(self):
        """get a person resource by id"""

        url_with_name = f'/api/{self.person.get("name")}'

        update_resp = client.put(url_with_name, json=self.new_data)
        person = update_resp.json()

        assert update_resp.status_code == 200
        assert person.get("name") == self.new_name
        assert person.get("email") == self.new_email
        assert person.get("id") == self.person.get("id")


@pytest.mark.usefixtures("create_person_fixture")
class TestDelete:
    """test update endpoint"""

    # Note: the fixture creates a person resource
    # and sets it as a class attribute

    def test_delete_person(self):
        """get a person resource by id"""

        url_with_id = f'/api/{self.person.get("id")}'

        delete_resp = client.delete(url_with_id)

        assert delete_resp.status_code == 200

        read_resp = client.get(url_with_id)
        assert read_resp.status_code == 404


if __name__ == "__main__":
    pytest.main(["-s", __file__])

    try:
        os.remove('./test_db.sqlite3')
    except FileNotFoundError:
        pass
