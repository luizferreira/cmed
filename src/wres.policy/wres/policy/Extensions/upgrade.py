# edit this line before upgrade.
version = '0.5' # ex: '0.8'

import os
# from wres.policy.Extensions import exporter
# from wres.policy.Extensions import importer

def main(self):
    if version == '0.0':
        raise Exception('You need to set the release version!')
    export_dir = self.z_export(self, version)
    # export_dir = exporter.main(self, version)
    abs_export_dir = os.path.abspath(export_dir)
    # importer.main(self, export_dir, version)
    self.z_import(self, abs_export_dir, version)
