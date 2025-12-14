"""Tests for EntityService"""
import pytest
from unittest.mock import Mock, MagicMock
from bshengine.services import EntityService
from bshengine import BshClient, BshResponse, BshSearch, Filter, Pagination


class TestEntityService:
    """Test EntityService class"""

    @pytest.fixture
    def mock_client(self):
        """Create mock client"""
        client = Mock(spec=BshClient)
        client.get = Mock()
        client.post = Mock()
        client.put = Mock()
        client.delete = Mock()
        client.download = Mock()
        return client

    @pytest.fixture
    def entity_service(self, mock_client):
        """Create EntityService instance"""
        return EntityService(mock_client, "TestEntity")

    def test_find_by_id(self, entity_service, mock_client):
        """Test find_by_id method"""
        mock_response = BshResponse(
            data=[{"id": "1", "name": "Test"}],
            code=200,
            status="OK",
            timestamp=1234567890,
        )
        mock_client.get.return_value = mock_response

        result = entity_service.find_by_id(id="1")

        assert mock_client.get.called
        call_args = mock_client.get.call_args[0][0]
        assert call_args.path == "/api/entities/TestEntity/1"
        assert call_args.api == "entities.TestEntity.findById"
        assert result == mock_response

    def test_find_by_id_with_custom_entity(self, entity_service, mock_client):
        """Test find_by_id with custom entity"""
        mock_response = BshResponse(
            data=[{"id": "1"}],
            code=200,
            status="OK",
            timestamp=1234567890,
        )
        mock_client.get.return_value = mock_response

        entity_service.find_by_id(id="1", entity="CustomEntity")

        call_args = mock_client.get.call_args[0][0]
        assert call_args.path == "/api/entities/CustomEntity/1"
        assert call_args.api == "entities.CustomEntity.findById"

    def test_create(self, entity_service, mock_client):
        """Test create method"""
        mock_response = BshResponse(
            data=[{"id": "1", "name": "New Entity"}],
            code=201,
            status="Created",
            timestamp=1234567890,
        )
        mock_client.post.return_value = mock_response

        payload = {"name": "New Entity"}
        result = entity_service.create(payload)

        assert mock_client.post.called
        call_args = mock_client.post.call_args[0][0]
        assert call_args.path == "/api/entities/TestEntity"
        assert call_args.options["body"] == payload
        assert call_args.api == "entities.TestEntity.create"
        assert result == mock_response

    def test_create_many(self, entity_service, mock_client):
        """Test create_many method"""
        mock_response = BshResponse(
            data=[{"id": "1"}, {"id": "2"}],
            code=201,
            status="Created",
            timestamp=1234567890,
        )
        mock_client.post.return_value = mock_response

        payload = [{"name": "Entity1"}, {"name": "Entity2"}]
        result = entity_service.create_many(payload)

        assert mock_client.post.called
        call_args = mock_client.post.call_args[0][0]
        assert call_args.path == "/api/entities/TestEntity/batch"
        assert call_args.options["body"] == payload
        assert call_args.api == "entities.TestEntity.createMany"
        assert result == mock_response

    def test_update(self, entity_service, mock_client):
        """Test update method"""
        mock_response = BshResponse(
            data=[{"id": "1", "name": "Updated Entity"}],
            code=200,
            status="OK",
            timestamp=1234567890,
        )
        mock_client.put.return_value = mock_response

        payload = {"id": "1", "name": "Updated Entity"}
        result = entity_service.update(payload)

        assert mock_client.put.called
        call_args = mock_client.put.call_args[0][0]
        assert call_args.path == "/api/entities/TestEntity"
        assert call_args.options["body"] == payload
        assert call_args.api == "entities.TestEntity.update"
        assert result == mock_response

    def test_update_many(self, entity_service, mock_client):
        """Test update_many method"""
        mock_response = BshResponse(
            data=[{"id": "1"}, {"id": "2"}],
            code=200,
            status="OK",
            timestamp=1234567890,
        )
        mock_client.put.return_value = mock_response

        payload = [{"id": "1", "name": "Updated1"}, {"id": "2", "name": "Updated2"}]
        result = entity_service.update_many(payload)

        assert mock_client.put.called
        call_args = mock_client.put.call_args[0][0]
        assert call_args.path == "/api/entities/TestEntity/batch"
        assert call_args.options["body"] == payload
        assert call_args.api == "entities.TestEntity.updateMany"
        assert result == mock_response

    def test_search(self, entity_service, mock_client):
        """Test search method"""
        mock_response = BshResponse(
            data=[{"id": "1"}],
            code=200,
            status="OK",
            timestamp=1234567890,
        )
        mock_client.post.return_value = mock_response

        search = BshSearch(
            filters=[Filter(field="name", operator="eq", value="Test")],
            pagination=Pagination(page=1, size=10),
        )
        result = entity_service.search(search)

        assert mock_client.post.called
        call_args = mock_client.post.call_args[0][0]
        assert call_args.path == "/api/entities/TestEntity/search"
        assert call_args.api == "entities.TestEntity.search"
        assert result == mock_response

    def test_delete(self, entity_service, mock_client):
        """Test delete method"""
        mock_response = BshResponse(
            data=[{"effected": 5}],
            code=200,
            status="OK",
            timestamp=1234567890,
        )
        mock_client.post.return_value = mock_response

        search = BshSearch(filters=[], pagination=Pagination(page=1, size=10))
        result = entity_service.delete(search)

        assert mock_client.post.called
        call_args = mock_client.post.call_args[0][0]
        assert call_args.path == "/api/entities/TestEntity/delete"
        assert call_args.api == "entities.TestEntity.delete"
        assert result == mock_response

    def test_delete_by_id(self, entity_service, mock_client):
        """Test delete_by_id method"""
        mock_response = BshResponse(
            data=[{"effected": 1}],
            code=200,
            status="OK",
            timestamp=1234567890,
        )
        mock_client.delete.return_value = mock_response

        result = entity_service.delete_by_id(id="1")

        assert mock_client.delete.called
        call_args = mock_client.delete.call_args[0][0]
        assert call_args.path == "/api/entities/TestEntity/1"
        assert call_args.api == "entities.TestEntity.deleteById"
        assert result == mock_response

    def test_columns(self, entity_service, mock_client):
        """Test columns method"""
        mock_response = BshResponse(
            data=[{"name": "id", "type": "string"}, {"name": "name", "type": "string"}],
            code=200,
            status="OK",
            timestamp=1234567890,
        )
        mock_client.get.return_value = mock_response

        result = entity_service.columns()

        assert mock_client.get.called
        call_args = mock_client.get.call_args[0][0]
        assert call_args.path == "/api/entities/TestEntity/columns"
        assert call_args.api == "entities.TestEntity.columns"
        assert result == mock_response

    def test_count(self, entity_service, mock_client):
        """Test count method"""
        mock_response = BshResponse(
            data=[{"count": 42}],
            code=200,
            status="OK",
            timestamp=1234567890,
        )
        mock_client.get.return_value = mock_response

        result = entity_service.count()

        assert mock_client.get.called
        call_args = mock_client.get.call_args[0][0]
        assert call_args.path == "/api/entities/TestEntity/count"
        assert call_args.api == "entities.TestEntity.count"
        assert result == mock_response

    def test_count_filtered(self, entity_service, mock_client):
        """Test count_filtered method"""
        mock_response = BshResponse(
            data=[{"count": 15}],
            code=200,
            status="OK",
            timestamp=1234567890,
        )
        mock_client.post.return_value = mock_response

        search = BshSearch(
            filters=[Filter(field="name", operator="eq", value="Test")],
            pagination=Pagination(page=1, size=10),
        )
        result = entity_service.count_filtered(search)

        assert mock_client.post.called
        call_args = mock_client.post.call_args[0][0]
        assert call_args.path == "/api/entities/TestEntity/count"
        assert call_args.api == "entities.TestEntity.countBySearch"
        assert result == mock_response

    def test_export(self, entity_service, mock_client):
        """Test export method"""
        mock_client.download.return_value = b"test content"

        search = BshSearch(filters=[], pagination=Pagination(page=1, size=10))
        entity_service.export(search, format="csv")

        assert mock_client.download.called
        call_args = mock_client.download.call_args[0][0]
        assert "/api/entities/TestEntity/export" in call_args.path
        assert "format=csv" in call_args.path
        assert "filename=" in call_args.path

    def test_export_with_custom_filename(self, entity_service, mock_client):
        """Test export with custom filename"""
        mock_client.download.return_value = b"test"

        search = BshSearch(filters=[], pagination=Pagination(page=1, size=10))
        entity_service.export(search, format="json", filename="custom-export.json")

        call_args = mock_client.download.call_args[0][0]
        assert "filename=custom-export.json" in call_args.path

