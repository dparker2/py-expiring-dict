import os
import sys

# Ensure dependencies
os.system(f"{sys.executable} -m pip install --user --upgrade setuptools wheel twine")

# Build
os.system(f"{sys.executable} setup.py sdist bdist_wheel")

# Upload
os.system(f"{sys.executable} -m twine upload dist/*")
