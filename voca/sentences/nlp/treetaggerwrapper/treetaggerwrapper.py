#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
About treetaggerwrapper
=======================

:author: Laurent Pointal <laurent.pointal@limsi.fr> <laurent.pointal@laposte.net>
:organization: CNRS - LIMSI
:copyright: CNRS - 2004-2019
:license: GNU-GPL Version 3 or greater
:version: 2.3

For language independent part-of-speech tagger TreeTagger,
see `Helmut Schmid TreeTagger site`_.

.. _Helmut Schmid TreeTagger site: http://www.ims.uni-stuttgart.de/projekte/corplex/TreeTagger/DecisionTreeTagger.html

For this module, see `Developer Project page`_ and `Project Source repository`_
on french academic repository SourceSup. And `Module Documentation`_ on Read The Docs.

.. _Developer  Project page: https://perso.limsi.fr/pointal/dev:treetaggerwrapper
.. _Project Source repository: https://sourcesup.renater.fr/projects/ttpw/
.. _Module Documentation: https://treetaggerwrapper.readthedocs.io/en/latest/

You can also retrieve the latest version of this module with the svn command::

    svn export https://subversion.renater.fr/ttpw/trunk/treetaggerwrapper.py

Or install it (and the module treetaggerpoll.py) using pip (add pip install option
:option:`--user` for user private installation)::

    pip install treetaggerwrapper

This wrapper tool is intended to be used in projects where multiple
chunk of texts must be processed via TreeTagger in an automatic
way (else you may simply use the base TreeTagger installation once as
an external command).

.. warning:: Parameter files renaming.

   Latest distributed files on TreeTagger site removed :code:`-utf8` part from
   parameter files names.
   This version 2.3 ot the wrapper tries to adapt to your installed version
   of TreeTagger: test existence of :code:`.par` file without :code:`-utf8` part, and if it
   failed, test existence of file with adding :code:`-utf8` part.

   If you use this wrapper, a small email would be welcome to support
   module maintenance (where, purpose, funding…).
   Send it to laurent.pointal@limsi.fr

Installation
============

Requirements
------------

``treetaggerwrapper`` rely on :mod:`six` module for Python2 and Python3
compatibility. It also uses standard :mod:`io` module for files reading with
decoding / encoding .

Tests have been limited to Python 2.7 and Python 3.4 under Linux and Windows.
It don't work with earlier version of Python as some names are not defined in
their standard libraries.

Automatic
---------

As the module is now registered on `PyPI`_, you can simply install it::

  pip install treetaggerwrapper

Or, if you can't (or don't want) to install the module system-wide (and don't
use a `virtual env`_)::

   pip install --user treetaggerwrapper

May use ``pip3`` to go with your Python3 installation.

.. _PyPI: https://pypi.python.org/pypi/treetaggerwrapper
.. _virtual env: https://virtualenv.pypa.io/en/latest/

If it is already installed as a package, use pip's install :option:`-U` option
to install the last version (update).

Manual
------

For a complete manual installation, install :mod:`six` module and other
dependencies, and simply put the :file:`treetaggerwrapper.py`
and :file:`treetaggerpoll.py` files in a
directory listed in the Python path (or in your scripts directory).

Configuration
=============

The wrapper search for the treetagger directory
(the one with :file:`bin`, :file:`lib` and :file:`cmd` subdirectories),
in several places, allowing variations in TreeTagger directory name
— see _`TreeTagger automatic locate` for details.

If the treetagger directory is found, its location is stored in a file
:file:`$HOME/.config/treetagger_wrapper.cfg` (or any place following
:envvar:`XDG_CONFIG_DIR` if it is specified),
and at next start the directory indicated in this file is used if it
still exists.

If you installed TreeTagger in a non-guessable location, you still can set up
an environment variable :envvar:`TAGDIR` to reference the
TreeTagger software installation directory, or give a `TAGDIR` named argument
when building a :class:`TreeTagger` object to provide this information,
or simply put that information into configuration file in section ``[CACHE]``
under key ``tagdir = …``.


Usage
=====

Primary usage is to wrap TreeTagger binary and use it as a functional tool.
You have to build a :class:`TreeTagger` object, specifying the target
language [by its country code!], and possibly some other TreeTagger parameters
(else we use standard files specified in the module for each supported language).
Once this wrapper object created, you can simply call its :any:`tag_text()`
method with the string to tag, and it will return a list of lines corresponding
to the text tagged by TreeTagger.

Example (with Python3, **Unicode strings** by default — with Python2 you
need to use explicit notation ``u"string"``, of if within a script start by a
:code:`from __future__ import unicode_literals` directive)::

    >>> import pprint   # For proper print of sequences.
    >>> import treetaggerwrapper
    >>> #1) build a TreeTagger wrapper:
    >>> tagger = treetaggerwrapper.TreeTagger(TAGLANG='en')
    >>> #2) tag your text.
    >>> tags = tagger.tag_text("This is a very short text to tag.")
    >>> #3) use the tags list... (list of string output from TreeTagger).
    >>> pprint.pprint(tags)
    ['This\tDT\tthis',
     'is\tVBZ\tbe',
     'a\tDT\ta',
     'very\tRB\tvery',
     'short\tJJ\tshort',
     'text\tNN\ttext',
     'to\tTO\tto',
     'tag\tVV\ttag',
     '.\tSENT\t.']
    >>> # Note: in output strings, fields are separated with tab chars (\t).


You can transform it into a list of named tuples ``Tag``, ``NotTag``
(unknown tokens) ``TagExtra`` (token having extra informations requested
via tagger options - like probabilistic indications) using the helper
:func:`make_tags` function::

    >>> tags2 = treetaggerwrapper.make_tags(tags)
    >>> pprint.pprint(tags2)
    [Tag(word='This', pos='DT', lemma='this'),
     Tag(word='is', pos='VBZ', lemma='be'),
     Tag(word='a', pos='DT', lemma='a'),
     Tag(word='very', pos='RB', lemma='very'),
     Tag(word='short', pos='JJ', lemma='short'),
     Tag(word='text', pos='NN', lemma='text'),
     Tag(word='to', pos='TO', lemma='to'),
     Tag(word='tag', pos='VV', lemma='tag'),
     Tag(word='.', pos='SENT', lemma='.')]


You can also directly process files using :meth:`TreeTagger.tag_file` and
:meth:`TreeTagger.tag_file_to` methods.

The module itself can be used as a command line tool too, for more information
ask for module help::

    python treetaggerwrapper.py --help

If available within :envvar:`PYTHONPATH`, the module can also be called
from anywhere with the :option:`-m` Python option::

    python -m treetaggerwrapper --help


Important modifications notes
=============================

On august 2015, the module has been reworked deeply, some
modifications imply modifications in users code.

- **Methods renamed** (and functions too) to follow Python rules,
  they are now lowercase
  with underscore separator between words.
  Typically for users, ``tt.TagText()`` becomes ``tt.tag_text()``
  (for this method a compatibility method has been written, but
  no longer support lists of non-Unicode strings).

- Work with Python2 and Python3, with same code.

- Use **Unicode strings** internally (it's no more possible to provide
  binary strings and their encoding as separated
  parameters - you have to decode the strings yourself before calling
  module functions).

- Assume **utf-8** when dealing with *TreeTagger binary*, default to its utf-8
  versions of parameter and abbrev files. If you use another encoding,
  you must specify these files: in your sources, or via environment
  vars, or in the :file:`treetagger_wrapper.cfg` configuration file under
  encoding name section (respecting Python encoding names as given by
  ``codecs.lookup(enc).name``, ie. uses ``utf-8``).

- Default to **utf-8** when reading *user files* (you need to specify latin1
  if you use such encoding - previously it was the default).

- **Guess TreeTagger location** — you can still provide :envvar:`TAGDIR` as
  environment variable or as :class:`TreeTagger` parameter,
  but it's no more necessary.
  Found directory is cached in :file:`treetagger_wrapper.cfg` configuration
  file to only guess once.

- Documentation has been revised to only export main things for module usage;
  internals stay documented via comments in the source.

- **Text chunking** (tokenizing to provide treetagger input)
  has been revisited and must be more efficient.
  And you can now also provide your own external chunking function when
  creating the wrapper — which will replace internal chunking in the whole
  process.

- XML tags generated have been modified (made shorted and with ``ttpw:``
  namespace).

- Can be used in **multithreading** context (pipe communications with TreeTagger
  are protected by a Lock, preventing concurrent access).
  If you need multiple parallel processing, you can create multiple
  :class:`TreeTagger` objects, put them in a poll, and work with them
  from different threads.

- Support polls of taggers for optimal usage on multi-core computers.
  See :class:`treetaggerwrapper.TaggerPoll` class for thread poll
  and :class:`treetaggerpoll.TaggerProcessPoll` class for process poll.

Processing
==========

This module does two main things
--------------------------------

- Manage preprocessing of text (chunking to extract tokens for treetagger
  input) in place of external Perl scripts as in base TreeTagger installation,
  thus avoid starting Perl each time a piece of text must be tagged.

- Keep alive a pipe connected to TreeTagger process, and use that pipe
  to send data and retrieve tags, thus avoid starting TreeTagger each
  time and avoid writing / reading temporary files on disk (direct
  communication via the pipe). Ensure flushing of tagger output.

Supported languages
^^^^^^^^^^^^^^^^^^^

.. note:: Encoding specification

   When specifying language with treetaggerwrapper, we use the the two
   chars language codes, not the complete language name.

This module support chunking (tokenizing) + tagging for languages:

- spanish (es)
- french (fr)
- english (en)
- german (de)

It can be used for tagging only for languages:

- bulgarian (bg)
- dutch (nl)
- estonian (et)
- finnish (fi)
- galician (gl)
- italian (it)
- korean (kr)
- latin (la)
- mongolian (mn)
- polish (pl)
- russian (ru)
- slovak (sk')
- swahili (sw)

Note: chunking parameters have not been adapted to these language
and their specific features, you may try to chunk with default processing…
with no guaranty.
If you have an external chunker, you can call the tagger with
option ``tagonly`` set to True, you should then provide a simple
string with one token by line (or list of strings with one token
by item).
If you chunker is a callable, you can provide your own chunking function
with :option:`CHUNKERPROC` named parameter when constructing :class:`TreeTagger`
object, and then use it normally (your function is called in place of
standard chunking).


For all these languages, the wrapper use standard filenames for
TreeTagger's parameter and abbreviation files.
You can override these names using :option:`TAGPARFILE` and
:option:`TAGABBREV` parameters, and then use alternate files.

Other things done by this module
--------------------------------

- Can number lines into XML tags (to identify lines after TreeTagger
  processing).
- Can mark whitespaces with XML tags.
- By default replace non-talk parts like URLs, emails, IP addresses,
  DNS names (can be turned off). Replaced by a 'replaced-xxx' string
  followed by an XML tag containing the replaced text as attribute
  (the tool was originally used to tag parts of exchanges from technical
  mailing lists, containing many of these items).
- Acronyms like U.S.A. are systematically written with a final dot,
  even if it is missing in original file.
- Automatic encode/decode files using user specified encoding (default
  to utf-8).

In normal mode, all journal outputs are done via Python standard logging system,
standard output is only used if a) you run the module in pipe mode (ie.
results goes to stdout), or b) you set DEBUG or DEBUG_PREPROCESS global
variables and you use the module directly on command line (which make journal
and other traces to be sent to stdout).

For an example of logging use, see :func:`enable_debugging_log` function.

Alternative tool
----------------

You may also take a look at project `treetagger python`_
which wraps TreeTagger command-line tools (simpler than
this module, it may be slower if you have many texts
to tag in your process as it calls and restarts TreeTagger
chunking then tagging tools chain for each text).

.. _treetagger python: https://github.com/miotto/treetagger-python/blob/master/treetagger.py


Hints
=====

Window buffer overflow
----------------------

On windows, if you get the following error about some file manipulation (ex. in an
:func:`abspath` call)::

    TypeError: must be (buffer overflow), not str

Check that directories and filenames total length don't exceed 260 chars.
If this is the case, you may try to use UNC names starting by ``\\?\`` (read Microsoft
`Naming Files, Paths, and Namespaces`_ documentation — note: you cannot use ``/``
to separate directories with this notation).


.. _Naming Files, Paths, and Namespaces: https://msdn.microsoft.com/en-us/library/windows/desktop/aa365247.aspx


TreeTagger automatic location
-----------------------------

For your TreeTagger to be automatically find by the script, its **directory**
must follow installation rules below:

Directory naming and content
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Location search function tries to find a directory beginning with ``tree``,
possibly followed by any char (ex. a space, a dash…), followed
by ``tagger``, possibly followed by any sequence of chars (ex. a
version number), and without case distinction.

This match directory names like ``treetagger``, ``TreeTagger``, ``Tree-tagger``,
``Tree Tagger``, ``treetagger-2.0``…

The directory must contain :file:`bin` and :file:`lib` subdirectories
(they are normally created by TreeTagger installation script, or directly
included in TreeTagger Windows zipped archive).

First directory corresponding to these criteria is considered to
be the TreeTagger installation directory.

Searched locations
^^^^^^^^^^^^^^^^^^

TreeTagger directory location is searched from local (user private installation)
to global (system wide installation).

1. Near the :file:`treetaggerwrapper.py` file (TreeTagger being in same directory).
2. Containing the :file:`treetaggerwraper.py` file (module inside TreeTagger directory).
3. User home directory (ex. :file:`/home/login`, :file:`C:\\Users\\login`).
4. First level directories in user home directory (ex. :file:`/home/login/tools`,
   :file:`C:\\Users\\login\\Desktop`).
