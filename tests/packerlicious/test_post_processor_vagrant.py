import packerlicious.post_processor as post_processor


class TestVagrantPostProcessor(object):

    def test_no_required_fields(self):
        b = post_processor.Vagrant()

        b.to_dict()
