import fabric.api as fab

fab.env.roledefs['www'] = ['exhuma@michel.albert.lu']


@fab.task
def build_slides():
    with fab.lcd('slides'):
        fab.local('make slides')


@fab.task
def build_html():
    with fab.lcd('slides'):
        fab.local('make html')


@fab.task
def build_linked():
    with fab.lcd('slides'):
        fab.local('make slides html')


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
    fab.execute(build_linked)
    fab.put('slides/_build/html',
            '/var/www/albert.lu/michel/shelf/python-advanced-2016')
    fab.put('slides/_build/slides',
            '/var/www/albert.lu/michel/shelf/python-advanced-2016')