5. For MacOSX, in :file:`~/Library/Frameworks`.
6. For Windows, in program files directories (ex. :file:`C:\\Program Files`).
7. For Windows, in each existing fixed disk root and its first level directories
   (ex. :file:`C:\\`, :file:`C:\\Tools`, :file:`E:\\`, :file:`E:\\Apps`).
8. For Posix (Linux, BSD… MacOSX), in a list of standard directories:

   - :file:`/usr/bin`,
   - :file:`/usr/lib`,
   - :file:`/usr/local/bin`,
   - :file:`/usr/local/lib`,
   - :file:`/opt`,
   - :file:`/opt/bin`,
   - :file:`/opt/lib`,
   - :file:`/opt/local/bin`,
   - :file:`/opt/local/lib`.

9. For MacOSX, in applications standard directories:

   - :file:`/Applications`,
   - :file:`/Applications/bin`,
   - :file:`/Library/Frameworks`.

TreeTagger probabilities
------------------------

Using :option:`TAGOPT` parameter when constructing :class:`TreeTagger` object,
you can provide :option:`-threshold` and :option:`-prob` parameters
to the treetagger process, and then retrieve probability informations
in the tagger output (see TreeTagger README file for all options).

    >>> import treetaggerwrapper as ttpw
    >>> tagger = ttpw.TreeTagger(TAGLANG='fr', TAGOPT="-prob -threshold 0.7 -token -lemma -sgml -quiet")
    >>> tags = tagger.tag_text('Voici un petit test de TreeTagger pour voir.')
    >>> import pprint
    >>> pprint.pprint(tags)
    ['Voici\tADV voici 1.000000',
    'un\tDET:ART un 0.995819',
    'petit\tADJ petit 0.996668',
    'test\tNOM test 1.000000',
    'de\tPRP de 1.000000',
    'TreeTagger\tNAM <unknown> 0.966699',
    'pour\tPRP pour 0.663202',
    'voir\tVER:infi voir 1.000000',
    '.\tSENT . 1.000000']
    >>> tags2 = ttpw.make_tags(tags, allow_extra=True)
    >>> pprint.pprint(tags2)
    [TagExtra(word='Voici', pos='ADV', lemma='voici', extra=(1.0,)),
    TagExtra(word='un', pos='DET:ART', lemma='un', extra=(0.995819,)),
    TagExtra(word='petit', pos='ADJ', lemma='petit', extra=(0.996668,)),
    TagExtra(word='test', pos='NOM', lemma='test', extra=(1.0,)),
    TagExtra(word='de', pos='PRP', lemma='de', extra=(1.0,)),
    TagExtra(word='TreeTagger', pos='NAM', lemma='<unknown>', extra=(0.966699,)),
    TagExtra(word='pour', pos='PRP', lemma='pour', extra=(0.663202,)),
    TagExtra(word='voir', pos='VER:infi', lemma='voir', extra=(1.0,)),
    TagExtra(word='.', pos='SENT', lemma='.', extra=(1.0,))]

.. note::

    This provides extra data for each token, your script must be adapted for
    this (you can note in the pprint formated display that we have tab and
    space separators — a tab after the word, then spaces between items).

