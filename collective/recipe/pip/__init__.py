# -*- coding: utf-8 -*-
"""Recipe pip."""
import itertools
import os

from pip import req
from pip.download import PipSession


old_parse_requirements = req.parse_requirements


def parse_requirements(filename, *kv, **kw):
    """Override requirements parsing."""
    file_dir = os.path.dirname(filename)
    if os.path.isdir(os.path.dirname(filename)):
        os.chdir(file_dir)
    return old_parse_requirements(filename, *kv, **kw)


req.parse_requirements = parse_requirements


class Recipe(object):
    """zc.buildout recipe"""

    default_vcs = 'git'
    skip_requirements_regex = ''

    def __init__(self, buildout, name, options):
        self.options = options
        self.buildout = buildout
        self.index_urls = []
        self.find_links = []
        self.isolated_mode = options.get('isolated_mode') == 'true'
        self.process()

    def install(self):
        """Installer"""
        return tuple()

    def process(self):
        """Process everything"""
        eggs = []
        versions = []
        urls = []
        for requirement in self.parse_files(self.options.get('configs').split()):
            if requirement.req is not None:
                specs = ','.join([''.join(s) for s in requirement.req.specs])
                eggs.append(requirement.name + specs)
            else:
                specs = None
            if specs:
                versions.append((requirement.name, specs[2:] if specs.startswith('=') else specs))
            if requirement.editable:
                urls.append(requirement.url)
            elif requirement.url:
                if not '#egg=' in requirement.url:
                    urls.append('{0}#egg={1}{2}'.format(requirement.url, requirement.name, specs))
                else:
                    urls.append(requirement.url)
        self.options['eggs'] = "\n".join(sorted(set(eggs)))
        self.options['urls'] = "\n".join(sorted(set(urls)))
        versions_part_name = self.options.get('versions')
        if versions_part_name:
            versions_part = self.buildout[versions_part_name]
            for egg, version in versions:
                versions_part.setdefault(egg, version)

    def parse_files(self, files):
        """Parse files."""
        return itertools.chain.from_iterable((self.parse_file(file) for file in files))

    def parse_file(self, file):
        """Parse single file."""
        try:
            file_dir = os.path.dirname(file)
            if os.path.exists(file_dir):
                os.chdir(file_dir)
            try:
                return req.parse_requirements(file, options=self, finder=self, session=PipSession())
            finally:
                os.chdir(self.buildout['buildout']['directory'])
        except SystemExit:
            raise RuntimeError("Can't parse {0}".format(file))

    update = install
