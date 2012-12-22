Overview
========

This recipe allows to parse pip configuration files (usually named requirements.txt) into just list of the eggs to use
in other parts of the buildout.

The recipe mirrors the parsed eggs list into its section, so that e.g.
``${pip:eggs}`` will give the list of parsed eggs.

For now single option of the recipe is ``configs`` - list of config files to parse.

The config files are parsed during the initialization of the ``Recipe`` instance,
i.e. after ``buildout.cfg`` is read but before any recipe is installed or updated.

Example usage: Use an environment variable
==========================================

Let's create test config files

    >>> write('requirements.txt',
    ... """
    ... some.egg
    ... -e http://some.package.git.url#egg=develop.egg
    ... """)

    >>> write('requirements2.txt',
    ... """
    ... some2.egg
    ... -e http://some2.package.git.url#egg=develop2.egg
    ... """)


We'll start by creating a buildout that uses the recipe::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = pip print
    ...
    ... [some-section]
    ... eggs = ${pip:eggs}
    ...
    ... [pip]
    ... recipe = collective.recipe.pip
    ... configs = requirements.txt
    ...           requirements2.txt
    ...
    ... [print]
    ... recipe = mr.scripty
    ... install =
    ...     ... print self.buildout['some-section']['eggs']
    ...     ... return []
    ... """)

The `mr.scripty`_ recipe is used to print out the value of the ${some-section:some-option}
option.

Running the buildout gives us::

    >>> print 'start', system(buildout)
    start...
    some.egg
    develop.egg
    some2.egg
    develop2.egg
    <BLANKLINE>