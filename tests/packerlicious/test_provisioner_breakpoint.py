import packerlicious.provisioner as provisioner


class TestBreakpointProvisioner(object):

    def test_no_required_fields(self):
        b = provisioner.Breakpoint()

        b.to_dict()
