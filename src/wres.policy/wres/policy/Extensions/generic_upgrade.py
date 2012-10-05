import os

#==========================================================================
#
# Scripts para importar instancias de uma maneira generica especificando
# parametros manualmente. Este e o module wres.policy.generic_upgrade
# Recomenda-se rodar de dentro de um plone site auxiliar para se 
# conseguir os contextos desejados.
#
#==========================================================================

# edit this line before upgrade.
version = '0.11' # ex: '0.8'

def main(self):
    if version == '0.0':
        raise Exception('You need to set the release version!')
    #fill this line before upgrading.
    export_dir =  'export-cmed'
    abs_export_dir = os.path.abspath(export_dir)
    self.z_import(self, abs_export_dir, version)