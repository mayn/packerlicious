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

    def __str__(self):
        return "Output: " + str(self.output) + \
                "\nReturn code: " + str(self.return_code) + \
                "\nError: " + str(self.error) + "\n"

CLEAN_UP = 1
ABORT    = 2

def check_available(packer_path):
    """
    Check if packer binary is available.
    Raises ValueError if not.
    """
    try:
        subprocess.Popen(packer_path + "packer", stdout=subprocess.PIPE)
    except OSError:
        raise ValueError("Packer Binary not available...")

def run_command(command, template):
    command += " - "
    proc = subprocess.Popen(shlex.split(command), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    proc.stdin.write(template.to_json())
    out, err = proc.communicate()
    return PackerOutput(proc.returncode, out, err)

def validate(template, syntax_only=False, _except=None, only=None, packer_path=""):
    """
    Validate template.
    Returns (Return Code, Output)
    """
    if len(packer_path) > 0 and packer_path[-1] != '/':
        packer_path += '/'
    check_available(packer_path)
    validate_command = packer_path + "packer validate "
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
    return run_command(validate_command, template)

def build(template, debug=False, _except=None, only=None, force=False, 
        machine_readable=False, on_error=CLEAN_UP, parellel=True, packer_path=""):
    """
    Execute build
    Returns (Return Code, Output)
    """
    if len(packer_path) > 0 and packer_path[-1] != '/':
        packer_path += '/'
    check_available(packer_path)
    build_command = packer_path + "packer build "
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
    if on_error == ABORT:
        build_command += "-on-error=abort "
    if not parellel:
        build_command += "-parallel=false "
    return run_command(build_command, template)

def inspect(template, machine_readable=False, packer_path=""):
    """
    Inspect template
    Returns (Return Code, Output)
    """
    if len(packer_path) > 0 and packer_path[-1] != '/':
        packer_path += '/'
    check_available(packer_path)
    inspect_command = packer_path + "packer inspect "
    if machine_readable:
        inspect_command += "-machine-readable "
    return run_command(inspect_command, template)

def push(template, name=None, token=None, sensitive=None, packer_path=""):
    """
    Push template to build service
    Returns (Return Code, Output)
    """
    if len(packer_path) > 0 and packer_path[-1] != '/':
        packer_path += '/'
    check_available(packer_path)
    push_command = packer_path + "packer push "
    if name is not None:
        push_command += "-name=\"" + name + "\" "
    if token is not None:
        push_command += "-token=\"" + token + "\" "
    if sensitive is not None:
        push_command += "-sensitive="
        for s in sensitive:
            push_command += s + ","
        push_command += " "
    return run_command(push_command, template)
