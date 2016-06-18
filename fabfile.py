import fabric.api as fab

fab.env.roledefs['www'] = ['exhuma@michel.albert.lu']


@fab.task
def build_slides():
    fab.local('make slides')


@fab.task
def build_html():
    fab.local('make html')


@fab.task
def build_linked():
    fab.local('make slides html')


@fab.task
def clean():
    fab.local('make clean')


@fab.task
def serve_slides():
    fab.execute(clean)
    fab.execute(build_slides)
    with fab.lcd('_build/slides'):
        fab.local('python3 -m http.server')


@fab.task
def serve_html():
    fab.execute(clean)
    fab.execute(build_html)
    with fab.lcd('_build/html'):
        fab.local('python3 -m http.server')


@fab.task
def serve_linked():
    fab.execute(clean)
    fab.execute(build_linked)
    with fab.lcd('_build'):
        fab.local('python3 -m http.server')


@fab.task
@fab.roles('www')
def publish():
    fab.execute(build_linked)
    fab.put('_build/html',
            '/var/www/albert.lu/michel/shelf/python-advanced-2016')
    fab.put('_build/slides',
            '/var/www/albert.lu/michel/shelf/python-advanced-2016')
