from . import PackerBuilder
from ..validator import mutually_exclusive
import warnings


class File(PackerBuilder):
    """
    File Builder
    https://www.packer.io/docs/builders/file.html
    """
    resource_type = "file"

    props = {
        'target': (basestring, True),
        'source': (basestring, False),
        'content': (basestring, False),
    }

    def validate(self):

        conds = [
            'source',
            'content',
        ]
        specified_count = mutually_exclusive(self.__class__.__name__, self.properties, conds)
        if specified_count == 0:
            warnings.warn("Both source and content not specified, artifact will be empty.")
