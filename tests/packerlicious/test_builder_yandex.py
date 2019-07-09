import pytest

import packerlicious.builder as builder


class TestYandexBuilder(object):

    def test_no_required_fields(self):
        b = builder.Yandex()

        b.to_dict()
