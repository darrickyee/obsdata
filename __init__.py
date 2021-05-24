from typing import Any, Callable
import jsonpointer as jp
from rx.core.typing import Mapper
import rx.operators as ops

from .obsdict import ObsDict
from .obslist import ObsList
from .obsset import ObsSet


def observe_path(obj: ObsDict, path: str):

    def resolve(doc: ObsDict) -> Any:
        return jp.resolve_pointer(doc, path, None)

    return obj.pipe(ops.map(resolve), ops.distinct_until_changed())
