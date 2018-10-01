# -*- coding: utf-8 -*- vim: et ts=8 sw=4 sts=4 si tw=79 cc=+1
"""Installer for the visaplan.plone.animations package."""

from setuptools import find_packages
from setuptools import setup
from os.path import isfile
# ---------------------------------------- [ destination locking ... [
import sys, os
try:  # Python 3:
    from configparser import ConfigParser
except ImportError:
    # Python 2:
    from ConfigParser import ConfigParser
# ---------------------------------------- ] ... destination locking ]

package_name = 'visaplan.plone.animations'

# -------------------------------------------- [ get the version ... [
def read_version(fn, sfn):
    main = open(fn).read().strip()
    if sfn is not None and isfile(sfn):
        suffix = valid_suffix(open(sfn).read().strip())
    else:
        suffix = ''
    return main + suffix
    # ... get the version ...
def valid_suffix(suffix):
    """
    Enforce our suffix convention
    """
    suffix = suffix.strip()
    if not suffix:
        return suffix
    allowed = set('.dev0123456789')
    disallowed = set(suffix).difference(allowed)
    if disallowed:
        disallowed = ''.join(sorted(disallowed))
        raise ValueError('Version suffix contains disallowed characters'
                         ' (%(disallowed)s)'
                         % locals())
    chunks = suffix.split('.')
    chunk = chunks.pop(0)
    if chunk:
        raise ValueError('Version suffix must start with "."'
                         ' (%(suffix)r)'
                         % locals())
    if not chunks:
        raise ValueError('Version suffix is too short'
                         ' (%(suffix)r)'
                         % locals())
    for chunk in chunks:
        if not chunk:
            raise ValueError('Empty chunk %(chunk)r in '
                             'version suffix %(suffix)r'
                             % locals())
        char = chunk[0]
        if char in '0123456789':
            raise ValueError('Chunk %(chunk)r of version suffix %(suffix)r'
                             ' starts with a digit'
                             % locals())
        char = chunk[-1]
        if char not in '0123456789':
            raise ValueError('Chunk %(chunk)r of version suffix %(suffix)r'
                             ' doesn\'t end with a digit'
                             % locals())
    return suffix  # ... valid_suffix
    # ... get the version ...
    # ... get the version ...
VERSION = read_version('VERSION',
                       'VERSION_SUFFIX')
# -------------------------------------------- ] ... get the version ]


# ---------------------------------------- [ destination locking ... [
def inject_repository_url(server):
    COMMANDS_WATCHED = ('register', 'upload')
    changed = False

    for command in COMMANDS_WATCHED:
        if command in sys.argv:
            #found one command, check for -r or --repository
            commandpos = sys.argv.index(command)
            i = commandpos+1
            repo = None
            while i<len(sys.argv) and sys.argv[i].startswith('-'):
                #check all following options (not commands)
                if (sys.argv[i] == '-r') or (sys.argv[i] == '--repository'):
                    #next one is the repository itself
                    try:
                        repo = sys.argv[i+1]
                        if repo.lower() != server.lower():
                            print "You tried to %s to %s, while this package "\
                                   "is locked to %s" % (command, repo, server)
                            sys.exit(1)
                        else:
                            #repo OK
                            pass
                    except IndexError:
                        #end of args
                        pass
                i=i+1

            if repo is None:
                #no repo found for the command
                print "Adding repository %s to the command %s" % (
                    server, command )
                sys.argv[commandpos+1:commandpos+1] = ['-r', server]
                changed = True

    if changed:
        print "Final command: %s" % (' '.join(sys.argv))


def check_repository(name):
    server = None
    # find repository in .pypirc file
    rc = os.path.join(os.path.expanduser('~'), '.pypirc')
    if os.path.exists(rc):
        config = ConfigParser()
        config.read(rc)
        if 'distutils' in config.sections():
            # let's get the list of servers
            index_servers = config.get('distutils', 'index-servers')
            _servers = [s.strip() for s in index_servers.split('\n')
                        if s.strip() != '']
            for srv in _servers:
                if srv == name:
                    repos = config.get(srv, 'repository')
                    print "Found repository %s for %s in '%s'" % (
                        repos, name, rc)
                    server = repos
                    break

    if not server:
        print "No repository for %s found in '%s'" % (name, rc)
        sys.exit(1)

    inject_repository_url(server)


def check_server(server):
    if not server:
        return
    inject_repository_url(server)


# use one of these to check the correct destination:
PYPI_KEY = 'visaplan'
PYPI_URL = 'https://pypi.visaplan.com'

check_repository(PYPI_KEY)
# check_server(PYPI_URL)
# ---------------------------------------- ] ... destination locking ]


# ------------------------------------------- [ for setup_kwargs ... [
long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])

# see as well --> src/visaplan/plone/animations/configure.zcml:
exclude_subpackages = (
        )
exclude_packages = []
for subp in exclude_subpackages:
    exclude_packages.extend([package_name + '.' + subp,
                             package_name + '.' + subp + '.*',
                             ])
packages = find_packages(
            'src',
            exclude=exclude_packages)
# ------------------------------------------- ] ... for setup_kwargs ]

setup_kwargs = dict(
    name=package_name,
    version=VERSION,
    description="A dexterity-based content type for animations.",
    long_description=long_description,
    # Get more from https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Intended Audience :: Developers",
        "Natural Language :: German",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    # keywords='Python Plone',
    author='Tobias Herp',
    author_email='tobias.herp@visaplan.com',
    url='https://pypi.org/project/visaplan.plone.animations',
    license='GPL version 2',
    packages=packages,
    namespace_packages=[
        'visaplan',
        'visaplan.plone',
        ],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'plone.app.dexterity',
        # ... from bobtemplates.Plone:
        'plone.api>=1.8.4',
        'Products.GenericSetup>=1.8.2',
        'plone.app.dexterity<=2.1.1',
        'plone.app.referenceablebehavior',
        'plone.app.relationfield',
        'plone.app.lockingbehavior',
        'plone.schema',
        # ... further requirements removed
    ],
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
setup(**setup_kwargs)
