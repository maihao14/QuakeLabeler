
.. figure:: Images/slc_logo.png
   :align: center

Licence
=======

Copyright 2021 Hao Mai & Pascal Audet

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Installation
============

Dependencies
------------

The current version has been tested using **Python3.7 and 3.8** \
Also, the following packages are required:

- `obspy <https://github.com/obspy/obspy/>`_
- `requests <https://github.com/psf/requests/>`_

Required packages (e.g., ``obspy``)
will be automatically installed by ``SeisLabelCreator``.

Conda environment
-----------------

We recommend creating a custom ``conda`` environment
where ``SeisLabelCreator`` can be installed along with some of its dependencies.

.. sourcecode:: bash

   conda create -n slc python=3.8 obspy -c conda-forge

Activate the newly created environment:

.. sourcecode:: bash

   conda activate slc


Installing from Pypi
--------------------

*This option is not available at this time*

Installing from source
----------------------

- Clone the repository:

.. sourcecode:: bash

   git clone https://github.com/maihao14/SeisLabelCreator.git
   cd SeisLabelCreator


- Install using pip:

.. sourcecode:: bash

   pip install .

Running the scripts
===================

Quick Start
-----------

Create a work folder where you will run the scripts that accompany
``SeisLabelCreator``. For example:

.. sourcecode:: bash

   mkdir ~/WorkFolder
   cd WorkFolder

Run the main script ``SeisCreator`` with default arguments:

.. sourcecode:: bash

   SeisCreator
