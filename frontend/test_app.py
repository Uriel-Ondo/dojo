import pytest
from app import app
from unittest.mock import patch, Mock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_with_data(client):
    mock_data = [{"id": 1, "name": "Test Item"}]
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = mock_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        response = client.get('/')
        assert response.status_code == 200
        # Vérifier que la réponse contient les données (on peut checker le texte HTML)
        assert b'Test Item' in response.data

def test_index_without_data(client):
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("Connection error")
        response = client.get('/')
        assert response.status_code == 200
        assert b'Aucune donn\xc3\xa9e disponible' in response.data  # "Aucune donnée disponible" en bytes