#!/usr/bin/env python3
#
# Copyright 2021 Graviti. Licensed under MIT License.
#

"""Common_loads method, EqMixin class.

:meth:`common_loads` is a common method for loading an object from a dict or a list of dict.

:class:`EqMixin` is a mixin class to support __eq__() method,
which compares all the instance variables.

"""

import warnings
from functools import wraps
from typing import Any, Callable, Optional, Sequence, Tuple, Type, TypeVar, Union

import numpy as np

_T = TypeVar("_T")
MatrixType = Union[Sequence[Sequence[float]], np.ndarray]


def common_loads(object_class: Type[_T], contents: Any) -> _T:
    """A common method for loading an object from a dict or a list of dict.

    Arguments:
        object_class: The class of the object to be loaded.
        contents: The information of the object in a dict or a list of dict.

    Returns:
        The loaded object.

    """
    obj: _T = object.__new__(object_class)
    obj._loads(contents)  # type: ignore[attr-defined]  # pylint: disable=protected-access
    return obj


class EqMixin:  # pylint: disable=too-few-public-methods
    """A mixin class to support __eq__() method.

    The __eq__() method defined here compares all the instance variables.

    """

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False

        return self.__dict__ == other.__dict__


_Callable = TypeVar("_Callable", bound=Callable[..., Any])


class Deprecated:  # pylint: disable=too-few-public-methods
    """A decorator for deprecated functions.

    Arguments:
        since: The version the function is deprecated.
        remove_in: The version the function will be removed in.
        substitute: The substitute function.

    """

    def __init__(
        self, *, since: str, removed_in: Optional[str] = None, substitute: Optional[str] = None
    ) -> None:
        self._since = since
        self._removed_in = removed_in
        self._substitute = substitute

    def __call__(self, func: _Callable) -> _Callable:
        """Wrap the decorated function by adding the deprecated message.

        Arguments:
            func: The deprecated function.

        Returns:
            The wrapped function which shows the deprecated message when calling.

        """
        messages = [f'Function "{func.__name__}" is deprecated since version {self._since}.']
        if self._removed_in:
            messages.append(f'It will be removed in version "{self._removed_in}".')

        if self._substitute:
            messages.append(f'Use "{self._substitute}" instead.')

        message = " ".join(messages)

        @wraps(func)
        def wrapper(*arg: Any, **kwargs: Any) -> Any:
            warnings.warn(message, DeprecationWarning, 2)

            return func(*arg, **kwargs)

        wrapper.__doc__ = self._update_docstring(wrapper.__doc__)

        return wrapper  # type: ignore[return-value]

    def _update_docstring(self, docstring: Optional[str]) -> str:
        insert_block = [f".. deprecated:: {self._since}"]
        if self._removed_in:
            insert_block.append(f"   Will be removed in version {self._removed_in}.")
        if self._substitute:
            insert_block.append(f"   Use :meth:`{self._substitute}` instead.")

        if not docstring:
            return "\n".join(insert_block)

        lines = docstring.splitlines()

        indent = ""
        for line in lines[1:]:
            if line:
                indent = line[: -len(line.lstrip())]
                break

        lines[1:1] = (f"{indent}{message}" for message in insert_block)
        lines.insert(1, "")

        return "\n".join(lines)


class KwargsDeprecated:  # pylint: disable=too-few-public-methods
    """A decorator for the function which has deprecated keyword arguments.

    Arguments:
        keywords: The keyword arguments which need to be deprecated.
        since: The version the keyword arguments are deprecated.
        remove_in: The version the keyword arguments will be removed in.
        substitute: The substitute usage.

    """

    def __init__(
        self,
        keywords: Tuple[str, ...],
        *,
        since: str,
        removed_in: Optional[str] = None,
        substitute: Optional[str] = None,
    ) -> None:
        self._keywords = keywords
        self._since = since
        self._removed_in = removed_in
        self._substitute = substitute

    def __call__(self, func: _Callable) -> _Callable:
        """Wrap the decorated function by adding the deprecated message.

        Arguments:
            func: The deprecated function.

        Returns:
            The wrapped function which shows the deprecated message when calling.

        """
        keywords = tuple(f'"{keyword}"' for keyword in self._keywords)
        if len(keywords) == 1:
            keyword_message = keywords[0]
            argument = "argument"
            be = "is"  # pylint: disable=invalid-name
        else:
            keyword_message = f"{' '.join(keywords[:-1])} and {keywords[-1]}"
            argument = "arguments"
            be = "are"  # pylint: disable=invalid-name

        messages = [
            (
                f'The keyword {argument}: {keyword_message} in "{func.__name__}" '
                f"{be} deprecated since version {self._since}."
            )
        ]
        if self._removed_in:
            messages.append(f'Will be removed in version "{self._removed_in}".')

        if self._substitute:
            messages.append(f'Use "{self._substitute}" instead.')

        message = " ".join(messages)

        @wraps(func)
        def wrapper(*arg: Any, **kwargs: Any) -> Any:
            if set(self._keywords) & kwargs.keys():
                warnings.warn(message, DeprecationWarning, 2)

            return func(*arg, **kwargs)

        return wrapper  # type: ignore[return-value]
