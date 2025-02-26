#!E:\www\w_pro\w_pro_abcerp\pro_abcerp_t1\codes\v1\v1.0_abcerp\venv_dev\Scripts\python.exe

# $Id: rst2s5.py 4564 2006-05-21 20:44:42Z wiemann $
# Author: Chris Liechti <cliechti@gmx.net>
# Copyright: This module has been placed in the public domain.

"""
A minimal front end to the Docutils Publisher, producing HTML slides using
the S5 template system.
"""

try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

from docutils.core import publish_cmdline, default_description


description = ('Generates S5 (X)HTML slideshow documents from standalone '
               'reStructuredText sources.  ' + default_description)

publish_cmdline(writer_name='s5', description=description)
