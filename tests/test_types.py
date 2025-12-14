"""Tests for type definitions"""
import pytest
from bshengine import BshResponse, BshError, is_ok, BshSearch, Filter, Pagination, Sort, GroupBy, Aggregate


class TestBshResponse:
    """Test BshResponse class"""

    def test_from_dict(self):
        """Test creating BshResponse from dictionary"""
        data = {
            "data": [{"id": 1}],
            "timestamp": 1234567890,
            "code": 200,
            "status": "OK",
            "error": None,
        }
        response = BshResponse.from_dict(data)
        
        assert response.data == [{"id": 1}]
        assert response.timestamp == 1234567890
        assert response.code == 200
        assert response.status == "OK"
        assert response.error is None

    def test_from_dict_with_optional_fields(self):
        """Test creating BshResponse with optional fields"""
        data = {
            "data": [],
            "timestamp": 1234567890,
            "code": 200,
            "status": "OK",
            "error": "Some error",
            "meta": {"type": "test"},
            "pagination": {"current": 1, "total": 10},
            "validations": [{"field": "email", "error": "Invalid"}],
        }
        response = BshResponse.from_dict(data)
        
        assert response.error == "Some error"
        assert response.meta == {"type": "test"}
        assert response.pagination == {"current": 1, "total": 10}
        assert response.validations == [{"field": "email", "error": "Invalid"}]


class TestBshError:
    """Test BshError class"""

    def test_constructor(self):
        """Test BshError constructor"""
        response = BshResponse(
            data=[],
            code=404,
            status="Not Found",
            timestamp=1234567890,
        )
        error = BshError(404, "/test", response)
        
        assert error.status == 404
        assert error.endpoint == "/test"
        assert error.response == response
        assert error.response.endpoint == "/test"
        assert str(error) is not None

    def test_constructor_without_response(self):
        """Test BshError constructor without response"""
        error = BshError(500, "/test")
        
        assert error.status == 500
        assert error.endpoint == "/test"
        assert error.response is None


class TestIsOk:
    """Test is_ok function"""

    def test_is_ok_with_success_response(self):
        """Test is_ok with successful response"""
        response = BshResponse(
            data=[],
            code=200,
            status="OK",
            timestamp=1234567890,
        )
        assert is_ok(response) is True

    def test_is_ok_with_error_response(self):
        """Test is_ok with error response"""
        response = BshResponse(
            data=[],
            code=404,
            status="Not Found",
            timestamp=1234567890,
        )
        assert is_ok(response) is False

    def test_is_ok_with_none(self):
        """Test is_ok with None"""
        assert is_ok(None) is False


class TestBshSearch:
    """Test BshSearch class"""

    def test_to_dict_basic(self):
        """Test BshSearch to_dict with basic fields"""
        search = BshSearch(
            entity="TestEntity",
            alias="t",
            fields=["id", "name"],
        )
        result = search.to_dict()
        
        assert result["entity"] == "TestEntity"
        assert result["alias"] == "t"
        assert result["fields"] == ["id", "name"]

    def test_to_dict_with_filters(self):
        """Test BshSearch to_dict with filters"""
        search = BshSearch(
            filters=[
                Filter(field="name", operator="eq", value="Test"),
                Filter(field="age", operator="gt", value=18),
            ]
        )
        result = search.to_dict()
        
        assert "filters" in result
        assert len(result["filters"]) == 2
        assert result["filters"][0]["field"] == "name"
        assert result["filters"][0]["operator"] == "eq"
        assert result["filters"][0]["value"] == "Test"

    def test_to_dict_with_nested_filters(self):
        """Test BshSearch to_dict with nested filters"""
        search = BshSearch(
            filters=[
                Filter(
                    operator="and",
                    filters=[
                        Filter(field="name", operator="eq", value="Test"),
                        Filter(field="status", operator="eq", value="active"),
                    ],
                )
            ]
        )
        result = search.to_dict()
        
        assert "filters" in result
        assert result["filters"][0]["operator"] == "and"
        assert "filters" in result["filters"][0]
        assert len(result["filters"][0]["filters"]) == 2

    def test_to_dict_with_pagination(self):
        """Test BshSearch to_dict with pagination"""
        search = BshSearch(
            pagination=Pagination(page=2, size=20)
        )
        result = search.to_dict()
        
        assert "pagination" in result
        assert result["pagination"]["page"] == 2
        assert result["pagination"]["size"] == 20

    def test_to_dict_with_sort(self):
        """Test BshSearch to_dict with sort"""
        search = BshSearch(
            sort=[
                Sort(field="name", direction=1),
                Sort(field="created", direction=-1),
            ]
        )
        result = search.to_dict()
        
        assert "sort" in result
        assert len(result["sort"]) == 2
        assert result["sort"][0]["field"] == "name"
        assert result["sort"][0]["direction"] == 1

    def test_to_dict_with_group_by(self):
        """Test BshSearch to_dict with group by"""
        search = BshSearch(
            group_by=GroupBy(
                fields=["category"],
                aggregate=[
                    Aggregate(function="COUNT", field="id", alias="total"),
                    Aggregate(function="SUM", field="price", alias="total_price"),
                ]
            )
        )
        result = search.to_dict()
        
        assert "groupBy" in result
        assert result["groupBy"]["fields"] == ["category"]
        assert len(result["groupBy"]["aggregate"]) == 2
        assert result["groupBy"]["aggregate"][0]["function"] == "COUNT"

    def test_to_dict_with_from(self):
        """Test BshSearch to_dict with from clause"""
        inner_search = BshSearch(entity="InnerEntity")
        search = BshSearch(from_=inner_search)
        result = search.to_dict()
        
        assert "from" in result
        assert result["from"]["entity"] == "InnerEntity"

