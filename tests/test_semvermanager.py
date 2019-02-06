import unittest
import os
from contextlib import contextmanager
from io import StringIO
import sys

import temp

from semvermanager import Version, VersionError
from semvermgr import main


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class TestVersionManager(unittest.TestCase):

    def test_init(self):
        v = Version()
        self.assertEqual(v.major, 0)
        self.assertEqual(v.minor, 0)
        self.assertEqual(v.patch, 0)
        self.assertEqual(v.tag, "alpha")

    def test_version(self):
        v = Version(0, 1, 0, "beta")
        self.assertEqual(v.major, 0)
        self.assertEqual(v.minor, 1)
        self.assertEqual(v.patch, 0)
        self.assertEqual(v.tag, "beta")

        v = Version(1, 0, 0, "beta")
        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 0)
        self.assertEqual(v.patch, 0)
        self.assertEqual(v.tag, "beta")

        v = Version(0, 0, 1, "beta")
        self.assertEqual(v.major, 0)
        self.assertEqual(v.minor, 0)
        self.assertEqual(v.patch, 1)
        self.assertEqual(v.tag, "beta")

        v = Version(0, 0, 1, "alpha")
        self.assertEqual(v.major, 0)
        self.assertEqual(v.minor, 0)
        self.assertEqual(v.patch, 1)
        self.assertEqual(v.tag, "alpha")

        v = Version(0, 0, 1, "beta")
        self.assertEqual(v.major, 0)
        self.assertEqual(v.minor, 0)
        self.assertEqual(v.patch, 1)
        self.assertEqual(v.tag, "beta")

        v = Version(0, 0, 1, "")
        self.assertEqual(v.major, 0)
        self.assertEqual(v.minor, 0)
        self.assertEqual(v.patch, 1)
        self.assertEqual(v.tag, "")

        self.assertRaises(VersionError, Version, 0, 0, 1, "test")

    def test_bump(self):

        tags = Version.TAGS
        v = Version(0, 0, 1, "alpha")
        v.bump_tag()
        self.assertEqual(v.tag, tags[1])
        v.bump_tag()
        self.assertEqual(v.tag, tags[2])
        v.bump_tag()
        self.assertEqual(v.tag, tags[0])

        v = Version(0, 0, 1, "alpha")
        self.assertEqual(v.tag, "alpha")
        self.assertEqual(v.tag_version, 0)
        v.bump_tag_version()
        self.assertEqual(v.tag, "alpha")
        self.assertEqual(v.tag_version, 1)
        self.assertEqual(v, Version( 0, 0, 1, "alpha", 1))

        v.bump_patch()
        self.assertEqual(v.patch, 2)
        v.bump_patch()
        self.assertEqual(v.patch, 3)

        v.bump_minor()
        self.assertEqual(v.patch, 0)
        self.assertEqual(v.minor, 1)
        self.assertEqual(v.major, 0)

        v.bump_minor()
        self.assertEqual(v.patch, 0)
        self.assertEqual(v.minor, 2)
        self.assertEqual(v.major, 0)

        v.bump_major()
        self.assertEqual(v.patch, 0)
        self.assertEqual(v.minor, 0)
        self.assertEqual(v.major, 1)

        v.bump_major()
        self.assertEqual(v.patch, 0)
        self.assertEqual(v.minor, 0)
        self.assertEqual(v.major, 2)

    def test_file_write(self):

        temp_filename = temp.tempfile()
        try:
            v = Version(0, 4, 1, "beta")
            v.write(temp_filename)
            x = Version().read(temp_filename)
            self.assertEqual(x, v)
            x.bump_tag()
            x.write(temp_filename)
            w = Version().read(temp_filename)
            self.assertEqual(x, w)

            v = Version(0, 3, 1, 'beta')  # test single quotes for tag
            v.write(temp_filename)
            x = Version().read(temp_filename)
            self.assertEqual(x, v)

        finally:
            if os.path.isfile(temp_filename):
                os.unlink(temp_filename)

    def test_file_write_sep(self):

        temp_filename = temp.tempfile()
        try:
            v = Version(0, 4, 1, "beta", separator=":")
            v.write(temp_filename)
            x = Version().read(temp_filename, separator=":")
            self.assertEqual(x, v)
            x.bump_tag()
            x.write(temp_filename)
            w = Version().read(temp_filename, separator=":")
            self.assertEqual(x, w)

            v = Version(0, 3, 1, 'beta', separator="->")  # test single quotes for tag
            v.write(temp_filename)
            x = Version().read(temp_filename, separator="->")
            self.assertEqual(x, v)

        finally:
            if os.path.isfile(temp_filename):
                os.unlink(temp_filename)

    def test_file_update(self):

        v = Version(0, 4, 2, "")
        temp_filename = temp.tempfile()

        try:
            v.write(temp_filename)
            v2 = Version(0, 4, 3, "")
            print(v2)
            Version.update(temp_filename, v2)
            v3 = Version().read(temp_filename)
            self.assertEqual(v2, v3)
            self.assertNotEqual(v, v3)
        finally:
            if os.path.isfile(temp_filename):
                os.unlink(temp_filename)

    def test_parse_version(self):

        v = Version.parse_version("0.0.0-alpha")
        self.assertEqual(v, Version(0, 0, 0, "alpha"))

        v = Version.parse_version("VERSION=0.0.0-alpha")
        self.assertEqual(v, Version(0, 0, 0, "alpha"))

        v = Version.parse_version("  VERSION  =  0.0.0-alpha  ")
        self.assertEqual(v, Version(0, 0, 0, "alpha"))

        v = Version.parse_version("  0.0.0-alpha  ")
        self.assertEqual(v, Version(0, 0, 0, "alpha"))

        # VERSION = '0.0.1-alpha'

        v = Version.parse_version("VERSION = '0.0.1-alpha'")
        self.assertEqual(v, Version(0, 0, 1, "alpha"))

        v = Version.parse_version("version = '0.0.1-alpha'", lhs="version")
        self.assertEqual(v, Version(0, 0, 1, "alpha"))

        v = Version.parse_version("version : '0.0.1-alpha'", lhs="version", separator=":")
        self.assertEqual(v, Version(0, 0, 1, "alpha", tag_version=0, lhs="version", separator=":"))

        v = Version.parse_version("version : '0.4.2'", lhs="version", separator=":")
        self.assertEqual(v, Version(0, 4, 2, "", tag_version=0,  lhs="version", separator=":"))

    def test_find(self):
        # looking for VERSION = '0.0.1-alpha' in test_data

        try:
            with open("test_data", "w") as file:
                file.write("""
# Package meta-data.
NAME = 'semvermanager'
DESCRIPTION = "semvermamager implements a restricted subset of the SEMVER standard"

EMAIL = 'joe@joedrumgoole.com'
AUTHOR = 'Joe Drumgoole'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.0.1-alpha'
URL = 'https://github.com/jdrumgoole/semvermanager'
            """)
            v = Version.find("test_data")
            self.assertEqual(v, Version(0, 0, 1, "alpha"))
        finally:
            os.unlink("test_data")

    def test_cli(self):
        try:
            with captured_output() as (out, err):
                main(["--make", "--overwrite", "dummy1", "dummy2"])
                self.assertTrue(os.path.isfile("dummy1"))
                self.assertTrue(os.path.isfile("dummy1"))
                self.assertTrue(out.getvalue().startswith("Created version VERSION = '0.0.0-alpha0' in 'dummy1'"))
                main(["--bump", "tag_version", "--overwrite", "dummy1"])
        finally:
            os.unlink("dummy1")
            os.unlink("dummy2")


if __name__ == '__main__':
    unittest.main()
