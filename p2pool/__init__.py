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
    ver_file = '%s/VERSION' % os.path.dirname(os.path.dirname(dir_name))
    with open(ver_file, 'a+', encoding='UTF-8') as fh:
        fh.seek(0)
        cur_ver = fh.read().strip()
        if ret is not None and cur_ver != ret:
            fh.seek(0)
            fh.write(ret)
            return ret
        return cur_ver

__version__ = _get_version()

DEBUG = True
BENCH = False
