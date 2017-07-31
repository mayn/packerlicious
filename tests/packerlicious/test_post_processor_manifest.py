import packerlicious.post_processor as post_processor


class TestManifestPostProcessor(object):

    def test_no_required_fields(self):
        b = post_processor.Manifest()

        b.to_dict()
