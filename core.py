from functools import wraps
from typing import Callable, Union, cast

from rx.core.typing import Disposable
from rx.subject.subject import Subject

import jsonpointer as jp
import rx.operators as ops


class ObsMixin:

    _mutators: tuple[str] = tuple()

    @classmethod
    def _mutator(cls, fn: Callable):

        @wraps(fn)
        def _fn(obj: ObsMixin, *args, **kwargs):
            prev = obj.copy()

            value = fn(obj, *args, **kwargs)

            obj._update(prev)
            obj._notify()

            return value

        return _fn

    def __new__(cls, *args, **kwargs):
        for method_name in cls._mutators:
            setattr(cls, method_name, cls._mutator(
                getattr(super(), method_name)))

        return super().__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._subject = Subject()
        self.subscribe = self._subject.subscribe
        self.pipe = self._subject.pipe

        self._disposers: list[Disposable] = list()

        self._update(None)
        self._notify()

    def _notify(self):
        self._subject.on_next(self)

    def _update(self, prev):
        if prev is None or self != prev:
            for disposer in self._disposers:
                disposer.dispose()

            self._disposers = [value.subscribe(lambda _: self._notify())
                               for value in self.values()
                               if isinstance(value, ObsMixin)]

    def copy(self):
        return type(self)(cast(Union[dict, list, set], super()).copy())

    def __repr__(self) -> str:
        # set in CPython is hardcoded to print the class name if class isn't
        # exactly a set
        if isinstance(self, set):
            return super().__repr__()

        return f'{self.__class__.__name__}({super().__repr__()})'


def observe_path(obj: ObsMixin, path: str):

    def resolve(doc: ObsMixin):
        return jp.resolve_pointer(doc, path, None)

    return obj.pipe(ops.map(resolve), ops.distinct_until_changed())
