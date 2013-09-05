.. _readme:

=====
Tobin
=====

.. rubric:: Schematics, Data, and Databases.

Tobin is a data persistence layer for `Schematics <http://github.com/j2labs/schematics>`_.  We store data in denormalized
form and perform joins in software.  Good habits early make smoother sailing
later.

This project is named after Amon Tobin, a musician I am regularly inspired by.
If you're not familiar with his work, `try Hey Mr. Tree first
<http://www.youtube.com/watch?v=1JCZCYB0df0>`_.


Quick Example
=============

First, let's create a song model.

.. code:: Python

  from schematics.models import Model
  from schematics.types import StringType, URLType
  from schematics.types.serializable import serializable


  class Song(Model):
      name = StringType()
      artist = StringType()
      url = URLType()
      @serializable
      def id(self):
          return '%s/%s' % (self.artist, self.name)

Create a couple song instances.

.. code:: Python

  >>> s1 = Song()
  >>> s1.name = 'Hey Mr. Tree'
  >>> s1.artist = 'Amon Tobin'
  >>> s1.url = 'http://www.youtube.com/watch?v=1JCZCYB0df0'
  >>>
  >>> s2 = Song()
  >>> s2.artist = 'Shipyards'
  >>> s2.name = 'Headfirst Dive'
  >>> s2.url = 'https://soundcloud.com/shipyards/headfirst-dive'

Tobin aims for key-value'ish behavior, but we haven't set an id on the model.
Instead, we will use a function to generate the key from field values.  In this
case, we join the artist name and song name for a composite key.

Instantiate the query set and then save.
 
  >>> from tobin.base import DictQuerySet
  >>> dqs = DictQuerySet()
  >>> dqs.create(Song, [s1, s2])

Looping across data looks like this:

  >>> for (status, datum) in dqs.read(Song):
  ...     print datum
  ... 
  {'url': u'http://www.youtube.com/watch?v=1JCZCYB0df0', 'id': 'Amon Tobin/Hey Mr. Tree', 'name': u'Hey Mr. Tree', 'artist': u'Amon Tobin'}
  {'url': u'https://soundcloud.com/shipyards/headfirst-dive', 'id': 'Shipyards/Headfirst Dive', 'name': u'Headfirst Dive', 'artist': u'Shipyards'}

We could instantiate these as models too:

  >>> songs = list()
  >>> for (status, datum) in dqs.read(Song):
  ...     song = Song(datum)
  ...     songs.append(song)
  ... 
  >>> songs
  [<Song: Song object>, <Song: Song object>]

