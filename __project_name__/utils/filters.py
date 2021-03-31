from typing import Type, Optional, Dict, Tuple

from pydantic import BaseModel

from __project_name__.base.schemas import BaseOutputSchema, BaseListSchema


def get_schema(query_string: dict,
               schema_cls: Type[BaseOutputSchema],
               relationships: Dict[str, Tuple[BaseModel, ...]] = None,
               many: bool = False) -> Type[BaseOutputSchema]:

    embed = query_string.get('embed')

    if embed and relationships:

        relations = {}

        for rel in embed.split(','):
            if rel in relationships:
                relations[rel] = relationships[rel]

        if relations:
            schema_cls = schema_cls.add_fields(**relations)

    if many:
        return BaseListSchema[schema_cls]

    return schema_cls


def get_fields(query_string: dict) -> Optional[Dict[str, Optional[dict]]]:

    fields = query_string.get('fields')

    if not fields:
        return None

    return {k: ... for k in fields.split(",")}
