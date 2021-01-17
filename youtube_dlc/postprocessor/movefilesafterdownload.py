from __future__ import unicode_literals
import os
import shutil

from .common import PostProcessor
from ..utils import encodeFilename

class MoveFilesAfterDownloadPP(PostProcessor):
    PP_NAME = 'MoveFiles'

    def __init__(self, downloader, files_to_move):
        PostProcessor.__init__(self, downloader)
        self.files_to_move = files_to_move

    def run(self, info):
        self.files_to_move.append(info['__dl_filename'])
        outdir = os.path.dirname(os.path.abspath(encodeFilename(info['__final_filename'])))

        for oldfile in self.files_to_move:
            if not os.path.exists(encodeFilename(oldfile)):
                self.report_warning('File "%s" cannot be found' % oldfile)
                continue
            newfile = os.path.join(outdir, os.path.basename(encodeFilename(oldfile)))
            if os.path.abspath(encodeFilename(oldfile)) == os.path.abspath(newfile):
                continue
            if os.path.exists(newfile):
                if self.get_param('overwrites', True):
                    self.report_warning('Replacing existing file "%s"' % newfile)
                    os.path.remove(newfile)
                else:
                    self.report_warning(
                        'Cannot move file "%s" out of temporary directory since "%s" already exists. '
                        % (oldfile, newfile))
                    continue
            self.write_debug('Moving file "%s" to "%s"' % (oldfile, newfile))
            shutil.move(encodeFilename(oldfile), newfile)  # os.rename cannot move between volumes

        info['filepath'] = info['__final_filename']
        return [], info
