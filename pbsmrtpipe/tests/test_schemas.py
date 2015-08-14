import json
import logging
import unittest

from pbsmrtpipe.schemas import validate_pipeline_template

from base import get_data_file

log = logging.getLogger(__name__)


class TestPipelinTemplate(unittest.TestCase):
    def test_01(self):
        file_name = 'example_pipeline_template_01.json'
        path = get_data_file(file_name)

        with open(path, 'r') as f:
            d = json.loads(f.read())

        is_valid = validate_pipeline_template(d)
        self.assertTrue(is_valid, "pipeline template {p} is NOT valid.".format(p=path))