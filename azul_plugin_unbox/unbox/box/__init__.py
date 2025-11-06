"""Package for unboxing various archive/compression/packing formats."""

from abc import ABCMeta

from azul_plugin_unbox.unbox.box_base import Box


def _get_boxes():
    import importlib
    import os

    for filename in os.listdir(os.path.dirname(__file__)):
        if not (filename.startswith("box_") and filename.endswith(".py")):
            continue
        box_module_name = os.path.splitext(filename)[0]

        box_module = importlib.import_module("azul_plugin_unbox.unbox.box.%s" % box_module_name)
        for k in dir(box_module):
            v = getattr(box_module, k)
            if type(v) is not ABCMeta:
                continue

            if issubclass(v, Box):
                yield (v.__name__, v)
                break


class _Boxes(dict):
    """Dict like object to store boxname to boxclass mappings.

    Keys are forced to lowercase and all lookups are then performed as case insensitive.

    This is written for backwards compatibility, rather than just inserting the
    box keys in as lower to begin with.
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.update(*args, **kwargs)

    def __setitem__(self, key, value):
        dict.__setitem__(self, key.lower(), value)

    def __getitem__(self, key):
        return dict.__getitem__(self, key.lower())

    def __contains__(self, item):
        return dict.__contains__(self, item.lower())

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, dict.__repr__(self))

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v

    def get(self, k, d=None):
        k = k.lower()
        return dict.get(self, k, d)

    def setdefault(self, k, d=None):
        k = k.lower()
        return dict.setdefault(self, k, d)


box = _Boxes(_get_boxes())
box.__dict__.update(box)
locals().update(_get_boxes())
