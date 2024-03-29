from os import environ
from os.path import abspath

from fabric import task, Connection
from patchwork.transfers import rsync as rsync_

INSTANCE = '2023'


def rsync(ctx, *args, **kwargs):  # type: ignore
    """Ugly workaround for https://github.com/fabric/patchwork/issues/16."""
    ssh_agent = environ.get("SSH_AUTH_SOCK", None)
    if ssh_agent:
        ctx.config["run"]["env"]["SSH_AUTH_SOCK"] = ssh_agent
    return rsync_(ctx, *args, **kwargs)

@task
def publish(ctx):
    www = Connection(
        "ec2-user@michel.albert.lu",
        connect_kwargs={
            "disabled_algorithms": {"pubkeys": ["rsa-sha2-256", "rsa-sha2-512"]}
        },
    )
    remote_root = "/var/www/html/shelf"
    remote_folder = "%s/python-advanced-%s" % (remote_root, INSTANCE)
    latest_folder = "%s/python-advanced-latest" % remote_root
    www.run("mkdir -p %s" % remote_folder)
    rsync(
        www,
        "slides",
        remote_folder,
        delete=True,
        exclude=[
            "node_modules",
            "CONTRIBUTING.md",
            "LICENSE",
            "README.md",
            "css",
            "demo.html",
            "examples",
            "gulpfile.js",
            "js",
            "package-lock.json",
            "package.json",
            "test",
        ],
    )
    try:
        www.run("test -h {0} && rm {0}".format(latest_folder))
    except Exception as exc:
        print(exc)
    www.run("ln -s %s %s" % (remote_folder, latest_folder))

    pack_folder = "python-advanced-%s" % INSTANCE
    with www.cd(remote_folder):
        www.run("cp -r slides %s" % pack_folder)
        www.run("tar czf %s.tar.gz %s" % (pack_folder, pack_folder))
        www.run("rm -rf %s" % pack_folder)
