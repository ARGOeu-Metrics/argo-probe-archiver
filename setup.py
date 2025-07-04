from distutils.core import setup
import glob
import sys

NAME='argo-probe-archiver'
NAGIOSPLUGINS='/usr/libexec/argo/probes/archiver'

def get_ver():
    try:
        for line in open(NAME+'.spec'):
            if "Version:" in line:
                return line.split()[1]
    except IOError:
        sys.exit(1)


setup(name=NAME,
      version=get_ver(),
      license='ASL 2.0',
      author='SRCE, GRNET',
      author_email='dvrcic@srce.hr',
      description='Package include probe for checking ams-consumer component',
      platforms='noarch',
      url='https://github.com/ARGOeu-Metrics/argo-probe-archiver',
      data_files=[(NAGIOSPLUGINS, glob.glob('src/*'))],
      packages=['argo_probe_archiver'],
      package_dir={'argo_probe_archiver': 'modules/'},
      )
