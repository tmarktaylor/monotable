"""Create a preview of setup.py's long description.

usage: python readme_preview.py path_to_rst2html.py path_to_html_output_file

Runs setup.py --long-description, converts the .rst output to .html,
and saves to a file.

The output should have a similar appearance to how the long description
will appear on the Python Package Index.

Runs the script rst2html which is installed by docutils and sphinx.

Somewhat duplicates the functionality of Python Package Index readme_renderer.
"""

import subprocess
import sys
import tempfile

rst2html_path = sys.argv[1]
output_file = sys.argv[2]

with tempfile.SpooledTemporaryFile(max_size=60000) as fp:
    subprocess.call('python setup.py --long-description', stdout=fp)
    fp.seek(0)
    cmd = 'python ' + rst2html_path + ' - ' + output_file
    subprocess.call(cmd, stdin=fp)
