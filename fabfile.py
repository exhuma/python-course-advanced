import fabric.api as fab
from fabric.context_managers import shell_env
from os.path import abspath

fab.env.roledefs['www'] = ['michel.albert.lu']
INSTANCE = '2018'
VIRTUAL_ENV = abspath('./env')
ENVPATH = '%s/bin:$PATH' % VIRTUAL_ENV


@fab.task
def fetch_common_files():
    '''
    Put shared files from the "common" folder of the repository into the proper
    place for building.
    '''
    l = fab.local
    l('cp -v common/custom.css slides/_static')


@fab.task
def build_slides():
    fab.execute(fetch_common_files)
    fab.local('cp -v common/slidestyle.css slides/_static/htmlstyle.css')
    with fab.lcd('slides'):
        with shell_env(PATH=ENVPATH, VIRTUAL_ENV=VIRTUAL_ENV):
            fab.local('make slides')


@fab.task
def build_html():
    fab.execute(fetch_common_files)
    fab.local('cp -v common/htmlstyle.css slides/_static/htmlstyle.css')
    with fab.lcd('slides'):
        with shell_env(PATH=ENVPATH, VIRTUAL_ENV=VIRTUAL_ENV):
            fab.local('make html')


@fab.task
def build_linked():
    fab.execute(fetch_common_files)
    with fab.lcd('slides'):
        with shell_env(PATH=ENVPATH, VIRTUAL_ENV=VIRTUAL_ENV):
            fab.local('make slides html')


@fab.task
def develop():
    fab.local('[ -d env ] || python3 -m venv env')
    fab.local('./env/bin/pip install hieroglyph')
    fab.local('git submodule init')
    fab.local('git submodule update')


@fab.task
def clean():
    with fab.lcd('slides'):
        fab.local('make clean')


@fab.task
def serve_slides():
    fab.execute(clean)
    fab.execute(build_slides)
    with fab.lcd('slides/_build/slides'):
        fab.local('python3 -m http.server')


@fab.task
def serve_html():
    fab.execute(clean)
    fab.execute(build_html)
    with fab.lcd('slides/_build/html'):
        fab.local('python3 -m http.server')


@fab.task
def serve_linked():
    fab.execute(clean)
    fab.execute(build_linked)
    with fab.lcd('slides/_build'):
        fab.local('python3 -m http.server')


@fab.task
@fab.roles('www')
def publish():
    remote_root = '/var/www/html/shelf'
    remote_folder = '%s/python-advanced-%s' % (remote_root, INSTANCE)
    latest_folder = '%s/python-advanced-latest' % remote_root
    fab.execute(build_html)
    fab.execute(build_slides)
    fab.run('mkdir -p %s' % remote_folder)
    fab.put('slides/_build/html', remote_folder)
    fab.put('slides/_build/slides', remote_folder)
    with fab.settings(warn_only=True):
        fab.run('test -h {0} && rm {0}'.format(latest_folder))
    fab.run('ln -s %s %s' % (remote_folder, latest_folder))

    pack_folder = 'python-advanced-%s' % INSTANCE
    fab.local('mkdir -p %s' % pack_folder)
    fab.local('mv slides/_build/html slides/_build/slides %s' % pack_folder)
    fab.local('tar czf %s.tar.gz %s' % (pack_folder, pack_folder))
    fab.local('rm -rf %s' % pack_folder)
    fab.put('%s.tar.gz' % pack_folder, remote_folder)
