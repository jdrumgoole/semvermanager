import os
import argparse


class VersionError(ValueError):
    pass


class Version:

    TAGS = {0: "alpha", 1: "beta", 2:"production"}
    FIELDS = ["major", "minor", "patch", "tag"]
    FILENAME = "VERSION"

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

    def __init__(self, major=0, minor=0, patch=0, tag="alpha"):
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

    def __str_(self):
        return f"{self._major}.{self._minor}.{self._patch}-{self._tag}"

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
            self._tag_index +=1
        self._tag = Version.TAGS[self._tag_index]

    @staticmethod
    def write(filename=None, version=None):
        if not filename:
            filename = Version.FILENAME

        if not version:
            version = Version()

        with open(filename, "w") as file:
            file.write(f"{str(version)}\n")

        return filename, version

    @staticmethod
    def read(filename):
        if not filename:
            filename = Version.FILENAME

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
            version = version.strip()
        except ValueError as e:
            raise VersionError(e)

        try:
            major, minor, patch = [int(x) for x in version.split('.')]
        except ValueError as e:
            raise VersionError(e)

        return Version(major, minor, patch, tag)

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

    def __repr__(self):
        return f"{self.__class__.__name__({self._major}, {self._minor}, {self._patch}, {self._tag})}"

    def __str__(self):
        return f"VERSION={self._major}.{self._minor}.{self._patch}-{self._tag}"


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--filename",
        default=Version.FILENAME,
        help="File to use as version file [default: %(default)s]"
    )
    parser.add_argument(
        "--make",
        default=False,
        action="store_true",
        help="Make a new version file")

    parser.add_argument(
        "--bump",
        choices=Version.FIELDS,
        help="Bump a version field")

    parser.add_argument(
        "--getversion",
        default=False,
        action="store_true",
        help="Report the current version in the specified file")

    parser.add_argument(
        "--overwrite",
        default=False,
        action="store_true",
        help="overwrite files without checking"
    )
    args = parser.parse_args()

    if args.make:
        if  args.overwrite or not os.path.isfile(args.filename):
            filename, version = Version.write(args.filename)
            print(f"Created {version} in '{args.filename}'")
        elif os.path.isfile(args.filename):
            answer = input(f"Overwrite file '{args.filename}' (Y/N [N]: ")
            if len(answer) > 0 and answer.strip().lower() == 'y':
                filename, version = Version.write(args.filename)
                print(f"Overwrote {version} in '{args.filename}'")

    if args.getversion:
        if os.path.isfile(args.filename):
            v = Version.read(args.filename)
            print(v)
        else:
            print(f"No such version file: '{args.filename}'")

    if args.bump in Version.FIELDS:
        if not os.path.isfile(args.filename):
            raise VersionError(f"No such file:'{args.filename}' can't bump {args.bump} version")
        v = Version.read(args.filename)
        print(f"Bumping '{args.bump}' value from {v.field(args.bump)} ", end="")
        v.bump(args.bump)
        print(f"to {v.field(args.bump)} in '{args.filename}'")
        Version.write(args.filename, v)
        print(f"new version: {v}")

