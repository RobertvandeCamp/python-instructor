"""Utilities for JSON serialization and deserialization with complex types."""

import json
import uuid
from datetime import datetime, date
from typing import Any, Dict, Type, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class JsonEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles UUID and other complex types."""
    
    def default(self, obj: Any) -> Any:
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, BaseModel):
            return obj.model_dump()
        return super().default(obj)

def dumps(obj: Any) -> str:
    """Serialize obj to a JSON formatted string using the custom encoder."""
    return json.dumps(obj, cls=JsonEncoder)

def loads(json_str: str) -> Any:
    """Deserialize json_str to a Python object."""
    return json.loads(json_str)

def model_to_dict(model: BaseModel) -> Dict:
    """Convert a Pydantic model to a dict with proper type conversions."""
    # First get the dict from the model
    data_dict = model.model_dump()
    
    # Then manually process fields that need custom serialization
    for key, value in list(data_dict.items()):
        if isinstance(value, uuid.UUID):
            data_dict[key] = str(value)
        elif isinstance(value, (datetime, date)):
            data_dict[key] = value.isoformat()
    
    return data_dict

def dict_to_model(data: Dict, model_class: Type[T]) -> T:
    """Convert a dict to a Pydantic model."""
    return model_class.model_validate(data) 