"""

from __future__ import print_function
# Following import prevent working with Python < 2.6 !
from __future__ import unicode_literals

# To allow use of epydoc documentation generation with reStructuredText markup.
# Note that use of sphinx 1.3 :any: role may broke epydoc (not tested).
__docformat__ = "restructuredtext en"

__version__ = '2.3'

# Note: I use re.VERBOSE option everywhere to allow spaces and comments into
#       regular expressions (more readable). And (?:...) allow to have
#       semantic groups of things in the expression but no submatch group
#       corresponding in the match object.
# ==============================================================================
__all__ = ["TreeTaggerError", "TreeTagger", "Tag", "make_tags"]

import codecs
import collections
import copy
from six.moves import configparser
import getopt
import glob
import io
import logging
import multiprocessing
import os
import os.path as osp
import platform
from six.moves import queue
import re
import shlex
import six
import string
import subprocess
import sys
import threading
import time

if six.PY2:
    # Under Python2 a permission denied error raises an OSError
    # with errno 13.
    PermissionError = OSError

# Set to enable debugging code (mainly logs).
DEBUG = 0

# Set to enable preprocessing specific debugging code.
DEBUG_PREPROCESS = 0

# Set to enable multithreading specific debugging code.
DEBUG_MULTITHREAD = 0

# Extension added to result files when using command-line.
# (TreeTagger result => ttr)
RESEXT = "ttr"

# We don't print for errors/warnings, we use Python logging system.
logger = logging.getLogger("TreeTagger")
# Avoid No handlers could be found for logger "TreeTagger" message.
logger.addHandler(logging.NullHandler())

# A tag to identify begin/end of a text in the data flow.
# (avoid to restart TreeTagger process each time)
STARTOFTEXT = "<ttpw:start-text />"
ENDOFTEXT = "<ttpw:end-text />"
# A tag to identify line numbers from source text.
NUMBEROFLINE = '<ttpw:line num="{}" />'
# And tags to identify location of whitespaces in source text.
TAGSPACE = "<ttpw:space />"
TAGTAB = "<ttpw:tab />"
TAGLF = "<ttpw:lf />"
TAGCR = "<ttpw:cr />"
TAGVT = "<ttpw:vt />"
TAGFF = "<ttpw:ff />"

# Default input and output for files and strings with no ecoding specified.
USER_ENCODING = "utf-8"

# Identify running plaftorm once.
ON_WINDOWS = (platform.system() == "Windows")
ON_MACOSX = (platform.system() == "Darwin")
ON_POSIX = (os.name == "posix")  # Care: true also under MACOSX.

# Extra configuration storage within a config file.
g_config = configparser.SafeConfigParser()

# The config file is stored following XDG rules.
CONFIG_FILENAME = "treetagger_wrapper.cfg"

# Sgml tags for replaced data (when kept in text).
REPLACED_URL_TAG = '<repurl text="{}" />'
REPLACED_EMAIL_TAG = '<repemail text="{}" />'
REPLACED_IP_TAG = '<repip text="{}" />'
REPLACED_DNS_TAG = '<repdns text="{}" />'

# Timeout in case of problem with the tagger process (used when reading).
TAGGER_TIMEOUT = 30

# ==============================================================================
# ALONEMARKS:
#   chars which must be kept alone, they must have spaces around them to make
#   them tokens (this is done by pre-processing text to chunks.
# Notes: chars from ALONEMARKS may be in pchar or fchar too, to identify
#   punctuation after a fchar.
# See Unicode database…
ALONEMARKS = "!?¿;\"«»“”´`¨,*¤@°:%|¦/" \
             "()[\\]{}<>«»\u008b\u009b\u0093" \
             "&~=±×\226\227" \
             "\t\n\r" \
             "\u2014\u203E\u0305\u2012\u2013" \
             "£¥$€©®"

NUMBER_EXPRESSION = r"""(
                    [-+]?[0-9]+(?:[.,][0-9]*)?(?:[eE][-+]?[0-9]+)?
                        |
                    [-+]?[.,][0-9]+(?:[eE][-+]?[0-9]+)?
                )"""

# Langage support.
# Dictionnary g_langsupport is indexed by language code (en, fr, de...).
# Each language code has a dictionnary as value, with corresponding entries:
#   tagparfile: name of the TreeTagger language file in TreeTagger lib dir.
#   abbrevfile: name of the abbreviations text file in TreeTagger lib dir.
#   encoding: encoding to use with TreeTagger, accordingly to these files.
#   pchar: characters which have to be cut off at the beginning of a word.
#          must be usable into a [] regular expression part.
#   fchar: characters which have to be cut off at the end of a word.
#          must be usable into a [] regular expression part.
#   pclictic: character sequences which have to be cut off at the beginning
#               of a word.
#   fclictic: character sequences which have to be cut off at the end of
#               a word.L
#   number: representation of numbers in the language.
#          must be a full regular expression for numbers.
#   dummysentence: a language valid sentence (sent to ensure that TreeTagger
#          push remaining data). Sentence must only contain words and spaces
#          (even spaces between punctuation as string is simply splitted
#          on whitespaces before being sent to TreeTagger.
#   replurlexp: regular expression subtitution string for URLs.
#   replemailexp: regular expression subtitution string for emails.
#   replipexp: regular expression subtitution string for IP addresses.
#   repldnsexp: regular expression subtitution string for DNS names.
g_langsupport = {
    "__base__": {
        "encoding": "utf-8",
        "tagparfile": "",
        "abbrevfile": "",
        "pchar": ALONEMARKS + "'",
        "fchar": ALONEMARKS + "'",
        "pclictic": "",
        "fclictic": "",
        "number": NUMBER_EXPRESSION,
        "dummysentence": " .",  # Just a final sentence dot.
        "replurlexp": 'replaced-url',
        "replemailexp": 'replaced-email',
        "replipexp": 'replaced-ip',
        "repldnsexp": 'replaced-dns'
    },
    "en": {
        "encoding": "utf-8",
        "tagparfile": "english.par",
        "abbrevfile": "english-abbreviations",
        "pchar": ALONEMARKS + "'",
        "fchar": ALONEMARKS + "'",
        "pclictic": "",
        "fclictic": "'(s|re|ve|d|m|em|ll)|n't",
        "number": NUMBER_EXPRESSION,
        "dummysentence": "This is a dummy sentence to ensure data push . .",
        "replurlexp": 'replaced-url',
        "replemailexp": 'replaced-email',
        "replipexp": 'replaced-ip',
        "repldnsexp": 'replaced-dns'
    },
    "fr": {
        "encoding": "utf-8",
        "tagparfile": "french.par",
        "abbrevfile": "french-abbreviations-utf8",
        "pchar": ALONEMARKS + "'",
        "fchar": ALONEMARKS + "'",
        "pclictic": "[dcjlmnstDCJLNMST]'|[Qq]u'|[Jj]usqu'|[Ll]orsqu'",
        "fclictic": "'-t-elles|-t-ils|-t-on|-ce|-elles|-ils|-je|-la|"
                    "-les|-leur|-lui|-mêmes|-memes|-même|-meme|-m'|-moi|-on|-toi|-tu|-t'|"
                    "-vous|-en|-y|-ci|-là|-la",
        "number": NUMBER_EXPRESSION,
        "dummysentence": "Cela est une phrase inutile pour assurer la "
                         "transmission des données . .",
        "replurlexp": 'url-remplacée',
        "replemailexp": 'email-remplacé',
        "replipexp": 'ip-remplacée>',
        "repldnsexp": 'dns-remplacé'
    },
    "de": {
        "encoding": "utf-8",
        "tagparfile": "german.par",
        "abbrevfile": "german-abbreviations-utf8",
        "pchar": ALONEMARKS + "'",
        "fchar": ALONEMARKS + "'",
        "pclictic": "",
        "fclictic": "'(s|re|ve|d|m|em|ll)|n't",
        "number": NUMBER_EXPRESSION,
        "dummysentence": "Das ist ein Testsatz um das Stossen der "
                         "daten sicherzustellen . .",
        "replurlexp": 'replaced-url',
        "replemailexp": 'replaced-email',
        "replipexp": 'replaced-ip',
        "repldnsexp": 'replaced-dns'
    },
    "es": {
        "encoding": "utf-8",
        "tagparfile": "spanish.par",
        "abbrevfile": "spanish-abbreviations",
        "pchar": ALONEMARKS + "'",
        "fchar": ALONEMARKS + "'",
        "pclictic": "",
        "fclictic": "",
        "number": NUMBER_EXPRESSION,
        "dummysentence": "Quiero darle las gracias a usted y explicar un "
                         "malentendido . .",
        "replurlexp": 'sustituir-url>',
        "replemailexp": 'sustituir-email',
        "replipexp": 'sustituir-ip',
        "repldnsexp": 'sustituir-dns'
    },
}
# For other languages, we provide a way to call TreeTagger, but
# we currently cannot provide pre-processing (chunking).
for name, lang in [
    ('bulgarian', 'bg'),
    ('dutch', 'nl'),
    ('estonian', 'et'),
    ('finnish', 'fi'),
    ('galician', 'gl'),
    ('italian', 'it'),
    ('korean', 'kr'),
    ('latin', 'la'),
    ('mongolian', 'mn'),
    ('polish', 'pl'),
    ('russian', 'ru'),
    ('slovak', 'sk'),
    ('swahili', 'sw')]:
    ls = g_langsupport[lang] = copy.deepcopy(g_langsupport['__base__'])
    if lang in ('la', 'mn', 'sw'):
        ls['encoding'] = 'latin-1'
        ls['tagparfile'] = name + '.par'
        ls['abbrevfile'] = name + '-abbreviations'
    else:  # __base__ has 'encoding' utf8
        ls['tagparfile'] = name + '.par'
        ls['abbrevfile'] = name + '-abbreviations-utf8'
# "C'est la fin ." (+google translate…) - in case someone tries to use
# the module for chunking an officially unsupport language.
g_langsupport['bg']['dummysentence'] = 'Това е края . .'
g_langsupport['nl']['dummysentence'] = 'Dit is het einde . .'
g_langsupport['et']['dummysentence'] = 'See on lõpuks . .'
g_langsupport['fi']['dummysentence'] = 'Tämä on loppu . .'
g_langsupport['gl']['dummysentence'] = 'Este é o final . .'
g_langsupport['it']['dummysentence'] = 'Questa è la fine . .'
g_langsupport['kr']['dummysentence'] = '끝 이 야 . .'
g_langsupport['la']['dummysentence'] = 'Hoc est finis . .'
g_langsupport['mn']['dummysentence'] = 'Энэ нь эцсийн байна . .'
g_langsupport['pl']['dummysentence'] = 'To jest koniec . .'
g_langsupport['ru']['dummysentence'] = 'Это конец . .'
g_langsupport['sk']['dummysentence'] = 'To je koniec . .'
g_langsupport['sw']['dummysentence'] = 'Hii ni mwisho . .'

g_langsupport['it']['pclictic'] = "[dD][ae]ll'|[nN]ell'|[Aa]ll'|[lLDd]'|[Ss]ull'|" \
                                  "[Qq]uest'|[Uu]n'|[Ss]enz'|[Tt]utt'"
g_langsupport['gl']['fclictic'] = "-la|-las|-lo|-los|-nos"


# We consider following rules to apply whatever be the language.
# ... is an ellipsis, put spaces around before splitting on spaces
# (make it a token)
ellipfind_re = re.compile(r"((?:\.\.\.)|…)")
ellipfind_subst = " ... "
# A regexp to put spaces if missing after alone marks.
punct1find_re = re.compile("([" + ALONEMARKS + "])([^ ])",
                           re.IGNORECASE | re.VERBOSE)
punct1find_subst = "\\1 \\2"
# A regexp to put spaces if missing before alone marks.
punct2find_re = re.compile("([^ ])([[" + ALONEMARKS + "])",
                           re.IGNORECASE | re.VERBOSE)
punct2find_subst = "\\1 \\2"
# A regexp to identify acronyms like U.S.A. or U.S.A (written to force
# at least two chars in the acronym, and the final dot optionnal).
#acronymexpr_re = re.compile("^[a-zA-Z]+(\.[a-zA-Z])+\.?$",
# Change regexp to math any Unicode alphabetic (and allow diacritic marks
# on the acronym).
acronymexpr_re = re.compile(r"^[^\W\d_-]+(\.[^\W\d_-])+\.?$",
                            re.IGNORECASE | re.VERBOSE | re.UNICODE)


# ==============================================================================
class TreeTaggerError(Exception):
    """For exceptions generated directly by TreeTagger wrapper.
    """
    pass


# ==============================================================================
Tag = collections.namedtuple("Tag", "word pos lemma")
"""
A named tuple build by :func:`make_tags` to process :meth:`TreeTagger.tag_text`
output and get fields with meaning.
"""

TagExtra = collections.namedtuple("TagExtra", "word pos lemma extra")
"""
A named tuple build by :func:`make_tags` to process :meth:`TreeTagger.tag_text`
output and get fields with meaning when there are extra informations.
"""

NotTag = collections.namedtuple("NotTag", "what")
"""
A named tuple built by :func:`make_tags` when a TreeTagger output cannot
match a Tag.
"""


class FinalPart(object):
    """Used to wrap final texts, avoid re-trying to analyze them.
    """
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return repr(self.text)

    def __str__(self):
        return self.text


# ==============================================================================
def pipe_writer(pipe, text, flushsequence, encoding, errors):
    """Write a text to a pipe and manage pre-post data to ensure flushing.

    For internal use.

    If text is composed of str strings, they are written as-is (ie. assume
    ad-hoc encoding is providen by caller). If it is composed of unicode
    strings, then they are converted to the specified encoding.

    :param  pipe: the Popen pipe on what to write the text.
    :type   pipe: Popen object (file-like with write and flush methods)
    :param  text: the text to write.
    :type   text: string or list of strings
    :param  flushsequence: lines of tokens to ensure flush by TreeTagger.
    :type   flushsequence: string (with \\n between tokens)
    :param  encoding: encoding of texts written on the pipe.
    :type   encoding: str
    :param  errors: how to manage encoding errors: strict/ignore/replace.
    :type  errors: str
    """
    try:
        # Warn the user of possible bad usage.
        if not text:
            logger.warning("Requested to tag an empty text.")
            # We continue to unlock the thread waiting for the ENDOFTEXT on
            # TreeTagger output.

        logger.info("Writing starting part to pipe.")
        pipe.write((STARTOFTEXT + "\n").encode(encoding, errors))

        logger.info("Writing data to pipe.")

        if text:
            if isinstance(text, six.string_types):
                # Typically if called without pre-processing.
                if isinstance(text, six.text_type):
                    text = text.encode(encoding, errors)
                pipe.write(text)
                if text[-1] != '\n':
                    pipe.write("\n".encode(encoding, errors))
            else:
                assert isinstance(text, list)
                # Typically when we have done pre-processing.
                for line in text:
                    if isinstance(line, six.text_type):
                        line = line.encode(encoding, errors)
                    pipe.write(line)
                    pipe.write("\n".encode(encoding, errors))

        logger.info("Writing ending and flushing part to pipe.")
        # Note: ENDOFTEXT is a str - no encoding (basic ASCII).
        pipe.write((ENDOFTEXT + "\n.\n" + flushsequence + "\n").encode(encoding, errors))
        pipe.flush()
        logger.info("Finished writing data to pipe. Pipe flushed.")
    except:
        logger.error("Failure during pipe writing.", exc_info=True)


# ==============================================================================
class TreeTagger(object):
    """Wrap TreeTagger binary to optimize its usage on multiple texts.

    The two main methods you may use are the :meth:`__init__` initializer,
    and the :meth:`tag_text` method to process your data and get TreeTagger
    output results.
    """
    __internals_doc = """
    :ivar   lang: language to use for tagging.
    :type   lang: string
    :ivar   langsupport: dictionnary of language specific values (ref. to
                        g_langsupport[lang] dictionnary).
    :type   langsupport: dict
    :ivar   tagdir: path to directory of installation of TreeTagger.
                    Set via TAGDIR env. var or construction param, else
                    guess by :func:`locate_treetagger` function.
    :type   tagdir: string
    :ivar   tagbindir: path to binary dir into TreeTagger dir.
    :type   tagbindir: string
    :ivar   taglibdir: path to libraries dir into TreeTagger dir.
    :type   taglibdir: string
    :ivar   tagbin: path to TreeTagger binary file (used to launch process).
    :type   tagbin: string
    :ivar   tagopt: command line options for TreeTagger.
    :type   tagopt: string
    :ivar   tagparfile: path to TreeTagger library file.
    :type   tagparfile: string
    :ivar   abbrevfile: path to abbreviations file.
    :type   abbrevfile: string
    :ivar   taginencoding: encoding to use for TreeTagger input encoding.
    :type   taginencoding: str
    :ivar   tagoutencoding: encoding to use for TreeTagger output decoding.
    :type   tagoutencoding: str
    :ivar   taginencerr: management of encoding errors for TreeTagger input.
    :type   taginencerr: str
    :ivar   tagoutencerr: management of encoding errors for TreeTagger output.
    :type   tagoutencerr: str
    :ivar   abbterms: dictionnary of abbreviation terms for fast lookup.
                    Filled when reading abbreviations file.
    :type   abbterms: dict  [ form ] ==> term
    :ivar   pchar: characters which have to be cut off at the beginning of
                a word.
                Filled from g_langsupport dict.
    :type   pchar: string
    :ivar   pchar_re: regular expression object to cut-off such chars.
    :type   pchar_re: SRE_Pattern
    :ivar   fchar: characters which have to be cut off at the end of a word.
                Filled from g_langsupport dict.
    :type   fchar: string
    :ivar   fchar_re: regular expression object to cut-off such chars.
    :type   fchar_re: SRE_Pattern
    :ivar   pclictic: character sequences which have to be cut off at the
                    beginning of a word.
                    Filled from g_langsupport dict.
    :type   pclictic: string
    :ivar   pclictic_re: regular expression object to cut-off pclictic
                        sequences.
    :type   pclictic_re: SRE_Pattern
    :ivar   fclictic: character sequences which have to be cut off at the end
                    of a word.
                    Filled from g_langsupport dict.
    :type   fclictic: string
    :ivar   fclictic_re: regular expression object to cut-off fclictic
                        sequences.
    :type   fclictic_re: SRE_Pattern
    :ivar   number: regular expression of number recognition for the language.
                    Filled from g_langsupport dict.
    :type   number: string
    :ivar   number_re: regular expression object to identify numbers.
    :type   number_re: SRE_Pattern
    :ivar   dummysequence: just a small but complete sentence in the language.
                        Filled from g_langsupport dict.
    :type   dummysequence: string
    :ivar   replurlexp: regular expression subtitution string for URLs.
    :type   replurlexp: string
    :ivar   replemailexp: regular expression subtitution string for emails.
    :type   replemailexp: string
    :ivar   replipexp: regular expression subtitution string for IP addresses.
    :type   replipexp: string
    :ivar   repldnsexp: regular expression subtitution string for DNS names.
    :type   repldnsexp: string
    :ivar   tagpopen: TreeTagger process control tool.
    :type   tagpopen: Popen
    :ivar   taginput: pipe to write to TreeTagger input. Set when opening pipe.
    :type   taginput: write stream
    :ivar   tagoutput: pipe to read from TreeTagger input. Set whe opening
                    pipe.
    :type   tagoutput: read stream
    :ivar   taggerlock: synchronization tool for multuthread use of the object.
    :type   taggerlock: threading.Lock
    :ivar   chunkerproc: external function for chunking.
    :type   chunkerproc: fct(tagger, ['text']) => ['chunk']
    """
    # --------------------------------------------------------------------------
    def __init__(self, **kargs):
        """ Construction of a wrapper for a TreeTagger process.

        You can specify several parameters at construction time.
        These parameters can be set via environment variables too
        (except for CHUNKERPROC).
        All of them have standard default values, even TAGLANG
        default to tagging english.

        :keyword TAGLANG: language code for texts ('en','fr',...)
                          (default to 'en').
        :type   TAGLANG: string
        :keyword  TAGDIR: path to TreeTagger installation directory.
        :type   TAGDIR: string
        :keyword  TAGOPT: options for TreeTagger
                          (default to '-token -lemma -sgml -quiet', it is
                          recomanded to **keep these default options** for
                          correct use of this tool, and add other options on
                          your need).
        :type   TAGOPT: string
        :keyword  TAGPARFILE: parameter file for TreeTagger.
                              (default available for supported languages).
                              Use value None to force use of default if
                              environment variable define a value you don't wants
                              to use.
        :type   TAGPARFILE: string
        :keyword  TAGABBREV: abbreviation file for preprocessing.
                             (default available for supported languages).
        :type   TAGABBREV: string
        :keyword TAGINENC: encoding to use for TreeTagger input, default
                           to utf8.
        :type TAGINENC:    str
        :keyword TAGOUTENC: encoding to use for TreeTagger output, default
                            to utf8
        :type TAGOUTENC:    str
        :keyword TAGINENCERR: management of encoding errors for TreeTagger
                              input, strict or ignore or replace -
                              default to replace.
        :type TAGINENCERR:    str
        :keyword TAGOUTENCERR: management of encoding errors for TreeTagger
                               output, strict or ignore or replace -
                               default to replace.
        :type TAGOUTENCERR:    str
        :keyword CHUNKERPROC: function to call for chunking in place of
                            wrapper's chunking — default to None (use
                            standard chunking).
                            Take the TreeTagger object as
                            first parameter and a list of str to chunk as
                            second parameter. Must return a list of chunk str
                            (tokens).
                            Note that normal initialization of chunking
                            parameters is done even with an external chunking
                            function, so these parameters are available
                            for this function.
        :type CHUNKERPROC: fct(tagger, ['text']) => list ['chunk']
        :return: None
        """
        # Get data in different place, setup context for pre-processing and
        # processing.
        logger.debug("Using treetaggerwrapper.py from %s", osp.abspath(__file__))
        self._set_language(kargs)
        self._set_tagger(kargs)
        self._set_preprocessor(kargs)
        # Note: TreeTagger process is started later, when really needed.
        if kargs:
            badargs = ", ".join(sorted(kargs.keys()))
            logger.error("Uknown TreeTagger() parameters: %s", badargs)
            raise TreeTaggerError("Uknown TreeTagger() parameters: %s" % (badargs,))

    # -------------------------------------------------------------------------
    def _set_language(self, kargs):
        """Set language for tagger.

        Internal use.
        """
        # ----- Find language to tag.
        self.lang = get_param("TAGLANG", kargs, "en")
        if self.lang not in g_langsupport:
            allowed = ', '.join(sorted(g_langsupport.keys()))
            logger.error("Language %s not supported - allowed: %s",
                         self.lang, allowed)
            raise TreeTaggerError("Unsupported language code: " + self.lang +
                                  ". allowed: " + allowed)
        logger.info("lang=%s", self.lang)
        self.langsupport = g_langsupport[self.lang]

    # -------------------------------------------------------------------------
    def _set_tagger(self, kargs):
        """Set tagger paths, files, and options.

        Internal use.
        """
        self.taggerlock = threading.Lock()

        # ----- Find TreeTagger directory.
        self.tagdir = get_param("TAGDIR", kargs, None)
        if self.tagdir is None:
            founddir = locate_treetagger()
            if founddir:
                self.tagdir = founddir
            else:
                logger.error("Can't locate TreeTagger directory (and "
                             "no TAGDIR specified).")
                raise TreeTaggerError("Can't locate TreeTagger directory (and "
                                      "no TAGDIR specified).")
        self.tagdir = os.path.abspath(self.tagdir)
        if not os.path.isdir(self.tagdir):
            logger.error("Bad TreeTagger directory: %s", self.tagdir)
            raise TreeTaggerError("Bad TreeTagger directory: " + self.tagdir)
        logger.info("tagdir=%s", self.tagdir)

        # ----- Set subdirectories.
        self.tagbindir = os.path.join(self.tagdir, "bin")
        self.taglibdir = os.path.join(self.tagdir, "lib")

        # ----- Set binary by platform.
        if ON_WINDOWS:
            self.tagbin = os.path.join(self.tagbindir, "tree-tagger.exe")
        elif ON_MACOSX or ON_POSIX:
            self.tagbin = os.path.join(self.tagbindir, "tree-tagger")
        else:
            logger.error("TreeTagger binary name undefined for platform %s",
                         sys.platform)
            raise TreeTaggerError("TreeTagger binary name undefined " \
                                  "for platform " + sys.platform)
        if not os.path.isfile(self.tagbin):
            logger.error("TreeTagger binary invalid: %s", self.tagbin)
            raise TreeTaggerError("TreeTagger binary invalid: " + self.tagbin)
        logger.info("tagbin=%s", self.tagbin)

        # ----- Find parameter file.
        self.tagparfile = get_param("TAGPARFILE", kargs, None)
        # Not in previous else to manage None parameter in kargs.
        if self.tagparfile is None:
            self.tagparfile = self.langsupport["tagparfile"]
        # If it's directly a visible file, then use it, else try to locate
        # it in TreeTagger library directory.
        maybefile = os.path.abspath(self.tagparfile)
        parfilefound = False
        if os.path.isfile(maybefile):
            self.tagparfile = maybefile
            parfilefound = True
        else:
            maybefile = os.path.join(self.taglibdir, self.tagparfile)
            if os.path.isfile(maybefile):
                self.tagparfile = maybefile
                parfilefound = True
            else:
                # As of version 2.3, tries with -utf8 parameter files.
                if '-utf8' not in maybefile:
                    name, ext = osp.splitext(maybefile)
                    maybefile = name + '-utf8' + ext
                    if os.path.isfile(maybefile):
                        self.tagparfile = maybefile
                        parfilefound = True
                        logger.warning("tagparfile automatically replaced with utf8 version"
                                       " - you may update your TreeTagger installation")
        # Report error or trace
        if not parfilefound:
            logger.error("TreeTagger parameter file invalid: %s",
                         self.tagparfile)
            raise TreeTaggerError("TreeTagger parameter file invalid: " + \
                                  self.tagparfile)
        else:
            logger.info("tagparfile=%s", self.tagparfile)

        # ----- Store encoding/decoding parameters.
        enc = get_param("TAGINENC", kargs, self.langsupport['encoding'])
        self.taginencoding = codecs.lookup(enc).name

        enc = get_param("TAGOUTENC", kargs, self.langsupport['encoding'])
        self.tagoutencoding = codecs.lookup(enc).name

        self.taginencerr = get_param("TAGINENCERR", kargs, "replace")

        self.tagoutencerr = get_param("TAGOUTENCERR", kargs, "replace")

        # ----- Find TreeTagger options.
        self.tagopt = get_param("TAGOPT", kargs, "-proto-with-prob -token -lemma -sgml -quiet -no-unknown")
        # If user dont want sgml, we activate them on the TreeTagger side,
        # but will remove them when reading.
        if "-sgml" not in self.tagopt:
            self.tagopt = "-sgml " + self.tagopt
            self.removesgml = True
        else:
            self.removesgml = False

        logger.info("tagopt=%s", self.tagopt)
        logger.info("taginencoding=%s", self.taginencoding)
        logger.info("tagoutencoding=%s", self.tagoutencoding)
        logger.info("taginencerr=%s", self.taginencerr)
        logger.info("tagoutencerr=%s", self.tagoutencerr)

        # TreeTagger is started later (when needed).
        self.tagpopen = None
        self.taginput = None
        self.tagoutput = None

    # -------------------------------------------------------------------------
    def _set_preprocessor(self, kargs):
        """Set preprocessing files, and options.

        Internal use.
        """
        # ----- Find abbreviations file.
        self.abbrevfile = get_param("TAGABBREV", kargs, None)
        # Not in previous else to manage None parameter in kargs.
        if self.abbrevfile is None:
            self.abbrevfile = self.langsupport["abbrevfile"]
        # If it's directly a visible file, then use it, else try to locate
        # it in TreeTagger library directory.
        maybefile = os.path.abspath(self.abbrevfile)
        if os.path.isfile(maybefile):
            self.abbrevfile = maybefile
        else:
            maybefile = os.path.join(self.taglibdir, self.abbrevfile)
            if os.path.isfile(maybefile):
                self.abbrevfile = maybefile
            else:
                logger.warning("Abbreviation file not found: %s", self.abbrevfile)
                logger.warning("Processing without abbreviations file.")
                self.abbrevfile = None
        logger.info("abbrevfile=%s", self.abbrevfile)

        # ----- Read file containing list of abbrevitations.
        self.abbterms = {}
        if self.abbrevfile is not None:
            # As we have an existing abbreviations file, we try to read
            # it and we consider a read failure as an error.
            try:
                with io.open(self.abbrevfile, "r", encoding=self.taginencoding) as f:
                    for line in f:
                        line = line.strip()  # Remove blanks after and before.
                        if not line: continue  # Ignore empty lines
                        if line[0] == '#': continue  # Ignore comment lines.
                        self.abbterms[line.lower()] = line  # Store as a dict keys.
                logger.info("Read %d abbreviations from file: %s",
                            len(self.abbterms), self.abbrevfile)
            except:
                logger.exception("Failure to read abbreviations file: %s",
                                 self.abbrevfile, exc_info=True)
                raise

        # ----- Prefix chars at beginning of string.
        self.pchar = self.langsupport["pchar"]
        if self.pchar:
            self.pchar_re = re.compile("^([" + self.pchar + "])(.*)$",
                                       re.IGNORECASE | re.VERBOSE)
        else:
            self.pchar_re = None

        # ----- Suffix chars at end of string.
        self.fchar = self.langsupport["fchar"]
        if self.fchar:
            self.fchar_re = re.compile("^(.*)([" + self.fchar + "])$",
                                       re.IGNORECASE | re.VERBOSE)
            self.fcharandperiod_re = re.compile("(.*)([" + self.fchar + ".])\\.$")
        else:
            self.fchar_re = None
            self.fcharandperiod_re = None

        # ----- Character *sequences* to cut-off at beginning of words.
        self.pclictic = self.langsupport["pclictic"]
        if self.pclictic:
            self.pclictic_re = re.compile("^(" + self.pclictic + ")(.*)$",
                                          re.IGNORECASE | re.VERBOSE)
        else:
            self.pclictic_re = None

        # ----- Character *sequences* to cut-off at end of words.
        self.fclictic = self.langsupport["fclictic"]
        if self.fclictic:
            self.fclictic_re = re.compile("^(.*)(" + self.fclictic + ")$",
                                          re.IGNORECASE | re.VERBOSE)
        else:
            self.fclictic_re = None

        # ----- Numbers recognition.
        self.number = self.langsupport["number"]
        self.number_re = re.compile(self.number, re.IGNORECASE | re.VERBOSE)

        # ----- Dummy string to flush
        sentence = self.langsupport["dummysentence"]
        self.dummysequence = "\n".join(sentence.split())

        # ----- Replacement string for
        self.replurlexp = self.langsupport["replurlexp"]
        self.replemailexp = self.langsupport["replemailexp"]
        self.replipexp = self.langsupport["replipexp"]
        self.repldnsexp = self.langsupport["repldnsexp"]

        # ----- External chunking proc
        # (this would be necessary for multiprocess with chunker from an external module)
        self.chunkerproc = get_param("CHUNKERPROC", kargs, None)
        if isinstance(self.chunkerproc, six.text_type):
            # TODO: Allow str in CHUNKERPROC, and import corresponding name
            raise NotImplementedError("CHUNKERPROC as name")
        if self.chunkerproc is not None and not callable(self.chunkerproc):
            logger.error("Chunker function in CHUNKERPROC is not callable.")
            raise TreeTaggerError("Chunker function in CHUNKERPROC is not callable.")

    # --------------------------------------------------------------------------
    def _start_process(self):
        """Start TreeTagger processing chain.

        Internal use.
        """
        # ----- Start the TreeTagger.
        tagcmdlist = [self.tagbin]
        tagcmdlist.extend(shlex.split(self.tagopt))
        tagcmdlist.append(self.tagparfile)
        if ON_WINDOWS:
            # Prevent opening of a cmd console.
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        else:
            startupinfo = None
        try:
            # self.taginput,self.tagoutput = os.popen2(tagcmd)
            self.tagpopen = subprocess.Popen(
                tagcmdlist,  # Use a list of params in place of a string.
                bufsize=0,   # Not buffered to retrieve data asap from TreeTagger
                executable=self.tagbin,  # As we have it, specify it
                stdin=subprocess.PIPE,  # Get a pipe to write input data to TreeTagger process
                stdout=subprocess.PIPE,  # Get a pipe to read processing results from TreeTagger
                # stderr=None,     unused
                # preexec_fn=None, unused
                # close_fds=False, And cannot be set to true and use pipes simultaneously on windows
                # shell=False,     We specify full path to treetagger binary, no reason to use shell
                # cwd=None,        Normally files are specified with full path, so don't set cwd
                # env=None,        Let inherit from current environment
                # universal_newlines=False,  Keep no universal newlines, manage myself
                startupinfo=startupinfo,
                # creationflags=0   unused
            )
            self.taginput, self.tagoutput = self.tagpopen.stdin, self.tagpopen.stdout
            logger.info("Started TreeTagger from command: %r", tagcmdlist)
        except:
            logger.error("Failure to start TreeTagger with: %r", \
                         tagcmdlist, exc_info=True)
            raise

    # --------------------------------------------------------------------------
    def __del__(self):
        """Wrapper to be deleted.

        Cut links with TreeTagger process.
        """
        if hasattr(self, "taginput") and self.taginput:
            self.taginput.close()
            self.taginput = None
        if hasattr(self, "tagoutput") and self.tagoutput:
            self.tagoutput.close()
            self.tagoutput = None
        if hasattr(self, "tagpopen") and self.tagpopen:
            self.tagpopen.terminate()
            # Will see if it is necessary to replace terminate by kill.
            # self.tagpopen.kill()
            self.tagpopen = None

    #--------------------------------------------------------------------------
    def TagText(self, text, numlines=False, tagonly=False,
                prepronly=False, tagblanks=False, notagurl=False,
                notagemail=False, notagip=False, notagdns=False,
                encoding=None, errors="strict") :
        """Old method for compatibility.
        """
        if encoding and not isinstance(text, six.text_type):
            if isinstance(text, six.binary_type):
                text = text.decode(encoding)
            # Note: we don't manage decoding of lists of binary strings!
            # the function may fail later unless a list of Unicode strings
            # has been providen.
        return self.tag_text(text, numlines=numlines, tagonly=tagonly,
                             prepronly=prepronly, tagblanks=tagblanks, notagurl=notagurl,
                             notagemail=notagemail, notagip=notagip, notagdns=notagdns)

    # --------------------------------------------------------------------------
    def tag_text(self, text, numlines=False, tagonly=False,
                 prepronly=False, tagblanks=False, notagurl=False,
                 notagemail=False, notagip=False, notagdns=False,
                 nosgmlsplit=False):
        """Tag a text and returns corresponding lines.

        This is normally the method you use on this class. Other methods
        are only helpers of this one.

        The return value of this method can be processed by :func:`make_tags`
        to retrieve a list of :class:`Tag` named tuples with meaning fields.

        :param  text: the text to tag.
        :type   text: unicode string   /   [ unicode string ]
        :param  numlines: indicator to keep line numbering information in
                          data flow (done via SGML tags) (default to False).
        :type   numlines: boolean
        :param  tagonly: indicator to only do TreeTagger tagging processing
                         on input (default to False).
                         If tagonly is set, providen text must be composed
                         of one token by line (either as a collection of
                         line-feed separated lines in one string, or as a list
                         of lines).
        :type   tagonly: boolean
        :param  prepronly: indicator to only do preprocessing of text without
                           tagging (default to False).
        :type   prepronly: boolean
        :param  tagblanks: indicator to keep blanks characters information in
                           data flow (done via SGML tags) (default to False).
        :type   tagblanks: boolean
        :param  notagurl: indicator to not do URL replacement (default to False).
        :type   notagurl: boolean
        :param  notagemail: indicator to not do email address replacement
                            (default to False).
        :type   notagemail: boolean
        :param  notagip: indicator to not do IP address replacement (default
                         to False).
        :type   notagip: boolean
        :param  notagdns: indicator to not do DNS names replacement (default
                          to False).
        :type   notagdns: boolean
        :param  nosgmlsplit: indicator to not split on sgml already within
                          the text (default to False).
        :type   nosgmlsplit: boolean
        :return: List of output strings from the tagger.
                        You may use :func:`make_tags` function to build
                        a corresponding list of named tuple, for
                        further processing readbility.
        :rtype:  [ str ]
        """
        logger.debug("tag_text with option: numlines=%d, tagonly=%d, "
                     "prepronly=%d, notagurl=%d, tagblanks=%d, "
                     "notagemail=%d, notagip=%d, notagdns=%d, nosgmlsplit=%d).",
                     numlines, tagonly, prepronly, tagblanks, notagurl, notagemail,
                     notagip, notagdns, nosgmlsplit)

        # Check for incompatible options.
        if (tagblanks or numlines) and self.removesgml:
            logger.error("Line numbering/blanks tagging need use of -sgml " + \
                         "option for TreeTagger.")
            raise TreeTaggerError("Line numbering/blanks tagging need use " + \
                                  "of -sgml option for TreeTagger.")

        if isinstance(text, six.binary_type):
            # Raise exception now, with an explicit message.
            logger.error("Must use *unicode* string as text to tag, not %s.", type(text))
            raise TreeTaggerError("Must use *unicode* string as text to tag.")

        if isinstance(text, six.text_type):
            text = [text]
        else:
            for t in text:
                if isinstance(t, six.binary_type):
                    # Raise exception now, with an explicit message.
                    logger.error("Must use list of *unicode* string as text to tag, not %s.", type(t))
                    raise TreeTaggerError("Must use list of *unicode* string as text to tag.")


        # Preprocess text (prepare for TreeTagger).
        if not tagonly:
            if self.chunkerproc is None:
                logger.debug("Pre-processing text with internal chunker.")
                lines = self._prepare_text(text, tagblanks=tagblanks, numlines=numlines,
                                           notagurl=notagurl, notagemail=notagemail,
                                           notagip=notagip, notagdns=notagdns,
                                           nosgmlsplit=nosgmlsplit)
            else:
                logger.debug("Pre-processing text with user providen chunker.")
                lines = self.chunkerproc(self, text)
        else:
            # Adapted to support list of lines.
            # And do split on end of lines, not on spaces (ie if we don't prepare the
            # text, we can consider that it has been prepared elsewhere by caller,
            # and there is only one token item by line for TreeTagger).
            lines = []
            for l in text:
                lines.extend(l.splitlines())

        if prepronly:
            return lines

        # Prevent concurrent access to the pipe if used in multithreading
        # context.
        with self.taggerlock:
            # TreeTagger process is started at first need.
            if self.taginput is None:
                self._start_process()

            # Send text to TreeTagger, get result.
            logger.debug("Tagging text.")
            t = threading.Thread(target=pipe_writer,
                                 args=(self.taginput,
                                       lines, self.dummysequence,
                                       self.taginencoding,
                                       self.taginencerr))
            t.start()

            result = []
            intext = False
            lastline_time = time.time()
            while True:
                line = self.tagoutput.readline()
                if DEBUG: logger.debug("Read from TreeTagger: %r", line)
                if not line:
                    if (time.time() - lastline_time) > TAGGER_TIMEOUT:
                        # We already wait some times, there may be a problem with tagging
                        # process communication. This avoid infinite loop.
                        logger.error("Time out for TreeTagger reply.")
                        raise TreeTaggerError("Time out for TreeTagger reply, enable debug / see error logs")
                    else:
                        # We process too much quickly, leave time for tagger and writer
                        # thread to work.
                        time.sleep(0.1)
                        continue    # read again.
                lastline_time = time.time()

                line = line.decode(self.tagoutencoding, self.tagoutencerr)
                line = line.strip()
                if line == STARTOFTEXT:
                    intext = True
                    continue
                if line == ENDOFTEXT:  # The flag we sent to identify texts.
                    intext = False
                    break
                if intext and line:
                    if not (self.removesgml and is_sgml_tag(line)):
                        result.append(line)

            # Synchronize to avoid possible problems.
            t.join()

        return result

    # --------------------------------------------------------------------------
    def tag_file(self, infilepath, encoding=USER_ENCODING,
                 numlines=False, tagonly=False,
                 prepronly=False, tagblanks=False, notagurl=False,
                 notagemail=False, notagip=False, notagdns=False,
                 nosgmlsplit=False):
        """Call :meth:`tag_text` on the content of a specified file.

        :param infilepath: pathname to access the file to read.
        :type infilepath: str
        :param encoding: specify encoding of the file to read, default to utf-8.
        :type encoding: str
        :return: List of output strings from the tagger.
        :rtype:  [ str ]

        Other parameters are simply passed to :meth:`tag_text`.
        """
        with io.open(infilepath, "r", encoding=encoding) as f:
            content = f.read()

        return self.tag_text(content,
                             numlines=numlines, tagonly=tagonly,
                             prepronly=prepronly, tagblanks=tagblanks, notagurl=notagurl,
                             notagemail=notagemail, notagip=notagip, notagdns=notagdns,
                             nosgmlsplit=nosgmlsplit)

    # --------------------------------------------------------------------------
    def tag_file_to(self, infilepath, outfilepath, encoding=USER_ENCODING,
                    numlines=False, tagonly=False,
                    prepronly=False, tagblanks=False, notagurl=False,
                    notagemail=False, notagip=False, notagdns=False,
                    nosgmlsplit=False):
        """Call :meth:`tag_text` on the content of a specified file and write
        result to a file.

        :param infilepath: pathname to access the file to read.
        :type infilepath: str
        :param outfilepath: pathname to access the file to write.
        :type outfilepath: str
        :param encoding: specify encoding of the files to read/write, default to utf-8.
        :type encoding: str

        Other parameters are simply passed to :meth:`tag_text`.
        """
        logger.info("Processing with file %s, reading input.", infilepath)
        with io.open(infilepath, "r", encoding=encoding) as f:
            content = f.read()

        logger.info("Processing with file %s, tagging.", infilepath)
        res = self.tag_text(content,
                            numlines=numlines, tagonly=tagonly,
                            prepronly=prepronly, tagblanks=tagblanks, notagurl=notagurl,
                            notagemail=notagemail, notagip=notagip, notagdns=notagdns,
                            nosgmlsplit=nosgmlsplit)

        logger.info("Processing with file %s, writing to %s.",
                    infilepath, outfilepath)
        res = "\n".join(res)
        with io.open(outfilepath, "w", encoding=encoding) as f:
            content = f.write(res)

        logger.info("Processing with file %s, finished.", infilepath)

    # --------------------------------------------------------------------------
    def _prepare_text(self, text, tagblanks=False, numlines=False,
                      notagurl=False, notagemail=False, notagip=False,
                      notagdns=False, nosgmlsplit=False):
        """Prepare a text for processing by TreeTagger.

        :param  text: the text to split into base elements.
        :type   text: unicode   /   [ unicode ]
        :param  tagblanks: transform blanks chars into SGML tags.
        :type   tagblanks: boolean
        :param  numlines: indicator to create sgml  tag for line numbering.
        :type   numlines: boolean
        :param  notagurl: indicator to not do URL replacement (default to False).
        :type   notagurl: boolean
        :param  notagemail: indicator to not do email address replacement
                            (default to False).
        :type   notagemail: boolean
        :param  notagip: indicator to not do IP address replacement (default
                         to False).
        :type   notagip: boolean
        :param  notagdns: indicator to not do DNS names replacement (default
                          to False).
        :type   notagdns: boolean
        :param  nosgmlsplit: indicator to not split on sgml already within the text.
        :type   nosgmlsplit: boolean
        :return: List of lines to process as TreeTagger input (no \\n at end of line).
        :rtype: [ unicode ]
        """
        logger.debug("Preparing text for tagger with options tagblanks=%d, numlines=%d, notagurl=%d, "
                     "notagemail=%d, notagip=%d, notagdns=%d, nosgmlsplit=%d).",
                     tagblanks, numlines, notagurl, notagemail, notagip, notagdns, nosgmlsplit)

        # To avoid searching in many place for SGML tags, such tags
        # are wrapped inside an FinalPart object.

        # Build a list of lines. If we start from a list of text
        if isinstance(text, six.text_type):
            lines = text.splitlines()
        else:
            lines = []
            for t in text:
                if '\n' in t:
                    lines.extend(t.splitlines())
                else:
                    lines.append(t)

        # If necessary, add line numbering SGML tags (which will
        # be passed out as is by TreeTagger and which could be
        # used to identify lines in the flow of tags).
        if numlines:
            logger.debug("Numbering lines.")
            parts = []
            for num, line in enumerate(lines):
                parts.append(FinalPart(NUMBEROFLINE.format(num + 1,)))
                parts.append(line)
            # Remove temporary storage.

            logger.debug("Inserted line numbers as SGML tags between lines.")
        else:
            parts = lines

        # First, we split the text between SGML tags and non SGML
        # part tags (for pure text, this will make no difference,
        # but consume time).
        if not nosgmlsplit:
            logger.debug("Identifying SGML tags from within text.")
            newparts = []
            for part in parts:
                if isinstance(part, FinalPart):
                    newparts.append(part)
                else:
                    newparts.extend(split_sgml(part))
            parts = newparts
            logger.debug("Splitted between SGML tags and others %r.")

        newparts = []
        if tagblanks:
            # If requested, replace internal blanks by other SGML tags.
            logger.debug("Replacing blanks by corresponding SGML tags.")
            for part in parts:
                if isinstance(part, FinalPart):
                    newparts.append(part)
                else:
                    newparts.extend(blank_to_tag(part))
        else:
            # Else, replace cr, lf, vt, ff, and tab characters with blanks.
            logger.debug("Replacing blanks by spaces.")
            for part in parts:
                if isinstance(part, FinalPart):
                    newparts.append(part)
                else:
                    newparts.append(blank_to_space(part))
        parts = newparts
        logger.debug("Blanks replacement done.")

        if not notagurl:
            logger.debug("Replacing URLs.")
            parts = build_with_callable(parts,
                                        split_url, self.replurlexp, REPLACED_URL_TAG)
            logger.debug("URLs replacement done.")

        if not notagemail:
            logger.debug("Replacing Emails.")
            parts = build_with_callable(parts,
                                        split_email, self.replemailexp, REPLACED_EMAIL_TAG)
            logger.debug("Emails replacement done.")

        if not notagip:
            logger.debug("Replacing IP addresses.")
            parts = build_with_callable(parts,
                                        split_ip, self.replipexp, REPLACED_IP_TAG)
            logger.debug("IP adresses replacement done.")

        if not notagdns:
            logger.debug("Replacing DNS names.")
            parts = build_with_callable(parts,
                                        split_dns, self.repldnsexp, REPLACED_DNS_TAG)
            logger.debug("DNS names replacement done.")

        # Process part by part, some parts wille be SGML tags, other don't.
        logger.debug("Splittint parts of text.")
        newparts = []
        for part in parts:
            if isinstance(part, FinalPart):
                # TreeTagger process by line... a token cannot be on multiple
                # lines (in case it occured in source text).
                part.text = part.text.replace("\n", " ")
                logger.debug("No _prepare_part() for final part %s.", part)
                newparts.append(part)
            else:
                # This is another part which need more analysis.
                newparts.extend(self._prepare_part(part))
        parts = newparts

        logger.debug("Text preprocessed, parts splitted one by line.")

        # Return only str items for caller.
        return [x.text if isinstance(x, FinalPart) else x for x in parts]

    # --------------------------------------------------------------------------
    def _prepare_part(self, text):
        """Prepare a basic text.

        Prepare non-SGML text parts.

        :param  text: unicode text of part to process.
        :type   text: unicode
        :return: List of lines to process as TreeTagger input.
        :rtype: [ str ]
        """
        # May occur when recursively calling after splitting on dot, if there
        # are two consecutive dots.
        if not text: return []

        text = " " + text + " "

        # Put blanks before and after '...' (extract ellipsis).
        text = ellipfind_re.sub(ellipfind_subst, text)

        # Put space between punctuation ;!?:, and following text if space missing.
        text = punct1find_re.sub(punct1find_subst, text)

        # Put space between text and punctuation ;!?:, if space missing.
        text = punct2find_re.sub(punct2find_subst, text)

        # Here some script put blanks after dots (while processing : and , too).
        # This break recognition of texts like U.S.A later.

        # Cut on whitespace, and work on subpart item by subpart item.
        # Extend newparts after each part processing.
        parts = text.split()
        newparts = []
        for pidx, part in enumerate(parts):
            if DEBUG_PREPROCESS: logger.debug("Processing part: %r", part)
            # We should not have final parts at this time.
            assert not isinstance(part, FinalPart)
            # For single characters or ellipsis, no more processing.
            if len(part) == 1 or part == "...":
                newparts.append(FinalPart(part))
                continue

            # handle explicitly listed tokens
            # Now done before all prefix/suffix splitting as some abbreviations
            # include such chars.
            if part.lower() in self.abbterms:
                if DEBUG_PREPROCESS: logger.debug("Found explicit token: %r", part)
                newparts.append(FinalPart(part))
                continue

            # We put prefix subparts in the prefix list, and suffix subparts in the
            # suffix list, at the end prefix + part + suffix are added to newparts.
            prefix = []
            suffix = []
            # Separate punctuation and parentheses from words.
            while True:
                finished = True  # Exit at end if no match.
                # cut off preceding punctuation
                if self.pchar_re is not None:
                    matchobj = self.pchar_re.match(part)
                    if matchobj is not None:
                        if DEBUG_PREPROCESS:
                            logger.debug("Splitting preceding punct: %r", matchobj.group(1))
                        prefix.append(matchobj.group(1))  # First pchar.
                        part = matchobj.group(2)  # Rest of text.
                        finished = False
                # cut off trailing punctuation
                if self.fchar_re is not None:
                    matchobj = self.fchar_re.match(part)
                    if matchobj is not None:
                        if DEBUG_PREPROCESS:
                            logger.debug("Splitting following punct: %r", matchobj.group(2))
                        suffix.insert(0, matchobj.group(2))
                        part = matchobj.group(1)
                        finished = False
                # cut off trailing periods if punctuation precedes
                if self.fcharandperiod_re is not None:
                    matchobj = self.fcharandperiod_re.match(part)
                    if matchobj is not None:
                        if DEBUG_PREPROCESS:
                            logger.debug("Splitting dot after following punct: .")
                        suffix.insert(0, ".")  # Last dot.
                        part = matchobj.group(1) + matchobj.group(2)  # Other.
                        finished = False
                # Exit while loop if no match in regular expressions.
                if finished: break

            # Process with the dot problem...
            # Look for acronyms of the form U.S.A. or U.S.A
            if acronymexpr_re.match(part):
                if DEBUG_PREPROCESS: logger.debug("Found acronym: %r", part)
                if part[-1] != '.':
                    # Force final dot to have homogeneous acronyms.
                    part += '.'
                newparts.extend(prefix)
                newparts.append(FinalPart(part))
                newparts.extend(suffix)
                continue

            # identify numbers.
            matchobj = self.number_re.match(part)
            if matchobj is not None:
                # If there is only a dot after the number which is not
                # recognized, then split it and take the number.
                if matchobj.group() == part[:-1] and part[-1] == ".":
                    part = part[:-1]  # Validate next if... process number.
                    suffix.insert(0, FinalPart("."))
                if matchobj.group() == part:  # It's a *full* number.
                    if DEBUG_PREPROCESS: logger.debug("Found number: %r", part)
                    newparts.extend(prefix)
                    newparts.append(FinalPart(part))
                    newparts.extend(suffix)
                    continue

            # Remove possible trailing dots.
            while part and part[-1] == '.':
                if DEBUG_PREPROCESS: logger.debug("Found trailing dot: .")
                suffix.insert(0, FinalPart("."))
                part = part[:-1]
                if DEBUG_PREPROCESS:
                    logger.debug("Prefix/part/suffix: %r/%r/%r.", prefix, part, suffix)

            # If still has dot, split around dot, and process subpart by subpart
            # (call this method recursively).
            # 2004-08-30 - LP
            # As now DNS names and so on are pre-processed, there should no
            # longer be things like www.limsi.fr, remaining dots may be parts
            # of names as in J.S.Bach.
            # So commented the code out (keep it here).
            # if "." in part :
            #    if DEBUG_PREPROCESS :
            #        print "Splitting around remaining dots:",part
            #    newparts.extend(prefix)
            #    subparts = part.split(".")
            #    for index,subpart in enumerate(subparts) :
            #        newparts.extend(self._prepare_part(subpart))
            #        if index+1<len(subparts) :
            #            newparts.append(".")
            #    newparts.extend(suffix)
            #    continue

            # cut off clictics
            if self.pclictic_re is not None:
                retry = True
                while retry:
                    matchobj = self.pclictic_re.match(part)
                    if matchobj is not None:
                        if DEBUG_PREPROCESS:
                            logger.debug("Splitting begin clictic: %r %r",
                                         matchobj.group(1), matchobj.group(2))
                        prefix.append(matchobj.group(1))
                        part = matchobj.group(2)
                        if DEBUG_PREPROCESS:
                            logger.debug("Prefix/part/suffix: %r/%r/%r.", prefix, part, suffix)
                    else:
                        retry = False

            if self.fclictic_re is not None:
                retry = True
                while retry:
                    matchobj = self.fclictic_re.match(part)
                    if matchobj is not None:
                        if DEBUG_PREPROCESS:
                            logger.debug("Splitting end clictic: %r %r",
                                         matchobj.group(1), matchobj.group(2))
                        suffix.insert(0, matchobj.group(2))
                        part = matchobj.group(1)
                        if DEBUG_PREPROCESS:
                            logger.debug("Prefix/part/suffix: %r/%r/%r.", prefix, part, suffix)
                    else:
                        retry = False

            newparts.extend(prefix)
            newparts.append(FinalPart(part))
            newparts.extend(suffix)

        return newparts


# ==============================================================================
def build_with_callable(parts, fct, *args):
    """Build a new parts list resultnig from function call on each part.

    FinalParts are left as is.
    The function must take a part as first parameter and return a list of
    parts.
    """
    newparts = []
    for part in parts:
        if isinstance(part, FinalPart):
            newparts.append(part)
        else:
            newparts.extend(fct(part, *args))
    return newparts


# ==============================================================================
# XML element/attributes names syntax (including xml namespace):
SGML_name = r"""(?:[a-z][-_.a-z0-9]*(?::[-_.a-z0-9]*)?)"""

# XML attribute in an element tag (allow non-quoted value for bad html...)
SGML_att = SGML_name + r"""\s*=\s*(?:(?:"[^>"]*")|(?:'[^>']*')|(?:[^\s]+))"""

# XML tags (as group, with parenthesis !!!).
SGML_tag = r"""
    (
        (?:<!-- .*? -->)                   # XML/SGML comment
            |                              # -- OR --
        (?:
        <[!?/]?""" + SGML_name + r"""      # Start of tag/directive
            (?:\s+""" +SGML_att + r""")*   # [attributes]
         \s*[/?]?>                         # End of tag/directive - maybe autoclosed
        )
    )"""
SGML_tag_re = re.compile(SGML_tag, re.IGNORECASE | re.VERBOSE | re.DOTALL)


def is_sgml_tag(text):
    """Test if a text is - completly - a SGML tag.

    :param  text: the text to test.
    :type  text: string
    :return: True if it's an SGML tag.
    :rtype: boolean
    """
    return SGML_tag_re.match(text) is not None


# ==============================================================================
def split_sgml(text):
    """Split a text between SGML-tags and non-SGML-tags parts.

    :param  text: the text to split.
    :type  text: string
    :return: List of text/SgmlTag in their apparition order.
    :rtype: list
    """
    # Simply split on XML tags recognized by regular expression.
    parts = SGML_tag_re.split(text)
    parts[1::2] = [FinalPart(x) for x in parts[1::2]]
    # Remove heading and trailing empty string (here when an sgml tag is at
    # beginning or end).
    if not parts[0]:
        parts = parts[1:]
    if len(parts) and not parts[-1]:
        parts = parts[:-1]
    return parts


# ==============================================================================
BLANK_TO_TAG_TAGS = [(' ', FinalPart(TAGSPACE)), ('\t', FinalPart(TAGTAB)),
                     ('\n', FinalPart(TAGLF)), ('\r', FinalPart(TAGCR)),
                     ('\v', FinalPart(TAGVT)), ('\f', FinalPart(TAGFF))]


def blank_to_tag(text):
    """Replace blanks characters by corresponding SGML tags in a text.

    :param  text: the text to transform from blanks.
    :type  text: string
    :return: List of texts and sgml tags where there was a blank.
    :rtype: list.
    """
    parts = [text]
    for c, r in BLANK_TO_TAG_TAGS:
        newparts = []
        for part in parts:
            if isinstance(part, FinalPart) or c not in part:
                newparts.append(part)
            else:
                # Insert r between each splitted item between c char.
                items = part.split(c)
                mix = ([None, r] * len(items))[:-1]
                mix[::2] = items
                newparts.extend(mix)
        parts = newparts
    return parts


# ==============================================================================
def maketrans_unicode(s1, s2, todel=""):
    """Build translation table for use with unicode.translate().

    :param s1: string of characters to replace.
    :type s1: unicode
    :param s2: string of replacement characters (same order as in s1).
    :type s2: unicode
    :param todel: string of characters to remove.
    :type todel: unicode
    :return: translation table with character code -> character code.
    :rtype: dict
    """
    # We go unicode internally - ensure callers are ok with that.
    assert (isinstance(s1, six.text_type))
    assert (isinstance(s2, six.text_type))
    trans_tab = dict(zip(map(ord, s1), map(ord, s2)))
    trans_tab.update((ord(c), None) for c in todel)
    return trans_tab


# ==============================================================================
BLANK_TO_SPACE_TABLE = maketrans_unicode("\r\n\t\v\f", "     ")


def blank_to_space(text):
    """Replace blanks characters by real spaces.

    May be good to prepare for regular expressions & Co based on whitespaces.

    :param  text: the text to clean from blanks.
    :type  text: string
    :return: List of parts in their apparition order.
    :rtype: [ string ]
    """
    return text.translate(BLANK_TO_SPACE_TABLE)


# ==============================================================================
# Not perfect, but work mostly.
# From http://www.faqs.org/rfcs/rfc1884.html
# Ip_expression = r"""
#     (?:                         # ----- Classic dotted IP V4 address -----
#         (?:[0-9]{1,3}\.){3}[0-9]{1,3}
#     )
#             |
#     (?:                         # ----- IPV6 format. -----
#       (?:[0-9A-F]{1,4}:){1,6}(?::[0-9A-F]{1,4}){1,6}        # :: inside
#                 |
#       (?:[0-9A-F]{1,4}:){1,6}:                              # :: at end
#                 |
#       :(?::[0-9A-F]{1,4}){1,6}                              # :: at begining
#                 |
#       (?:[0-9A-F]{1,4}:){7}[0-9A-F]{1,4}                    # Full IPV6
#                 |
#                 ::                                          # Empty IPV6
#     )
#         (?:(?:\.[0-9]{1,3}){3})?    # Followed by a classic IPV4.
#                                     # (first number matched by previous rule...
#                                     #  which may match hexa number too (bad) )
# """
# 2004-08-30 - LP
# As IP V6 can interfer with :: in copy/past code, and as it's (currently)
# not really common, I comment out the IP V6 recognition.
Ip_expression = r"""
    (?:                         # ----- Classic dotted IP V4 address -----
        (?:[0-9]{1,3}\.){3}[0-9]{1,3}
    )
    """
IpMatch_re = re.compile("(" + Ip_expression + ")",
                        re.VERBOSE | re.IGNORECASE)


def split_ip(text, replace, sgmlformat):
    return split_on_regexp(text, IpMatch_re, replace, sgmlformat)


# ==============================================================================
# Don't parentheses expression to reuse it inside URLs and emails.
# To not mismatch with acronyms, we exclude one char names in all places,
# and require al least two names separated by a dot.
DnsHost_expression = r"""
    (?:xn--)?   # Punycode notation for internationalized names
    (?:[a-z][-a-z0-9]{0,61}[a-z0-9]\.)+  # host and intermediate domain names
    (?:[[a-z][-a-z0-9]{0,61}[a-z0-9])     # tld name
    """
DnsHostMatch_re = re.compile("(" + DnsHost_expression + ")",
                             re.VERBOSE | re.IGNORECASE)


def split_dns(text, replace, sgmlformat):
    return split_on_regexp(text, DnsHostMatch_re, replace, sgmlformat)


# ==============================================================================
# See http://www.ietf.org/rfc/rfc1738.txt?number=1738
UrlMatch_expression = r"""(
                # Scheme part
        (?:ftp|https?|gopher|mailto|news|nntp|telnet|wais|file|prospero):
                # IP Host specification (optionnal)
        (?:// (?:[-a-z0-9_;?&=](?::[-a-z0-9_;?&=]*)?@)?   # User authentication.
             (?:(?:""" + DnsHost_expression + r""")
                        |
                (?:""" + Ip_expression + """)
              )
              (?::[0-9]+)?      # Port specification
        /)?
                # Scheme specific extension.
        (?:[-a-z0-9;/?:@=&\$_.+!*'(~#%,]+)*
        )"""
UrlMatch_re = re.compile(UrlMatch_expression, re.VERBOSE | re.IGNORECASE)


def split_url(text, replace, sgmlformat):
    return split_on_regexp(text, UrlMatch_re, replace, sgmlformat)


# ==============================================================================
EmailMatch_expression = r"""(
            [-a-z0-9._']+@
            """ + DnsHost_expression + r"""
            )"""
EmailMatch_re = re.compile(EmailMatch_expression, re.VERBOSE | re.IGNORECASE)


def split_email(text, replace, sgmlformat):
    return split_on_regexp(text, EmailMatch_re, replace, sgmlformat)


# ==============================================================================
def split_on_regexp(text, pattern, replace, sgmlformat):
    """Split a text between identified parts by regexp pattern.

    :param  text: the text to split.
    :type  text: string
    :param pattern: the compiled regular-expression.
    :type pattern: SRE_Pattern
    :param replace: meaningful replacement text
    :type replace: str
    :param sgmlformat: string format for a sgml tag
    :type sgmlformat: str
    :return: List of text/SgmlTag for emails in their apparition order.
    :rtype: list
    """
    parts = pattern.split(text)
    newparts = []
    for idx, part in enumerate(parts):
        if idx % 2 == 0:
            newparts.append(part)
        else:
            if replace:
                newparts.append(replace)
            if sgmlformat:
                newparts.append(FinalPart(sgmlformat.format(part)))
    parts = newparts
    # Remove heading and trailing empty string (here when an sgml tag is at
    # beginning or end).
    if not parts[0]:
        parts = parts[1:]
    if len(parts) and not parts[-1]:
        parts = parts[:-1]
    return parts


# ==============================================================================
debugging_log_enabled = False


def enable_debugging_log():
    """Setup logging module output.

    This setup a log file which register logs, and also dump logs to stdout.
    You can just copy/paste and adapt it to make logging write to your own log
    files.
    """
    # If debug is active, we log to a treetaggerwrapper.log file, and to
    # stdout too. If you wants to log for long time process, you may
    # take a look at RotatingFileHandler.
    global logger, debugging_log_enabled

    if debugging_log_enabled: return
    debugging_log_enabled = True

    hdlr = logging.FileHandler('treetaggerwrapper.log')
    hdlr2 = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        'T%(thread)d %(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    hdlr2.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.addHandler(hdlr2)
    logger.setLevel(logging.DEBUG)


# ==============================================================================
def locate_treetagger():
    """Try to find treetagger directory in some standard places.

    If a location is already available in treetaggerwrapper config file,
    then the function first check if it is still valid, and if yes
    simply return this location.

    A treetagger directory (any variation of directory name with *tree* and
    *tagger*, containing :file:`lib` and :file:`bin` subdirectories) is search:

    - In user home directories and its subdirectories.

    - In MacOSX user own library frameworks.

    - In system wide standard installation directories (depend on
      used platform).

    The found location, if any, is stored into :file:`treetagger_wrapper.cfg`
    file for later direct use (located in standard XDG config path).

    If not found, the function returns None.

    :return: directory conntaining TreeTagger installation, or None.
    :rtype: str
    """
    founddir = None
    # ===== Use cached last automatically found location if any.
    if g_config.has_section("CACHE") and g_config.has_option('CACHE', 'TAGDIR'):
        founddir = g_config.get('CACHE', 'TAGDIR')
        if osp.isdir(founddir):
            logger.info("Use previously found TreeTagger directory: %s", founddir)
            return founddir
        else:
            founddir = None

    # ===== Use environment vars as seen in other scripts using TreeTagger.
    if 'TREETAGGER' in os.environ:
        founddir = os.environ['TREETAGGER']
    elif 'TREETAGGER_HOME' in os.environ:
        founddir = os.environ['TREETAGGER_HOME']
    if founddir is not None and osp.isdir(founddir):
        logger.info("Use env var specified TreeTagger directory: %s", founddir)
        return founddir
        # Note: we don't cache the value set in env var.

    # ===== Search in possible known paths.
    # --- User own installation:

    # I initially listed some common home subdirs… finally use
    # a list of home and all its first level subdirectories.
    home = osp.abspath(osp.expanduser("~"))
    moduledir = osp.dirname(osp.abspath(__file__))
    moduleparentdir = osp.dirname(moduledir)

    searchdirs = []
    searchdirs.append(moduledir)
    if moduleparentdir != moduledir:
        searchdirs.append(moduleparentdir)
    if home not in searchdirs:
        searchdirs.append(home)
    homedirs = [osp.join(home, x) for x in os.listdir(home)]
    homedirs = [x for x in homedirs if osp.isdir(x) and x not in searchdirs]
    searchdirs.extend(homedirs)

    if ON_MACOSX:
        searchdirs.extend([
            '~/Library/Frameworks',
        ])

    # ---  System wide installations:
    # Windows (and maybe cygwin) installations.
    if ON_WINDOWS:
        if 'ProgramFiles' in os.environ:
            searchdirs.append(os.environ['ProgramFiles'])
        if 'ProgramFiles(x86)' in os.environ:
            searchdirs.append(os.environ['ProgramFiles(x86)'])
        if 'ProgramW6432' in os.environ:
            searchdirs.append(os.environ['ProgramW6432'])
        # Also search at root of drives and at one level subdirs
        # depth.
        try:
            import ctypes
            # May test GetDriveTypeW…
            GetDriveTypeW = ctypes.windll.kernel32.GetDriveTypeW
            GetDriveTypeW.argtypes = [ ctypes.c_wchar_p ]  # LPCTSTR
            for driveletter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                try:
                    drivepath = "{}:\\".format(driveletter)
                    drivetype = GetDriveTypeW(drivepath)
                    if drivetype != 3:  # 3 = DRIVE_FIXED
                        continue
                    if drivepath not in searchdirs:
                        searchdirs.append(drivepath)
                    diskdirs = [osp.join(drivepath, x) for x in os.listdir(drivepath)]
                    diskdirs = [x for x in diskdirs if osp.isdir(x) and x not in searchdirs]
                    searchdirs.extend(diskdirs)
                except PermissionError:
                    pass
        except:
            pass

    # Any posix OS (including Linux, *BSD… (so MacOSX), cygwin on Windows).
    if ON_POSIX:
        searchdirs.extend([
            '/usr/bin',
            '/usr/lib',
            '/usr/local/bin',
            '/usr/local/lib',
            '/opt',
            '/opt/bin',
            '/opt/lib',
            '/opt/local/bin',
            '/opt/local/lib'])
    # And finally MacOSX.
    if ON_MACOSX:
        searchdirs.extend([
            '/Applications',
            '/Applications/bin',
            '/Library/Frameworks',
        ])

    # Will search for any *directory* matching tree … tagger …
    # without case distinction.
    matchname = re.compile("tree.?tagger.*", re.IGNORECASE)

    # Search looks into subdirectories at one depth of searchdirs,
    # and stop at first match subdir having itself a bin/ and a lib/
    # subdirectories.
    founddir = None
    for directory in searchdirs:
        try:
            if not osp.isdir(directory):
                continue
            for candidate in os.listdir(directory):
                if not osp.isdir(osp.join(directory, candidate)):
                    continue
                if matchname.match(candidate) is not None:
                    # Check if ad-hoc subdirectories are here too.
                    if osp.isdir(osp.join(directory, candidate, "bin")) and \
                            osp.isdir(osp.join(directory, candidate, "lib")):
                        founddir = osp.join(directory, candidate)
                        break
        except PermissionError:     # Some directories may not be listable.
            pass
        if founddir is not None:
            break

    if founddir is None:
        logger.error("Failed to find TreeTagger from automatic directories list.")
        logger.error("If you installed TreeTagger in a standard place, please "
                     "contact the treetaggerwrapper author to add this place to this list.")
        logger.error("To continue working, setup TAGDIR env var to TreeTagger directory.")
    else:
        logger.info("Found TreeTagger directory: %s", founddir)
        if not g_config.has_section("CACHE"):
            g_config.add_section("CACHE")
        g_config.set('CACHE', "# Data in this section may be overwritten "
                              "by treetagger wraper.", '')
        g_config.set('CACHE', 'TAGDIR', founddir)
        save_configuration()

    return founddir


# ==============================================================================
def load_configuration():
    """Load configuration file for the TreeTagger wrapper.

    This file is used mainly to store last automatically found directory
    of TreeTagger installation.
    It can also be used ot override some default working parameters of this
    script.
    """
    if 'XDG_CONFIG_HOME' in os.environ:
        confdir = os.environ['XDG_CONFIG_HOME']
    else:
        confdir = osp.join(osp.expanduser("~"), '.config')
    ttconf = osp.join(confdir, CONFIG_FILENAME)

    if osp.isfile(ttconf):
        if six.PY2:
            with io.open(ttconf, "rb") as f:
                g_config.readfp(f)
        else:  # six.PY3
            with io.open(ttconf, "r", encoding="utf-8") as f:
                g_config.readfp(f)

                # TODO: load new g_language configurations from configuration file,
                # overriding existing definitions if already present.


# We automatically load the configuration on module loading.
load_configuration()


# ==============================================================================
def save_configuration():
    """Save configuration file for the TreeTagger wrapper.
    """
    if 'XDG_CONFIG_HOME' in os.environ:
        confdir = os.environ['XDG_CONFIG_HOME']
    else:
        confdir = osp.join(osp.expanduser("~"), '.config')
    ttconf = osp.join(confdir, CONFIG_FILENAME)

    if not osp.isdir(confdir):  # Ensure confdir exists.
        os.makedirs(confdir)

    if six.PY2:
        with io.open(ttconf, "wb") as f:
            g_config.write(f)
    else:  # six.PY3
        with io.open(ttconf, "w", encoding="utf-8") as f:
            g_config.write(f)


# ==============================================================================
def get_param(paramname, paramsdict, defaultvalue):
    """Search for a working parameter value.

    It is searched respectively in:

    1. parameters given at :class:`TreeTagger` construction.
    2. environment variables.
    3. configuration file, in ``[CONFIG]`` section.
    4. default value.
    """
    if paramname in paramsdict:
        param = paramsdict[paramname]
        logger.debug("Found param %s in paramsdict.", paramname)
        # Consume parameter from dict.
        del paramsdict[paramname]
    elif paramname in os.environ:
        param = os.environ[paramname]
        logger.debug("Found param %s in env vars.", paramname)
    elif g_config.has_section("CONFIG") and g_config.has_option('CONFIG', paramname):
        param = g_config.get('CONFIG', paramname)
        logger.debug("Found param %s in config file.", paramname)
    else:
        param = defaultvalue
        logger.debug("Use default value for param %s.", paramname)
    return param


# ==============================================================================
def make_tags(result, exclude_nottags=False, allow_extra=False):
    """Tool function to transform a list of TreeTagger tabbed text output strings
    into a list of ``Tag``/``TagExtra``/``NotTag`` named tuples.

    You call this function using the result of a :meth:`TreeTagger.tag_text`
    call. ``Tag`` and ``TagExtra`` have attributes ``word``, ``pos`` and
    ``lemma``.
    ``TagExtra`` has an ``extra`` attribute containing a tuple of tagger's
    output complement values (where numeric values are converted to float).
    ``NotTag`` has a simple attribute ``what``.

    :param result: result of a :meth:`TreeTagger.tag_text` call.
    :param bool exclude_nottags: dont generate ``NotTag`` for wrong size
        outputs. Default to False.
    :param bool allow_extra: build a ``TagExtra`` for outputs longer than
        expected. Default to False.
    """
    newres = []
    for line in result:
        word = pos = lemma = extra = None
        # Separator may vary when using options to request probabilistic
        # informations. We are sure to have a tab to separate the word
        # from remaining of line (and the word may contain a space).
        # For the remaining of line, separator can be tab or space, but
        # items may not contain space.
        items = line.split('\t', 1)
        if len(items) == 2:
            word = items[0]
            items = items[1].split()
            if len(items) >= 2:
                pos = items[0]
                lemma = items[1]
            if len(items) >= 3:
                extra = items[2:]
                for i, e in enumerate(extra):
                    try:
                        extra[i] = float(e)
                    except:
                        pass
                extra = tuple(extra)
        # Built result object upon extracted informations.
        if extra is not None:
            if allow_extra:
                newres.append(TagExtra(word, pos, lemma, extra))
            elif not exclude_nottags:
                newres.append(NotTag(line, ))
        elif word is not None and pos is not None and lemma is not None:
            newres.append(Tag(word, pos, lemma))
        elif not exclude_nottags:
            newres.append(NotTag(line, ))
    return newres


# ==============================================================================
class TaggerPoll(object):
    """Keep a poll of TreeTaggers for processing with different threads.

    This class is here for people preferring natural language processing
    over multithread programming… :-)

    Each poll manage a set of threads, able to do parallel chunking, and a
    set of taggers, able to do (more real) parallel tagging.
    All taggers in the same poll are created for same processing (with
    same options).

    :class:`TaggerPoll` objects has same high level interface than :class:`TreeTagger`
    ones with ``_async`` at end of methods names.
    Each of …_asynch method returns a :class:`Job` object allowing to know if
    processing is finished, to wait for it, and to get the result.

    If you want to **properly terminate** a :class:`TaggerPoll`, you must
    call its :func:`TaggerPoll.stop_poll` method.

    .. note::

        Parallel processing via threads in Python within the same
        process is limited due to the global interpreter lock
        (Python's GIL).
        See :ref:`polls of taggers process` for real parallel process.

    **Example of use**

    In this example no parameter is given to the poll, it auto-adapt
    to the count of CPU cores.

    .. code:: python

        import treetaggerwrapper as ttpw
        p = ttpw.TaggerPoll()

        res = []
        text = "This is Mr John's own house, it's very nice."
        print("Creating jobs")
        for i in range(10):
            print("\tJob", i)
            res.append(p.tag_text_async(text))
        print("Waiting for jobs to be completed")
        for i, r in enumerate(res):
            print("\tJob", i)
            r.wait_finished()
            print(r.result)
        p.stop_poll()
        print("Finished")
    """
    def __init__(self, workerscount=None, taggerscount=None, **kwargs):
        """Creation of a new TaggerPoll.

        By default a :class:`TaggerPoll` creates same count of threads and
        of TreeTagger objects than there are CPU cores on your computer.

        :param workerscount: number of worker threads to create.
        :type workerscount: int
        :param taggerscount: number of TreeTaggers objects to create.
        :type taggerscount: int
        :param kwargs: same parameters as :func:`TreeTagger.__init__`.
        """
        if workerscount is None:
            workerscount = multiprocessing.cpu_count()
        if taggerscount is None:
            taggerscount = multiprocessing.cpu_count()
        # Security, we need at least one worker and one tagger.
        if taggerscount < 1:
            raise ValueError("Invalid taggerscount %s", taggerscount)
        if workerscount < 1:
            raise ValueError("Invalid workerscount %s", workerscount)

        if DEBUG_MULTITHREAD:
            logger.debug("Creating TaggerPoll, %d workers, %d taggers",
                         workerscount,taggerscount )

        self._stopping = False
        self._workers = []
        self._waittaggers = queue.Queue()
        self._waitjobs = queue.Queue()

        self._build_taggers(taggerscount, kwargs)
        self._build_workers(workerscount)

        if DEBUG_MULTITHREAD:
            logger.debug("TaggerPoll ready")

    def _build_taggers(self, taggerscount, taggerargs):
        if DEBUG_MULTITHREAD:
            logger.debug("Creating taggers for TaggerPoll")
        for i in range(taggerscount):
            tt = TreeTagger(**taggerargs)
            self._waittaggers.put(tt)

    def _build_workers(self, workerscount):
        if DEBUG_MULTITHREAD:
            logger.debug("Creating workers for TaggerPoll")
        for i in range(workerscount):
            th = threading.Thread(target=self._worker_main)
            th.daemon = True
            self._workers.append(th)
            th.start()

    def _create_job(self, methname, **kwargs):
        if self._stopping:
            raise TreeTaggerError("TaggerPoll is stopped working.")
        job = Job(self, methname, kwargs)
        if DEBUG_MULTITHREAD:
            logger.debug("Job %d created, queuing it", id(job))
        self._waitjobs.put(job)
        return job

    def _worker_main(self):
        while True:
            if DEBUG_MULTITHREAD:
                logger.debug("Worker waiting for job to pick…")
            job = self._waitjobs.get()  # Pickup a job.
            if job is None:
                if DEBUG_MULTITHREAD:
                    logger.debug("Worker finishing")
                break   # Put Nones in jobs queue to stop workers.
            if DEBUG_MULTITHREAD:
                logger.debug("Worker doing picked job %d", id(job))
            job._execute()                       # Do the job

    def stop_poll(self):
        """Properly stop a :class:`TaggerPoll`.

        Takes care of finishing waiting threads, and deleting TreeTagger
        objects (removing pipes connexions to treetagger process).

        Once called, the :class:`TaggerPoll` is no longer usable.
        """
        if DEBUG_MULTITHREAD:
            logger.debug("TaggerPoll stopping")
        if not self._stopping:          # Just stop one time.
            if DEBUG_MULTITHREAD:
                logger.debug("Signaling to threads")
            self._stopping = True       # Prevent more Jobs to be queued.
            # Put one None by thread (will awake threads).
            for x in range(len(self._workers)):
                self._waitjobs.put(None)
        # Wait for threads to be finished.
        for th in self._workers:
            if DEBUG_MULTITHREAD:
                logger.debug("Signaling to thread %s (%d)", th.name, id(th))
            th.join()
        # Remove refs to threads.
        if hasattr(self, '_workers'):
            del self._workers
        # Remove references to TreeTagger objects.
        if hasattr(self, '_waittaggers'):
            del self._waittaggers
        if DEBUG_MULTITHREAD:
            logger.debug("TaggerPoll stopped")

    #---------------------------------------------------------------------------
    # Below methods have same interface than TreeTagger to tag texts.
    # --------------------------------------------------------------------------
    def tag_text_async(self, text, numlines=False, tagonly=False,
                       prepronly=False, tagblanks=False, notagurl=False,
                       notagemail=False, notagip=False, notagdns=False,
                       nosgmlsplit=False):
        """
        See :func:`TreeTagger.tag_text` method and :class:`TaggerPoll` doc.

        :return: a :class:`Job` object about the async process.
        :rtype: :class:`Job`
        """
        return self._create_job('tag_text', text=text, numlines=numlines,
                                tagonly=tagonly, prepronly=prepronly,
                                tagblanks=tagblanks, notagurl=notagurl,
                                notagemail=notagemail, notagip=notagip,
                                notagdns=notagdns, nosgmlsplit=nosgmlsplit)

    # --------------------------------------------------------------------------
    def tag_file_async(self, infilepath, encoding=USER_ENCODING,
                       numlines=False, tagonly=False,
                       prepronly=False, tagblanks=False, notagurl=False,
                       notagemail=False, notagip=False, notagdns=False,
                       nosgmlsplit=False):
        """
        See :func:`TreeTagger.tag_file` method and :class:`TaggerPoll` doc.

        :return: a :class:`Job` object about the async process.
        :rtype: :class:`Job`
        """
        return self._create_job('tag_file', infilepath=infilepath,
                                encoding=encoding, numlines=numlines,
                                tagonly=tagonly, prepronly=prepronly,
                                tagblanks=tagblanks, notagurl=notagurl,
                                notagemail=notagemail, notagip=notagip,
                                notagdns=notagdns, nosgmlsplit=nosgmlsplit)

    # --------------------------------------------------------------------------
    def tag_file_to_async(self, infilepath, outfilepath, encoding=USER_ENCODING,
                          numlines=False, tagonly=False,
                          prepronly=False, tagblanks=False, notagurl=False,
                          notagemail=False, notagip=False, notagdns=False,
                          nosgmlsplit=False):
        """
        See :func:`TreeTagger.tag_file_to` method and :class:`TaggerPoll` doc.

        :return: a :class:`Job` object about the async process.
        :rtype: :class:`Job`
        """
        return self._create_job('tag_file_to', infilepath=infilepath,
                                outfilepath=outfilepath,
                                encoding=encoding, numlines=numlines,
                                tagonly=tagonly, prepronly=prepronly,
                                tagblanks=tagblanks, notagurl=notagurl,
                                notagemail=notagemail, notagip=notagip,
                                notagdns=notagdns, nosgmlsplit=nosgmlsplit)

class Job(object):
    """Asynchronous job to process a text with a Tagger.

    These objects are automatically created for you and returned by
    :class:`TaggerPoll` methods :func:`TaggerPoll.tag_text_async`,
    :func:`TaggerPoll.tag_file_async` and :func:`TaggerPoll.tag_file_to_async`.

    You use them to know status of the asynchronous request, eventually
    wait for it to be finished, and get the final result.

    :ivar finished: Boolean indicator of job termination.
    :ivar result: Final job processing result — or exception.
    """
    def __init__(self, poll, methname, kwargs):
        self._poll = poll
        self._methname = methname
        self._kwargs = kwargs
        self._event = threading.Event()
        self._finished = False
        self._result = None

    def _execute(self):
        # Pickup a tagger.
        logger.debug("Job %d waitin for a tagger", id(self))
        tagger = self._poll._waittaggers.get()
        if DEBUG_MULTITHREAD:
            logger.debug("Job %d picked tagger %d for %s", id(self),
                         id(tagger), self._methname)
        try:
            meth = getattr(tagger, self._methname)
            self._result = meth(**self._kwargs)
        except Exception as e:
            if DEBUG_MULTITHREAD:
                logger.debug("Job %d exit with exception", id(self))
            self._result = e
        # Release the tagger, signal the Job end of processing.
        if DEBUG_MULTITHREAD:
            logger.debug("Job %d give back tagger %d", id(self),
                         id(tagger))
        self._poll._waittaggers.put(tagger)
        self._finished = True
        self._event.set()
        if DEBUG_MULTITHREAD:
            logger.debug("Job %d finished", id(self))

    @property
    def finished(self):
        return self._finished

    def wait_finished(self):
        """Lock on the Job event signaling its termination.
        """
        self._event.wait()

    @property
    def result(self):
        return self._result


# ==============================================================================
help_string = """treetaggerwrapper.py

Usage:
    python treetaggerwrapper.py [options] input_file

Read data from specified files, process them one by one, sending data to
TreeTagger, and write TreeTagger output to files with .{RESEXT} extension.

    python treetaggerwrapper.py [options] --pipe < input_stream > output_stream

Read all data from the input stream, then preprocess it, send it to
TreeTagger, and write  TreeTagger output to output stream.

Options:
    -p          preprocess only (no tagger)
    -t          tagger only (no preprocessor)
    -n          number lines of original text as SGML tags
    -b          transform blanks into SGML tags
    -l lang     language to tag (es de fr en, default to en)
                if tagger only (-t option), you can also use languages
                bg nl et fi gl it la mn pl ru sk sw
    -d dir      TreeTagger base directory (may be automatically detected)
    -e enc      encoding used for user data (default to {USER_ENCODING})

Other options:
    --version               print script version and exit.
    --ttparamfile fic       file to use as TreeTagger parameter file.
    --ttoptions "options"   TreeTagger specific options (cumulated).
    --abbreviations fic     file to use as abbreviations terms.
    --pipe                  use pipe mode on standard input/output 
                            (cannot provide files on command line).
    --encerrors err         management of encoding errors for user data,
                            strict or ignore or replace (default
                            to strict).
    --debug                 enable debugging log file (treetaggerwrapper.log)
    --numlines              number lines with sgml tags (as -n).
    --tagonly               only tag text, no chunking (as -t).
    --prepronly             only chunking, no tagging (as -p).
    --tagblanks             insert sgml tags for blank chars (as -b).
    --notagurl              don't insert sgml tags for URLs.
    --notagemail            don't insert sgml tags for emails.
    --notagip               don't insert sgml tags for ip addresses.
    --notagdns              don't insert sgml tags for dns names.
    --nosgmlsplit           don't split on sgml/xml markups.
    
Options you should not have to use:
    --ttinencoding enc      encoding to use for TreeTagger input
    --ttoutencoding enc     encoding to use for TreeTagger output
    --ttinencerr err        management of encoding errors for TreeTagger
                            input encoding, strict or ignore or replace
                            (default to replace).
    --ttoutencerr err       management of encoding errors for TreeTagger
                            output decoding, strict or ignore or replace
                            (default to replace).

This Python module can be used as a tool for a larger project by creating a
TreeTagger object and using its tag_text method.
It tries to guess Treetagger directory installation. If it fails, you
have to setup a TAGDIR environment variable containing TreeTagger installation
directory path.

Note: in pipe mode -e enc option is only considered if stdin/stdout has
no encoding information associated (typically with char flow  using shell pipes
or direct files content using shell redirections).

Note: When numbering lines, you must ensure that SGML/XML tags in your data
file doesn't split around lines (else you will get line numberning tags into
your text tags... with bad result on tags recognition by regular expression).

Examples with pipe:

Once installed in the PYTHONPATH, the module can be used from anywhere
Using Python -m option. Combined with pipe, you can easily do some tests
(console encoding is detected if possible, default to {USER_ENCODING} if
not detected ; can use -e option to change):

To preprocess and tag a small text:

    echo "This is the sentence." | python -m treetaggerwrapper --pipe

To just see preprocessing (chunking) result:

    echo "This is the sentence." | python -m treetaggerwrapper --pipe --prepronly

To just see tagging (TreeTagger call) result:

    echo -e "This\nis\nthe\nsentence\n." | python -m treetaggerwrapper --pipe --tagonly

Written by Laurent Pointal <laurent.pointal@limsi.fr> for CNRS-LIMSI.
Alternate email: <laurent.pointal@laposte.net>
""".format(RESEXT=RESEXT, USER_ENCODING=USER_ENCODING)


def main(*args):
    """Test/command line usage code.

    See command line usage help with::

      python treetaggerwrapper.py --help

    or::

        python -m treetaggerwrapper --help
    """
    if args and args[0].lower() in ("-h", "h", "--help", "-help", "help",
                                    "--aide", "-aide", "aide", "?"):
        print(help_string)
        sys.exit(0)

    # Set default, then process options.
    numlines = tagonly = prepronly = tagblanks = pipemode = False
    filesencoding = USER_ENCODING
    encerrors = "strict"
    tagonly = prepronly = tagblanks = notagurl = False
    notagemail = notagip = notagdns = nosgmlsplit = False
    tagbuildopt = {}
    try:
        optlist, args = getopt.getopt(args, 'ptnl:d:be:', ["version", "abbreviations=",
                                                           "ttparamfile=", "ttoptions=", "pipe",
                                                           "ttinencoding=", "ttoutencoding=",
                                                           "ttinencerr=", "ttoutencerr=",
                                                           "debug", "numlines",
                                                           "tagonly", "prepronly",
                                                           "tagblanks", "notagurl", "notagemail",
                                                           "notagip", "notagdns", "nosgmlsplit"])
    except getopt.GetoptError as err:
        print("Error,", err)
        print("See usage with: python treetaggerwrapper.py --help")
        sys.exit(-1)

    for opt, val in optlist:
        if opt == "--debug":
            enable_debugging_log()
        if opt == '-p':
            prepronly = True
        elif opt == '-t':
            tagonly = True
        elif opt == '-n':
            numlines = True
        elif opt == '-l':
            tagbuildopt["TAGLANG"] = val
        elif opt == '-b':
            tagblanks = True
        elif opt == '-d':
            tagbuildopt["TAGDIR"] = val
        elif opt == '-e':
            filesencoding = val
        elif opt == "--ttparamfile":
            tagbuildopt["TAGPARFILE"] = val
        elif opt == "--ttoptions":
            tagbuildopt["TAGOPT"] = tagbuildopt.get("TAGOPT", "") + " " + val
        elif opt == "--abbreviations":
            tagbuildopt["TAGABBREV"] = val
        elif opt == "--pipe":
            pipemode = True
        elif opt == "--ttinencoding":
            tagbuildopt["TAGINENC"] = val
        elif opt == "--ttoutencoding":
            tagbuildopt["TAGOUTENC"] = val
        elif opt == "--ttinencerr":
            tagbuildopt["TAGINENCERR"] = val
        elif opt == "--ttoutencerr":
            tagbuildopt["TAGOUTENCERR"] = val
        elif opt == "--numlines":
            numlines = True
        elif opt == "--tagonly":
            tagonly = True
        elif opt == "--prepronly":
            prepronly = True
        elif opt == "--tagblanks":
            tagblanks = True
        elif opt == "--notagurl":
            notagurl = True
        elif opt == "--notagemail":
            notagemail = True
        elif opt == "--notagip":
            notagip = True
        elif opt == "--notagdns":
            notagdns = True
        elif opt == "--nosgmlsplit":
            nosgmlsplit = True
        elif opt == "--version":
            print("treetaggerwrapper.py", __version__)
            sys.exit(0)

    # Find files to process.
    files = []
    for f in args:
        files.extend(glob.glob(f))

    if pipemode and files:
        enable_debugging_log()
        logger.error("Cannot use pipe mode with files.")
        logger.info("See online help with --help.")
        return -1

    if DEBUG: logger.info("files to process: %r", files)
    logger.info("filesencoding=%s", filesencoding)
    tagger = TreeTagger(**tagbuildopt)

    if pipemode:
        # Find in/out encoding for pipe.
        if hasattr(sys.stdin, "encoding") and sys.stdin.encoding is not None:
            inencoding = sys.stdin.encoding
        else:
            inencoding = filesencoding
        if hasattr(sys.stdout, "encoding") and sys.stdout.encoding is not None:
            outencoding = sys.stdout.encoding
        else:
            outencoding = filesencoding
        logger.info("Processing with stdin/stdout, reading input.")
        text = sys.stdin.read()
        if six.PY2:
            text = text.decode(inencoding, encerrors)

        logger.info("Processing with stdin/stdout, tagging.")
        res = tagger.tag_text(text, numlines=numlines, tagonly=tagonly,
                              prepronly=prepronly, tagblanks=tagblanks, notagurl=notagurl,
                              notagemail=notagemail, notagip=notagip, notagdns=notagdns,
                              nosgmlsplit=nosgmlsplit)

        logger.info("Processing with stdin/stdout, writing to stdout.")
        res = "\n".join(res)
        if six.PY2:
            res = res.encode(outencoding, encerrors)
        sys.stdout.write(res)
        logger.info("Processing with stdin/stdout, finished.")
    else:
        for f in files:
            fout = f + "." + RESEXT
            tagger.tag_file_to(f, fout, encoding=filesencoding,
                               numlines=numlines, tagonly=tagonly,
                               prepronly=prepronly, tagblanks=tagblanks, notagurl=notagurl,
                               notagemail=notagemail, notagip=notagip, notagdns=notagdns,
                               nosgmlsplit=nosgmlsplit)

    logger.info("treetaggerwrapper.py - process terminate normally.")
    return 0


# ==============================================================================
if __name__ == "__main__":
    if DEBUG: enable_debugging_log()
    try:
        sys.exit(main(*(sys.argv[1:])))
    except TreeTaggerError:
        if not DEBUG:
            print("##### Try running with --debug option to get more informations #####")
        raise
