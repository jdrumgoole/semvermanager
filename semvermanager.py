import os
import argparse


class VersionError(ValueError):
    """Exception for handling errors in Version Class"""
    pass


class Version:
    """
    Handle creation and storage of SEMVER version numbers. In this case
    SEMVERs must be of the form a.b.c-tag, Where a,b and c are integers
    in the range 0-n and tag is one of `Version.TAGS`.

    Version numbers may be bumped by using the various bump functions.
    Bumping minor zeros patch, bumping major zeros minor.

    """

    TAGS = {0: "alpha", 1: "beta", 2: "prod"}
    FIELDS = ["major", "minor", "patch", "tag"]
    FILENAME = "VERSION"

    def __init__(self, major=0, minor=0, patch=0, tag="alpha"):
        """

        :param major: 0-n
        :param minor: 0-n
        :param patch: 0-n
        :param tag: member of Version.TAGs.values()
        """
        self._major = major
        self._minor = minor
        self._patch = patch
        self._tag_index = None
        self._tag = None
        for k, v in Version.TAGS.items():
            if tag == v:
                self._tag = v
                self._tag_index = k

        if self._tag_index is None:
            raise VersionError(f"'{tag}' is not a valid version tag")

    def get_field(self, field):
        if field in self.FIELDS:
            return self.field_map()[field]
        else:
            raise VersionError(f"No such field name: '{field}'")

    def set_field(self, field, value):
        if field == "TAG":
            self.field_map()[field] = value
        elif type(value) is int and value >= 0:
            if field in self.FIELDS:
                self.field_map()[field] = value
            else:
                raise VersionError(f"No such field name: '{field}'")
        else:
            raise VersionError(f"{value} is not an integer value 0 or greater")

    def field(self, field):
        return self.field_map()[field]

    def bump(self, field):
        self.bump_map()[field]()

    def bump_major(self):
        self._patch = 0
        self._minor = 0
        self._major += 1

    def bump_minor(self):
        self._patch = 0
        self._minor += 1

    def bump_patch(self):
        self._patch += 1

    def bump_tag(self):
        if self._tag_index == len(Version.TAGS) - 1:
            self._tag_index = 0
        else:
            self._tag_index += 1
        self._tag = Version.TAGS[self._tag_index]

    @property
    def major(self):
        return self._major

    @major.setter
    def major(self, value):
        self._major = value

    @property
    def minor(self):
        return self._minor

    @minor.setter
    def minor(self, value):
        self._minor = value

    @property
    def patch(self):
        return self._patch

    @patch.setter
    def patch(self, value):
        self._patch = value

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        self._tag = value

    def bump_map(self):
        return {"major": self.bump_major,
                "minor": self.bump_minor,
                "patch": self.bump_patch,
                "tag": self.bump_tag}

    def field_map(self):
        return {"major": self.major,
                "minor": self.minor,
                "patch": self.patch,
                "tag": self.tag}

    @staticmethod
    def update(filename=None, version=None):
        if not filename:
            filename = Version.FILENAME

        if not version:
            version = Version()

        with open(filename, "r") as input_file:
            with open(filename+".temp", "w") as output_file:
                for line in input_file:
                    candidate = line.strip()
                    if candidate.startswith("VERSION"):
                        output_file.write(f"{str(version)}\n")
                    else:
                        output_file.write(line)

        os.rename(filename, filename+".old")
        os.rename(filename+".temp", filename)

    @staticmethod
    def write(filename, version):
        """
        Write a version to a file as a single line in the form
        `VERSION = 'MAJOR.MINOR.PATH-TAG'`
        """

        if not isinstance(version, Version):
            raise VersionError(f"{version} is not an instance of Version")

        with open(filename, "w") as file:
            file.write(f"{str(version)}\n")

        return filename, version

    @staticmethod
    def find(filename):
        """Look for the first instance of a VERSION definition in a file
        and try and parse it as a `Version`"""

        version = None
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith("VERSION"):
                    version = Version.parse_version(line)
                    break

        return version


    @staticmethod
    def read(filename):
        """Read a single lien from a file and try and parse it as `Version`"""

        with open(filename, "r") as file:
            line = file.readline()
            line.rstrip()

        try:
            _, rhs = line.split("=")
        except ValueError as e:
            raise VersionError(e)

        try:
            version, tag = rhs.split("-")
            tag = tag.strip()
            tag = tag.strip("\"\'")
            version = version.strip()  # whitespace
            version = version.strip("\"\'")  # quotes
        except ValueError as e:
            raise VersionError(e)

        try:
            major, minor, patch = [int(x) for x in version.split('.')]
        except ValueError as e:
            raise VersionError(e)

        return Version(major, minor, patch, tag)

    @staticmethod
    def parse_version(line):
        line = line.strip()
        if line.startswith("VERSION"):
            try:
                version_label, rhs = line.split("=")
                version_label = version_label.strip()
                rhs = rhs.strip()
                assert version_label == "VERSION"
            except ValueError as e:
                raise VersionError(f"{e} : in '{line}'")
        else:
            rhs = line

        try:
            if "-" in rhs:
                version, tag = rhs.split("-")
                tag = tag.strip()
                tag = tag.strip("\"\'")
                version = version.strip()
                version = version.strip("\"\'")
            else:
                raise VersionError(f"The tag value must be separated by a '-' in '{rhs}'")
        except ValueError as e:
            raise VersionError(f"{e} : in '{rhs}'")

        try:
            major, minor, patch = [int(x) for x in version.split('.')]
        except ValueError as e:
            raise VersionError(f"{e} : in '{version}'")

        return Version(major, minor, patch, tag)

    def __eq__(self, other):
        return self.major == other.major and \
               self.minor == other.minor and \
               self.patch == other.patch and \
               self.tag == other.tag

    def __str__(self):
        return f"VERSION = '{self._major}.{self._minor}.{self._patch}-{self._tag}'"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.major}, {self.minor}, {self.patch}, '{self.tag}')"

    def bare_version(self):
        return f'{self._major}.{self._minor}.{self._patch}-{self._tag}'


