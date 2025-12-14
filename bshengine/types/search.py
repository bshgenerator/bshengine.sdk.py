"""Search and filter types"""
from typing import Optional, List, Union, Literal, Any
from dataclasses import dataclass, field

LogicalOperator = Literal["and", "or", "AND", "OR"]
ComparisonOperator = Literal[
    "eq", "ne", "gt", "gte", "lt", "lte",
    "like", "ilike", "contains", "icontains",
    "starts", "istarts", "in", "nin", "between",
    "isnull", "notnull",
    "EQ", "NE", "GT", "GTE", "LT", "LTE",
    "LIKE", "ILIKE", "CONTAINS", "ICONTAINS",
    "STARTS", "ISTARTS", "IN", "NIN", "BETWEEN",
    "ISNULL", "NOTNULL",
]
AggregateFunction = Literal["COUNT", "SUM", "AVG", "MIN", "MAX"]


@dataclass
class Filter:
    """Filter criteria for search"""
    operator: Optional[Union[ComparisonOperator, LogicalOperator]] = None
    field: Optional[str] = None
    value: Optional[Any] = None
    type: Optional[str] = None
    filters: Optional[List["Filter"]] = None


@dataclass
class Aggregate:
    """Aggregation function"""
    function: Optional[AggregateFunction] = None
    field: Optional[str] = None
    alias: Optional[str] = None


@dataclass
class GroupBy:
    """Group by configuration"""
    fields: Optional[List[str]] = None
    aggregate: Optional[List[Aggregate]] = None


@dataclass
class Sort:
    """Sort configuration"""
    field: Optional[str] = None
    direction: Optional[Literal[-1, 1]] = None


@dataclass
class Pagination:
    """Pagination configuration"""
    page: Optional[int] = None
    size: Optional[int] = None


@dataclass
class BshSearch:
    """Search query structure"""
    entity: Optional[str] = None
    alias: Optional[str] = None
    fields: Optional[Union[str, List[str]]] = None
    filters: Optional[List[Filter]] = None
    group_by: Optional[GroupBy] = None
    sort: Optional[List[Sort]] = None
    pagination: Optional[Pagination] = None
    from_: Optional["BshSearch"] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        result = {}
        if self.entity:
            result["entity"] = self.entity
        if self.alias:
            result["alias"] = self.alias
        if self.fields:
            result["fields"] = self.fields
        if self.filters:
            result["filters"] = [
                self._filter_to_dict(f) for f in self.filters
            ]
        if self.group_by:
            result["groupBy"] = self._group_by_to_dict(self.group_by)
        if self.sort:
            result["sort"] = [
                {"field": s.field, "direction": s.direction}
                for s in self.sort
            ]
        if self.pagination:
            result["pagination"] = {
                "page": self.pagination.page,
                "size": self.pagination.size,
            }
        if self.from_:
            result["from"] = self.from_.to_dict()
        return result

    def _filter_to_dict(self, f: Filter) -> dict:
        """Convert filter to dictionary"""
        result = {}
        if f.operator:
            result["operator"] = f.operator
        if f.field:
            result["field"] = f.field
        if f.value is not None:
            result["value"] = f.value
        if f.type:
            result["type"] = f.type
        if f.filters:
            result["filters"] = [self._filter_to_dict(sub_f) for sub_f in f.filters]
        return result

    def _group_by_to_dict(self, gb: GroupBy) -> dict:
        """Convert group by to dictionary"""
        result = {}
        if gb.fields:
            result["fields"] = gb.fields
        if gb.aggregate:
            result["aggregate"] = [
                {
                    "function": a.function,
                    "field": a.field,
                    "alias": a.alias,
                }
                for a in gb.aggregate
            ]
        return result

