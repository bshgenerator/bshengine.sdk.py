"""Image service"""
from typing import Optional, Any
from ..client import BshClient, BshClientFnParams
from ..types import BshResponse


class ImageService:
    """Service for image operations"""

    def __init__(self, client: BshClient):
        self.client = client
        self.base_endpoint = "/api/images"

    def upload(
        self,
        file_path: str,
        namespace: Optional[str] = None,
        asset_id: Optional[str] = None,
        options: Optional[dict] = None,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Upload image"""
        import os
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            data = {}
            if namespace:
                data["namespace"] = namespace
            if asset_id:
                data["assetId"] = asset_id
            if options:
                import json
                data["options"] = json.dumps(options)
            
            return self.client.post(
                BshClientFnParams(
                    path=f"{self.base_endpoint}/upload",
                    options={
                        "response_type": "json",
                        "request_format": "form",
                        "body": {"files": files, "data": data},
                    },
                    bsh_options={"on_success": on_success, "on_error": on_error},
                    api="image.upload",
                )
            )

