Sphinx--Python Docstring Package
++++++++++++++++++++++++++++++++

What is Sphinx
==============
Sphinx is written in Python and supports Python 3.6+.
It builds upon the shoulders of many third-party libraries such as
Docutils and Jinja, which are installed when Sphinx is installed.

Text Formatting
===============

List and Number
---------------
* Use ``*`` for List
* Use ``#.`` for Numbered List

Admonitions
---------------
.. caution::
  This is a caution box.

.. danger::
  This is a danger box.
.. tip::
  This is a tip box.
.. note::
  This is a note box.

Images
---------------
Use this code::

  .. image:: /Images/homepage.png

Codes
---------------
* Simple

  .. note::
    Use ``::`` to note the following sections are codes.
  Example:
    Here's a simple sample to input codes,
    type in::

        #Write your codes Here
        #i.e. Python
        print("Hello Sphinx!")


* Specific

  .. note::

    Use *.. code-block:: python* to note the following sections are python codes.

  Example:

  .. code-block:: python
      #Here's a simple sample to input codes:
      #Type in .. code-block:: python
          #Write your codes Here
          #i.e. Python
          print("Hello Sphinx!")

Tabels
---------------
.. list-table:: Student Information 1
    :widths: 20 10 10 15
    :header-rows: 1

    * - Name
      - Sex
      - Age
      - Address
    * - Lisa
      - Female
      - 20
      - 160 Chapel st.
    * - John
      - Male
      - 23
      - 172 Albert st.

.. csv-table:: Student Information 2
    :header: Name,Sex,Age,Address
    :width:15 10 30 30

    Lisa,Female,20,160 Chapel st.
    John,Male,23,172 Albert st.


.. tip::
   You can click on ``View page source`` to checkout how these functions work
   in rst file.
