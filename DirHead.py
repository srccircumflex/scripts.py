# MIT License
#
# Copyright (c) 2022 Adrian F. Hoefflin [srccircumflex]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#


from os import scandir, access
from time import localtime, strftime, gmtime
from ast import literal_eval
from typing import Literal


class ConvertDirHeader:

    # https://docs.python.org/3.9/library/time.html#time.strftime

    def __init__(self, header, time_format: str = "%y.%m.%d-%H:%M", utc: bool = False):

        self.formt = time_format

        self.utc = utc

        self.header = header
        self.stats_convert: dict = {
            'st_mode': self.stat_origin_result,
            'st_ino': self.stat_origin_result,
            'st_dev': self.stat_origin_result,
            'st_nlink': self.stat_origin_result,
            'st_uid': self.stat_origin_result,
            'st_gid': self.stat_origin_result,
            'st_size': self.stat_size_conv,
            'st_atime': self.stat_time_conv,
            'st_mtime': self.stat_time_conv,
            'st_ctime': self.stat_time_conv
        }

    @staticmethod
    def stat_origin_result(_stat) -> str:
        return str(_stat)

    def stat_time_conv(self, _stat) -> str:
        if self.utc:
            return strftime(self.formt, gmtime(_stat))
        return strftime(self.formt, localtime(_stat))

    @staticmethod
    def stat_size_conv(_stat) -> dict[str:int]:
        return {
            'B': _stat,
            'K': round(_stat / 1024),
            'M': round(_stat / 1024 / 1024),
            'G': round(_stat / 1024 / 1024 / 1024),
        }

    def _str(self):
        if isinstance(self.header, str): return self.header
        return self.header.decode(errors="replace")

    def _liev(self):
        if type(self.header) in (tuple, list, dict, set): return self.header
        return literal_eval(self._str())

    def fformat(self):
        h_convert: dict = self._liev()
        for file_header in h_convert:
            for header_content_type in h_convert[file_header]:
                h_convert[
                    file_header
                ][
                    header_content_type
                ] = self.stats_convert[
                    header_content_type
                ].__call__(
                    h_convert[
                        file_header
                    ][
                        header_content_type
                    ]
                )
        return h_convert


class DirHeader:

    # stats
    #        # 0: 'st_mode',   # Permissions bits
    #        # 1: 'st_ino',    # (Inode@UNIX, FileIndex@WINDOWS)
    #        # 2: 'st_dev',    # Device identifier
    #        # 3: 'st_nlink',  # Number of hard links
    #        # 4: 'st_uid',    # User id
    #        # 5: 'st_gid',    # Group id
    #        6: 'st_size',   # Length
    #        7: 'st_atime',  # Access time
    #        8: 'st_mtime',  # Modification time
    #        9: 'st_ctime'   # (MetadataChangeTime@UNIX, CreationTime@WINDOWS)

    def __init__(self,
                 path: str = None,
                 desired_tag_indices: dict = None
                 ):

        self.tag_to_itotagitem = {
            'st_mode' : {0: 'st_mode'},
            'st_ino' : {1: 'st_ino'},
            'st_dev' : {2: 'st_dev'},
            'st_nlink' : {3: 'st_nlink'},
            'st_uid' : {4: 'st_uid'},
            'st_gid' : {5: 'st_gid'},
            'st_size' : {6: 'st_size'},
            'st_atime' : {7: 'st_atime'},
            'st_mtime' : {8: 'st_mtime'},
            'st_ctime' : {9: 'st_ctime'}
        }

        if desired_tag_indices is None:
            desired_tag_indices = {
                6: 'st_size',
                7: 'st_atime',
                8: 'st_mtime',
                9: 'st_ctime'
            }

        self.desired_tag_indexes = desired_tag_indices
        self.dir_entrys: list = list(scandir(path))

    def add_tag(self, tag: Literal['st_mode',
                                   'st_ino',
                                   'st_dev',
                                   'st_nlink',
                                   'st_uid',
                                   'st_gid',
                                   'st_size',
                                   'st_atime',
                                   'st_mtime',
                                   'st_ctime']):
        self.desired_tag_indexes |= self.tag_to_itotagitem[tag]
        return self

    def mk_header(self) -> dict:
        headers: dict = dict()
        for entry in self.dir_entrys:
            if entry.is_dir() and access(entry.path, 5):
                headers.setdefault(entry.name + '/', dict())
            elif entry.is_file() and access(entry.path, 4):
                headers.setdefault(entry.name, dict())
            else:
                continue
            entry_stats = list(entry.stat())
            for st_i in self.desired_tag_indexes:
                headers[list(headers)[-1]].setdefault(self.desired_tag_indexes[st_i], entry_stats[st_i])
        return headers

    def liev_(self):
        return self.mk_header()

    def __str__(self):
        return str(self.liev_())

    def __bytes__(self):
        return self.__str__().encode(errors="replace")


if __name__ == "__main__":

    from pprint import pprint

    dir_header = DirHeader(desired_tag_indices=dict())
    dir_header.add_tag('st_uid').add_tag('st_size').add_tag('st_atime').add_tag('st_mtime')
    raw_header = dir_header.mk_header()
    print("=================raw header=================")
    pprint(raw_header)
    print("============================================")
    print("==============converted header==============")
    pprint(ConvertDirHeader(raw_header).fformat())
    print("============================================")










