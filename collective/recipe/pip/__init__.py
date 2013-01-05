# -*- coding: utf-8 -*-
"""Recipe pip."""
import os
import itertools

class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.options = options
        self.buildout = buildout
        self.process()

    def install(self):
        """Installer"""
        return tuple()

    def process(self):
        """Process everything"""
        eggs = []
        versions = []
        for token in self.parse_files(self.options.get('configs').split()):
            #save fixed versions
            egg = version = None
            try:
                egg, version = token.split('==')
            except ValueError:
                try:
                    egg, version = token.split('>')
                    version = '>' + version
                except ValueError:
                    pass
            eggs.append(token)
            if version:
                versions.append((egg, version))

        self.options['eggs'] = "\n".join(eggs)
        versions_part_name = self.options.get('versions')
        if versions_part_name:
            versions_part = self.buildout[versions_part_name]
            for egg, version in versions:
                versions_part.setdefault(egg, version)

    def parse_files(self, files):
        """Parse files."""
        return itertools.chain.from_iterable(itertools.imap(self.parse_file, files))

    def parse_file(self, file):
        """Parse single file."""
        return itertools.chain.from_iterable(itertools.imap(self.parse_line, open(file).xreadlines()))

    def parse_line(self, line):
        """Parse single line."""
        if any(map(line.startswith, ('#', '-f'))):
            raise StopIteration()

        for token in line.split():
            yield self.parse_token(token)

    def parse_token(self, token):
        """Parse single token"""
        if token and not token[0] in ('-', '#'):
            if '#egg=' in token:
                return token.split('#egg=')[1]
            if '#' in token:
                raise StopIteration()
            return token
        raise StopIteration()

    update = install

