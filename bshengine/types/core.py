"""Core domain types"""
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field

# These are placeholder types - in a real implementation,
# you'd define them based on your actual API schema
BshUser = Dict[str, Any]
BshUserInit = Dict[str, Any]
BshEntities = Dict[str, Any]
BshSchemas = Dict[str, Any]
BshTypes = Dict[str, Any]
BshPolicy = Dict[str, Any]
BshRole = Dict[str, Any]
BshEmailTemplate = Dict[str, Any]
BshEventLogs = Dict[str, Any]
SentEmail = Dict[str, Any]
BshTrigger = Dict[str, Any]
BshTriggerInstance = Dict[str, Any]
BshFiles = Dict[str, Any]
BshConfigurations = Dict[str, Any]
BshSettings = Dict[str, Any]
BshApiKeys = Dict[str, Any]
BshApiKeysForm = Dict[str, Any]
UploadResponse = Dict[str, Any]
UploadOptions = Dict[str, Any]
MailingPayload = Dict[str, Any]
CacheInfo = Dict[str, Any]
BshTriggerPlugin = Dict[str, Any]
BshTriggerAction = Dict[str, Any]

