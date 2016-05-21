# -*- coding: utf-8 -*-
"""Recipe pip."""
import itertools
import os

from pip import req
try:
    from pip.download import PipSession
    has_pipsession = True
except ImportError:
    has_pipsession = False


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
        self.format_control = None
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
        for _req in self.parse_files(self.options.get('configs').split()):
            requirement = DownloadedReq(_req)
            if requirement.req is not None:
                if hasattr(requirement.req, 'specs'):
                    version_spec = requirement.req.specs
                else:
                    version_spec = [(spec.operator, spec.version) for spec in requirement.req.specifier]
                specs = ','.join([''.join(s) for s in version_spec])
                eggs.append(requirement.name + specs)
            else:
                specs = None
            if specs:
                versions.append((requirement.name, specs[2:] if specs.startswith('=') else specs))
            if requirement.editable:
                urls.append(requirement.url)
            elif requirement.url:
                if '#egg=' not in requirement.url:
                    urls.append('{0}#egg={1}{2}'.format(requirement.url, requirement.name, specs))
                else:
                    urls.append(requirement.url)

        # Buildout Option values must be strings
        self.options['eggs'] = "\n".join(sorted(set(eggs))).encode('utf-8')
        self.options['urls'] = "\n".join(sorted(set(urls))).encode('utf-8')
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
                if has_pipsession:
                    return req.parse_requirements(file, options=self, finder=self,
                                                  session=PipSession())
                else:
                    return req.parse_requirements(file, options=self, finder=self)
            finally:
                os.chdir(self.buildout['buildout']['directory'])
        except SystemExit:
            raise RuntimeError("Can't parse {0}".format(file))

    update = install


class DownloadedReq(object):
    """A wrapper around InstallRequirement"""

    def __init__(self, req):
        self._req = req

    def __getattr__(self, attr):
        return getattr(self._req, attr)

    def _link(self):
        try:
            return self._req.link
        except AttributeError:
            # The link attribute isn't available prior to pip 6.1.0, so fall
            # back to the now deprecated 'url' attribute.
            return self._req.url if self._req.url else None

    @property
    def url(self):
        link = self._link()
        return link.url if link else None
