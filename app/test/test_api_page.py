from fastapi.testclient import TestClient
from fastapi.security import APIKeyHeader

import random
import string
from app.main import app
from app.config.consts import config


api_key_header = APIKeyHeader(name="API-Key")
API_KEY = config["API_KEY"]

client = TestClient(app)
random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))



def test_read_main():
    response = client.get(("/"+random_string), headers={'API-Key': API_KEY})
    assert response.status_code == 404