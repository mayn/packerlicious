import subprocess
import shlex
import os
import tempfile
from packerlicious.template import Template

class Packer(object):
    """
    Packer Binary Wrapper
    """

    packer_path = ""
    template = None
    _vars = {}

    def __init__(self, template=None, _vars={}, packer_path=""):
        if len(packer_path) > 0 and packer_path[-1] != '/':
            packer_path += "/"
        self.packer_path = packer_path
        self.template = template
        self._vars = _vars
        self.check_available()

    def check_available(self):
        """
        Check if packer binary is available.
        Raises ValueError if not.
        """
        try:
            subprocess.Popen(self.packer_path + "packer", stdout=subprocess.PIPE)
        except OSError:
            raise ValueError("Packer Binary not available...")

    def add_template(self, template):
        self.template = template
    
    def add_var(self, var):
        self._vars.update(var)
    
    def add_vars(self, _vars):
        self._vars = _vars

    def validate(self, syntax_only=False, _except=None, only=None):
        """
        Validate template.
        Returns (Return Code, Output)
        """
        self.check_available()
        if self.template is None:
            raise ValueError("No template provided...")
        validate_command = self.packer_path + "packer validate "
        if syntax_only:
            validate_command += "-syntax_only "
        if _except is not None:
            validate_command += "-except="
            for e in _except:
                validate_command += e + ","
            validate_command += " "
        if only is not None:
            validate_command += "-only="
            for o in only:
                validate_command += o + ","
            validate_command += " "
        for key in self._vars:
            validate_command += "-var '" + key + "=" + self._vars[key] + "' "
        template_file, template_filename = tempfile.mkstemp()
        os.write(template_file, self.template.to_json())
        os.close(template_file)
        validate_command += template_filename
        proc = subprocess.Popen(shlex.split(validate_command), stdout=subprocess.PIPE)
        out = proc.communicate()[0]
        os.remove(template_filename)
        return proc.returncode, out