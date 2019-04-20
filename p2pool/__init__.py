import os
import re
import sys
import traceback
import subprocess
import binascii

def check_output(*popenargs, **kwargs):
    process = subprocess.Popen(stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        raise ValueError((retcode, output))
    return output

def _get_version():
    ret = None
    dir_name = __loader__.path
    try:
        ret = check_output(['git', 'describe', '--always', '--dirty'],
                cwd=os.path.dirname(os.path.abspath(sys.argv[0]))
                ).strip().decode('ascii')
    except:
        pass
    try:
        ret = check_output(['git.cmd', 'describe', '--always', '--dirty'],
                cwd=os.path.dirname(os.path.abspath(sys.argv[0]))
                ).strip().decode('ascii')
    except:
        pass

    cur_ver = None
    ver_file = '%s/VERSION' % os.path.dirname(os.path.dirname(dir_name))
    try:
        with open(ver_file, 'r', encoding='UTF-8') as fh:
            cur_ver = fh.read().strip()
    except FileNotFoundError:
        pass

    if ret is not None and cur_ver != ret:
        try:
            with open(ver_file, 'w+', encoding='UTF-8') as fh:
                fh.write(ret)
        except PermissionError as err:
            print(err)
            pass
        finally:
            cur_ver = ret

    return cur_ver

__version__ = _get_version()

DEBUG = True
BENCH = False
