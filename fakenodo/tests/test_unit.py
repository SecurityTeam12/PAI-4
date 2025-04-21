import pytest
from unittest.mock import patch
import json
from fakenodo.app.models import Deposition
import io


PATH_GET_ALL_DEPOSITIONS = 'fakenodo.app.routes.service.get_all_depositions'


DEPOSITIONS_URI = '/api/fakenodo/depositions'
DEPOSITION_URI = '/api/fakenodo/depositions/1'
UPLOAD_FILE_URI = '/api/fakenodo/depositions/1/files'
PUBLISH_URI = '/api/fakenodo/depositions/1/actions/publish'
DOI_URI = '/api/fakenodo/depositions/1/doi'
UPLOAD_FILE_URI = '/api/fakenodo/depositions/1/files'


SAMPLE_DEPOSITION = {
    "metadata": {
        "title": "Test Deposition",
        "upload_type": "dataset",
        "description": "This is a test deposition",
        "creators": [{"name": "John Doe"}],
    }
}


@pytest.fixture(scope="module")
def test_client(test_client):
    yield test_client


def mock_service(method, return_value=None, side_effect=None):
    return patch(f'fakenodo.app.routes.service.{method}', return_value=return_value, side_effect=side_effect)


def test_get_all_depositions_with_no_depositions(test_client):
    '''Test fakenodo deposition list without posting any deposition'''

    with mock_service('get_all_depositions', return_value=[]):
        response = test_client.get(DEPOSITIONS_URI)
        assert response.status_code == 200
        assert b'[]' in response.data


def test_post_depositions(test_client):
    '''Test post a deposition into fakenodo'''

    with mock_service('create_new_deposition', return_value=SAMPLE_DEPOSITION["metadata"]):
        response = test_client.post(DEPOSITIONS_URI, json=SAMPLE_DEPOSITION)
        assert response.status_code == 201
        assert b'This is a test deposition' in response.data


def test_get_all_depositions_with_depositions(test_client):
    '''Test fakenodo deposition list with depositions'''

    mock_deposition = Deposition(**SAMPLE_DEPOSITION["metadata"]).to_dict()
    with mock_service('get_all_depositions', return_value=[mock_deposition]):
        response = test_client.get(DEPOSITIONS_URI)
        assert response.status_code == 200
        assert b'[]' not in response.data
        response_list = json.loads(response.data.decode('utf-8'))
        assert len(response_list) == 1
        assert response_list[0]['description'] == mock_deposition['description']


def test_get_deposition(test_client):
    with mock_service('get_deposition', return_value=Deposition(title="Test Deposition")):
        response = test_client.get(DEPOSITION_URI)

        assert response.status_code == 200, response.data
        assert b'Test Deposition' in response.data, response.data


def test_delete_deposition(test_client):

    with mock_service('delete_deposition', return_value=None):
        with mock_service('get_deposition', return_value=Deposition(title="Test Deposition")):
            response = test_client.delete(DEPOSITION_URI)

            assert response.status_code == 204, response.data
            assert b'' == response.data, response.data


def create_sample_file():
    """Create a sample file"""

    data = io.BytesIO(b"Test file content")
    data.name = "test_file.txt"
    data.seek(0)
    return data


def test_upload_file(test_client):
    """Test de carga de archivo"""
    file_data = create_sample_file()

    with mock_service('upload_file', return_value=None):

        response = test_client.post(
            UPLOAD_FILE_URI,
            data={'file': (file_data, 'test_file.txt')},
            content_type='multipart/form-data'
        )

        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        assert b'File uploaded succesfully' in response.data, response.data


def test_publish_deposition(test_client):
    '''Test publish deposition'''

    with mock_service('get_deposition', return_value=Deposition(title="Test Deposition")):
        response = test_client.post(PUBLISH_URI)
        assert response.status_code == 201
        assert b'published succesfully' in response.data, response.data


def test_get_doi(test_client):
    '''Test get DOI of deposition'''

    doi = "10.1234/test.doi"
    with mock_service('get_doi', return_value=doi):
        response = test_client.get(DOI_URI)
        assert response.status_code == 200, response.data
        assert b'"doi":"' + doi.encode() in response.data, response.data


def test_deposition_not_found(test_client):
    '''Test if deposition is not found for GET, DELETE, and Publish actions'''

    with mock_service('get_deposition', side_effect=ValueError("Not found")):
        response = test_client.get('/api/fakenodo/depositions/999')
        assert response.status_code == 404, response.data
        assert b'Cannot find deposition with id' in response.data

        response = test_client.delete('/api/fakenodo/depositions/999')
        assert response.status_code == 404, response.data
        assert b'Cannot find deposition with id' in response.data

        response = test_client.post('/api/fakenodo/depositions/999/actions/publish')
        assert response.status_code == 404, response.data
        assert b'Deposition not found' in response.data
