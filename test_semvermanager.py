import unittest
import os

import temp

from versionmanager import Version, VersionError


class TestVersionManager(unittest.TestCase):

    def test_init(self):
        v = Version()
        self.assertEqual(v.major, 0)
        self.assertEqual(v.minor, 0)
        self.assertEqual(v.patch, 0)
        self.assertEqual(v.tag, "alpha")

    def test_version(self):
        v=Version(0, 1, 0, "beta")
        self.assertEqual(v.major, 0)
        self.assertEqual(v.minor, 1)
        self.assertEqual(v.patch, 0)
        self.assertEqual(v.tag, "beta")

        v=Version(1, 0, 0, "beta")
        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 0)
        self.assertEqual(v.patch, 0)
        self.assertEqual(v.tag, "beta")

        v=Version(0, 0, 1, "beta")
        self.assertEqual(v.major, 0)
        self.assertEqual(v.minor, 0)
        self.assertEqual(v.patch, 1)
        self.assertEqual(v.tag, "beta")

        v=Version(0, 0, 1, "alpha")
        self.assertEqual(v.major, 0)
        self.assertEqual(v.minor, 0)
        self.assertEqual(v.patch, 1)
        self.assertEqual(v.tag, "alpha")

        v=Version(0, 0, 1, "beta")
        self.assertEqual(v.major, 0)
        self.assertEqual(v.minor, 0)
        self.assertEqual(v.patch, 1)
        self.assertEqual(v.tag, "beta")

        v=Version(0, 0, 1, "prod")
        self.assertEqual(v.major, 0)
        self.assertEqual(v.minor, 0)
        self.assertEqual(v.patch, 1)
        self.assertEqual(v.tag, "prod")

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
            Version.write(temp_filename, v)
            x = Version.read(temp_filename)
            self.assertEqual(x, v)
            x.bump_tag()
            Version.write(temp_filename, x)
            w = Version.read(temp_filename)
            self.assertEqual(x, w)

            v = Version(0, 3, 1, 'beta')  # test single quotes for tag
            Version.write(temp_filename, v)
            x = Version.read(temp_filename)
            self.assertEqual(x, v)

        finally:
            if os.path.isfile(temp_filename):
                os.unlink(temp_filename)

    def test_file_update(self):

        v = Version(0, 4, 2, "prod")
        temp_filename = temp.tempfile()

        try:
            Version.write(temp_filename, v)
            v2 = Version(0, 4, 3, "prod")
            Version.update(temp_filename, v2)
            v3 = Version.read(temp_filename)
            self.assertEqual(v2, v3)
            self.assertNotEqual(v, v3)
        finally:
            if os.path.isfile(temp_filename):
                os.unlink(temp_filename)
if __name__ == '__main__':
    unittest.main()
