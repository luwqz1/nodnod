import inspect
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, cast, dataclass_transform

from nodnod.node import Node
from nodnod.utils.create_node import create_node


@dataclass_transform(field_specifiers=(field,))
def node_pack[T](cls: type[T], /) -> type[T]:
    new_node = create_node(
        name=cls.__name__,
        base_node=PackNode,
        bases=(cls,),
        namespace=dict(vars(cls)),
    )
    return cast("type[T]", new_node)


class PackNode(Node, abstract=True):
    def __init_subclass__(cls) -> None:
        dataclass(cls)

        @(lambda compose: setattr(cls, "__compose__", compose))
        @wraps(wrapped=cls.__init__, assigned=("__module__", "__doc__", "__annotate__", "__type_params__"))
        @(lambda compose: setattr(compose, "__signature__", inspect.signature(cls).replace(return_annotation=cls)) or compose)
        def __compose__(*args: Any, **kwargs: Any) -> Any:  # noqa
            instance = object.__new__(cls)
            instance.__init__(*args, **kwargs)
            return instance

        super().__init_subclass__()


__all__ = ("node_pack",)
