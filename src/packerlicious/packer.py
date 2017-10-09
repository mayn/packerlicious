import subprocess
import shlex
import os
import tempfile
from packerlicious.template import Template

class PackerOutput(object):
    """
    Output of Packer command
    """
    
    def __init__(self, return_code, output, error):
        self.return_code = return_code
        self.output = output
        self.error = error

class Packer(object):
    """
    Packer Binary Wrapper
    """

    CLEAN_UP = 1
    ABORT    = 2

    packer_path = ""
    template = None

    def __init__(self, template, packer_path=""):
        if len(packer_path) > 0 and packer_path[-1] != '/':
            packer_path += "/"
        self.packer_path = packer_path
        self.template = template
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

    def run_command(self, command):
        template_file, template_filename = tempfile.mkstemp()
        os.write(template_file, self.template.to_json())
        os.close(template_file)
        command += template_filename
        proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
        out, err = proc.communicate()
        os.remove(template_filename)
        return PackerOutput(proc.returncode, out, err)

    def validate(self, syntax_only=False, _except=None, only=None):
        """
        Validate template.
        Returns (Return Code, Output)
        """
        self.check_available()
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
        return self.run_command(validate_command)

    def build(self, debug=False, _except=None, only=None, force=False, 
            machine_readable=False, on_error=CLEAN_UP, parellel=True):
        """
        Execute build
        Returns (Return Code, Output)
        """
        self.check_available()
        build_command = self.packer_path + "packer build "
        if debug:
            build_command += "-debug "
        if _except is not None:
            build_command += "-except="
            for e in _except:
                build_command += e + ","
            build_command += " "
        if only is not None:
            build_command += "-only="
            for o in only:
                build_command += o + ","
            build_command += " "
        if force:
            build_command += "-force "
        if machine_readable:
            build_command += "-machine_readable "
        if on_error == Packer.ABORT:
            build_command += "-on-error=abort "
        if not parellel:
            build_command += "-parallel=false "
        return self.run_command(build_command)

    def inspect(self, machine_readable=False):
        """
        Inspect template
        Returns (Return Code, Output)
        """
        self.check_available()
        inspect_command = self.packer_path + "packer inspect "
        if machine_readable:
            inspect_command += "-machine-readable "
        return self.run_command(inspect_command)

    def push(self, name=None, token=None, sensitive=None):
        """
        Push template to build service
        Returns (Return Code, Output)
        """
        self.check_available()
        push_command = self.packer_path + "packer push "
        if name is not None:
            push_command += "-name=\"" + name + "\" "
        if token is not None:
            push_command += "-token=\"" + token + "\" "
        if sensitive is not None:
            push_command += "-sensitive="
            for s in sensitive:
                push_command += s + ","
            push_command += " "
        return self.run_command(push_command)


        

