from cgi import test
from fastapi.testclient import TestClient
from src.main import app
from src.classes.funcs import md5,sha1,sha256

client = TestClient(app)
with TestClient(app) as client:

    def test_read_root():
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"msg": "Hello World"}

    def test_read_docs():
        response = client.get("/docs")
        assert response.status_code == 200
        response = client.get("/redoc")
        assert response.status_code == 200

    def test_read_hashes():
        test_criteria = "Hello"
        hashes = {
            "md5": md5(test_criteria),
            "sha1": sha1(test_criteria),
            "sha256": sha256(test_criteria),
        }

        # Test MD5/ endpoint
        response = client.get(f"/md5/{test_criteria}")
        assert response.status_code == 200
        assert response.json() == {"md5": hashes['md5']}

        # Test SHA1/ endpoint
        response = client.get(f"/sha1/{test_criteria}")
        assert response.status_code == 200
        assert response.json() == {"sha1": hashes['sha1']}

        # Test SHA256/ endpoint
        response = client.get(f"/sha256/{test_criteria}")
        assert response.status_code == 200
        assert response.json() == {"sha256": hashes['sha256']}

        # Test hashes/ endpoint
        response = client.get(f"/hashes/{test_criteria}")
        assert response.status_code == 200
        assert response.json() == hashes

    def test_read_health():
        response = client.get("/health/")
        assert response.status_code == 200

    def test_read_health_healthy():
        """ Check /health/ and fail if any services are down """
        response = client.get("/health/")
        assert response.status_code == 200
        for _,v in response.json().items():
            if v is False:
                assert False

    def test_read_services():
        response = client.get("/services")
        assert response.status_code == 200