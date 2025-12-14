"""Entity service for CRUD operations"""
from typing import Optional, Any, Dict, List
from ..client import BshClient, BshClientFnParams
from ..types import BshResponse, BshSearch


class EntityService:
    """Service for entity operations"""

    def __init__(self, client: BshClient, entity: Optional[str] = None):
        self.client = client
        self.entity = entity
        self.base_endpoint = "/api/entities"

    def find_by_id(
        self,
        id: str,
        entity: Optional[str] = None,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Get a single entity by ID"""
        entity_name = entity or self.entity
        return self.client.get(
            BshClientFnParams(
                path=f"{self.base_endpoint}/{entity_name}/{id}",
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api=f"entities.{entity_name}.findById",
            )
        )

    def create(
        self,
        payload: Any,
        entity: Optional[str] = None,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Create a new entity"""
        entity_name = entity or self.entity
        return self.client.post(
            BshClientFnParams(
                path=f"{self.base_endpoint}/{entity_name}",
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "body": payload,
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api=f"entities.{entity_name}.create",
            )
        )

    def create_many(
        self,
        payload: List[Any],
        entity: Optional[str] = None,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Create multiple entities in batch"""
        entity_name = entity or self.entity
        return self.client.post(
            BshClientFnParams(
                path=f"{self.base_endpoint}/{entity_name}/batch",
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "body": payload,
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api=f"entities.{entity_name}.createMany",
            )
        )

    def update(
        self,
        payload: Any,
        entity: Optional[str] = None,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Update an existing entity"""
        entity_name = entity or self.entity
        return self.client.put(
            BshClientFnParams(
                path=f"{self.base_endpoint}/{entity_name}",
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "body": payload,
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api=f"entities.{entity_name}.update",
            )
        )

    def update_many(
        self,
        payload: List[Any],
        entity: Optional[str] = None,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Update multiple entities in batch"""
        entity_name = entity or self.entity
        return self.client.put(
            BshClientFnParams(
                path=f"{self.base_endpoint}/{entity_name}/batch",
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "body": payload,
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api=f"entities.{entity_name}.updateMany",
            )
        )

    def search(
        self,
        payload: BshSearch,
        entity: Optional[str] = None,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Search for entities"""
        entity_name = entity or self.entity
        search_dict = payload.to_dict() if hasattr(payload, "to_dict") else payload
        return self.client.post(
            BshClientFnParams(
                path=f"{self.base_endpoint}/{entity_name}/search",
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "body": search_dict,
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api=f"entities.{entity_name}.search",
            )
        )

    def delete(
        self,
        payload: BshSearch,
        entity: Optional[str] = None,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Delete entities by search criteria"""
        entity_name = entity or self.entity
        search_dict = payload.to_dict() if hasattr(payload, "to_dict") else payload
        return self.client.post(
            BshClientFnParams(
                path=f"{self.base_endpoint}/{entity_name}/delete",
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "body": search_dict,
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api=f"entities.{entity_name}.delete",
            )
        )

    def delete_by_id(
        self,
        id: str,
        entity: Optional[str] = None,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Delete a single entity by ID"""
        entity_name = entity or self.entity
        return self.client.delete(
            BshClientFnParams(
                path=f"{self.base_endpoint}/{entity_name}/{id}",
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api=f"entities.{entity_name}.deleteById",
            )
        )

    def columns(
        self,
        entity: Optional[str] = None,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Get entity columns"""
        entity_name = entity or self.entity
        return self.client.get(
            BshClientFnParams(
                path=f"{self.base_endpoint}/{entity_name}/columns",
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api=f"entities.{entity_name}.columns",
            )
        )

    def count(
        self,
        entity: Optional[str] = None,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Count entities"""
        entity_name = entity or self.entity
        return self.client.get(
            BshClientFnParams(
                path=f"{self.base_endpoint}/{entity_name}/count",
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api=f"entities.{entity_name}.count",
            )
        )

    def count_filtered(
        self,
        payload: BshSearch,
        entity: Optional[str] = None,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Count entities with search criteria"""
        entity_name = entity or self.entity
        search_dict = payload.to_dict() if hasattr(payload, "to_dict") else payload
        return self.client.post(
            BshClientFnParams(
                path=f"{self.base_endpoint}/{entity_name}/count",
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "body": search_dict,
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api=f"entities.{entity_name}.countBySearch",
            )
        )

    def export(
        self,
        payload: BshSearch,
        format: str = "csv",
        filename: Optional[str] = None,
        entity: Optional[str] = None,
        on_download: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> None:
        """Export entities"""
        entity_name = entity or self.entity
        from datetime import date
        default_name = f"{entity_name}_export_{date.today().isoformat()}"
        export_filename = filename or f"{default_name}.{format if format != 'excel' else 'xlsx'}"
        
        search_dict = payload.to_dict() if hasattr(payload, "to_dict") else payload
        
        self.client.download(
            BshClientFnParams(
                path=f"{self.base_endpoint}/{entity_name}/export?format={format}&filename={export_filename}",
                options={
                    "response_type": "blob",
                    "request_format": "json",
                    "body": search_dict,
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_download": on_download, "on_error": on_error},
                api=f"entities.{entity_name}.export",
            )
        )

