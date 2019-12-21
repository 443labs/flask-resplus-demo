from datetime import datetime, date
from decimal import Decimal
from json import JSONEncoder
from uuid import UUID


def monkey_patch_json_encoder():
    _encoder_default = JSONEncoder.default

    def _better_encoder_default(self, o):
        if isinstance(o, Decimal) or isinstance(o, UUID):
            return str(o)

        if isinstance(o, datetime) or isinstance(o, date):
            return o.isoformat()

        return _encoder_default(self, o)

    JSONEncoder.default = _better_encoder_default
