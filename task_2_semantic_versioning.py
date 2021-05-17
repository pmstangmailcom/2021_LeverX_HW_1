'''
Расширить реализацию класса Version (см. файл task_2.py), чтобы позволять использовать его для
семантического сравнения.

Пример:

>>> Version('1.1.3') < Version('2.2.3')
True

>>> Version('1.3.0') > Version('0.3.0')
True

>>> Version('0.3.0b') < Version('1.2.42')
True

>>> Version('1.3.42') == Version('42.3.1')
False
'''

import functools


@functools.total_ordering
class Version:

    def __init__(self, version):
        self.major = self.select_version_components(version)[0]
        self.minor = self.select_version_components(version)[1]
        self.patch = self.select_version_components(version)[2]
        self.pre_release = self.select_version_components(version)[3]

    def __eq__(self, other):
        return (self.major, self.minor, self.patch, self.pre_release) == (
            other.major, other.minor, other.patch, other.pre_release)

    def __lt__(self, other):
        if (self.major, self.minor, self.patch) != (other.major, other.minor, other.patch):
            return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)
        else:
            if len(self.pre_release) == 0:
                return False
            elif len(other.pre_release) == 0:
                return True
            else:
                return self.pre_release < other.pre_release

    def select_version_components(self, version):
        '''
        Selects {major}.{minor}.{patch}-{pre_release} components from the version number.
        Return tuple(major, minor, patch, pre_release)
        '''
        version_str = str(version)
        version_split = version_str.split('.')
        major = version_split[0]
        try:
            minor = version_split[1]
        except IndexError:
            minor = '0'

        if '-' not in version_str:
            try:
                patch_str = version_split[2]
            except IndexError:
                patch_str = '0'
            pre_release = ''
        else:
            hyphen_idx = version_str.index('-')
            dot_2_idx = version_str.index('.', 2)
            patch_str = version_str[dot_2_idx + 1:hyphen_idx]
            pre_release = version_str[hyphen_idx + 1:]

        patch = (''.join(x for x in patch_str if x.isdigit() or None),
                 ''.join(x for x in patch_str if x.isalpha() or None))

        return (major, minor, patch, pre_release)


def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0")
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), "le failed"
        assert Version(version_2) > Version(version_1), "ge failed"
        assert Version(version_2) != Version(version_1), "neq failed"


if __name__ == "__main__":
    main()
