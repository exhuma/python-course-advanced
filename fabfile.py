import fabric.api as fab

fab.env.roledefs['www'] = ['exhuma@michel.albert.lu']
INSTANCE = '2016'


@fab.task
def fetch_common_files():
    '''
    Put shared files from the "common" folder of the repository into the proper
    place for building.
    '''
    l = fab.local
    l('cp -v ../common/*.css slides/_static')


@fab.task
def build_slides():
    fab.execute(fetch_common_files)
    with fab.lcd('slides'):
        fab.local('make slides')


@fab.task
def build_html():
    fab.execute(fetch_common_files)
    with fab.lcd('slides'):
        fab.local('make html')


@fab.task
def build_linked():
    fab.execute(fetch_common_files)
    with fab.lcd('slides'):
        fab.local('make slides html')


@fab.task
def clean():
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
    remote_folder = '/var/www/albert.lu/michel/shelf/python-advanced-%s' % INSTANCE
    latest_folder = '/var/www/albert.lu/michel/shelf/python-advanced-latest'
    fab.execute(build_linked)
    fab.run('mkdir -p %s' % remote_folder)
    fab.put('slides/_build/html', remote_folder)
    fab.put('slides/_build/slides', remote_folder)
    with fab.settings(warn_only=True):
        fab.run('test -h {0} && rm {0}'.format(latest_folder))
    fab.run('ln -s %s %s' % (remote_folder, latest_folder))
