QuakeLabeler Tutorial
=====================

Overview
--------

``QuakeLabeler`` (QL) is a Python package containing command-line interactive
tools to help you quick deploy your personal seismic datasets. ``QuakeLabeler``
collects seismograms from online data centres (i.e. IRIS) based on user's input
options. Then ``QuakeLabeler`` can automatic run a series of signal processing
methods and data augmenting techniques also based on user's needs. After that
raw seismic data will be transformed to acceptable training samples. Finally
``QL`` will annotate these samples with manual reviewed event information (arrival time,
phase name, magnitude, etc), generate datasets and statistical figures.

``QuakeLabeler`` runs in a very human way and it can help researchers to create
training data with little experience of making labels. The rendered datasets
is mainly prepared for the training procedure of subsequent machine learning
(deep learning) applications. For example:
    #. Earthquake detection;
    #. Phase picking;
    #. Waveform classification;
    #. Magnitude prediction.
    #. Earthquake location.

Usage
-----
Start ``QuakeLabeler`` in any of your interactive shell (eg. in ``MAC OS``, open ``terminal``),
type::

    # get start QuakeLabeler
    QuakeLabeler

``QuakeLabeler`` will initialize and hint you select one of the running mode::

    (ql) hao@HaodeMacBook-Pro QuakeLabeler % QuakeLabeler
    Welcome to QuakeLabeler----Fast AI Earthquake Dataset Deployment Tool!
    QuakeLabeler provides multiple modes for different levels of Seismic AI researher

    [Beginner] mode -- well prepared case studies;
    [Advanced] mode -- produce earthquake samples based on Customized parameters.

    Please select a mode: [1/Beginner/2/Advanced]

If you have little knowledge of how to create training dataset, ``[Beginner]``
mode is best for you to quick start::

    # you can also input: 1 or beginner for simplify.
    Beginner

The package will start ``Beginner`` function, several study regions are listed
for you to choose::

    Initialize Beginner Mode...
    Select one of the following sample fields:  [1/2/3/4]
                       [1] 2010 Cascadia subduction zone earthquake activities
                       [2] 2011 Tōhoku earthquake and tsunami
                       [3] 2016 Oklahoma human activity-induced earthquakes
                       [4] 2018 Big quakes in Southern California
                       [0] Re-direct to Advanced mode.

For example, you can enter ``1`` to create training data base on 2010 Cascadia
subduction zone earthquake activities, ``QL`` will automatically search event
information from default online data center (``IRIS``)::

    1

.. note::
    Request event information (catalog) from online data center needs time.
    Therefore you need to wait, also the script will hint this::

        Loading time varies on your network connections, search region scale, time range, etc. Please be patient, estimated time: 3 mins
        Request completed！！！
        1525 events have been found!

Once you are informed the events has been found. The script will run into next step.
``QL`` will ask you to input following settings to generate datasets::

    Please define your own expection for Seismic labled samples:

    How many samples do you wish to create? [1- ] (input MAX for all available waveform):

The first question is about the total number (volume) of samples you wish to create,
for basic machine learning methods, you could enter::

    5000

For deep learning applications, they usually need more than 10,000 samples to avoid overfitting.
``QL`` does not have a maximum volume limit, however process time might be longer when you want to
create a big dataset.

.. caution::
    You need to make sure your local drive has enough memory to save your datasets.

Following questions all runs in the same way, you only need to type in your desired options::

    Do you want fixed sample length? [y/n] (default: y):y

    Enter sample length (how many sample points do you wish in a trace)?(default 5000):

    Select label type: [simple/specific]?
    [simple]: P/S;
    [specific]: P/Pn/Pb/S/Sn,etc.

    Enter a fixed sampling rate(i.e.: 100.0) or skip for keep original sampling rate:
    Select filter function for preprocess? [0/1/2/3]:
    [0]: Do not apply filter function;
    [1]: Butterworth-Lowpass;
    [2]: Butterworth-Highpass;
    [3]: Butterworth-Bandpass.

    Do you want to detrend the waveforms ? [y/n]

    Would you like random input? [y/n]n
    Input waveforms start at: __ seconds before arrival.

It's worth to mention that here are 2 different formats to generate sample segment:

    #. Random Input : Arrival time will be set on random position of the waveform;
    #. Input waveform start at __ seconds before arrival.

For other questions, you can leave them all blank to use ``default`` parameters, or
input the ``key words`` which fit your preference. Note that for some question, you
can input multiple key words (i.e., `SACMAT` or ``MAT_MiniSeed``) ::

    # Leave blank if you wish to apply default options
    Do you want to add random noise: [y/n] n
    Select export file format: [SAC/MSEED/SEGY/NPZ/MAT]SAC
    Save as single trace or multiple-component seismic data? [y/n]
    Do you want to separate save traces as input and output? [y/n]
    Do you want to separate save arrival information as a CSV file? [y/n]
    Please input a folder name for your dataset (optional):
    Do you want to generate statistical charts after creating the dataset? [y/n]

Once the questions are done, ``QL`` will automatic deploy customized dataset::

    Processing |################################| 5/5Save to target folder: MyDataset2021-05-31T10:06
    6 Trace(s) in Stream:
    IU.COR.00.BH1 | 2010-09-07T11:39:49.719539Z - 2010-09-07T11:43:59.669539Z | 20.0 Hz, 5000 samples
    IU.COR.00.BH2 | 2010-09-07T11:39:49.719539Z - 2010-09-07T11:43:59.669539Z | 20.0 Hz, 5000 samples
    IU.COR.00.BHZ | 2010-09-07T11:39:49.719539Z - 2010-09-07T11:43:59.669539Z | 20.0 Hz, 5000 samples
    IU.COR.10.BH1 | 2010-09-07T11:39:49.719538Z - 2010-09-07T11:41:54.694538Z | 40.0 Hz, 5000 samples
    IU.COR.10.BH2 | 2010-09-07T11:39:49.719538Z - 2010-09-07T11:41:54.694538Z | 40.0 Hz, 5000 samples
    IU.COR.10.BHZ | 2010-09-07T11:39:49.719539Z - 2010-09-07T11:41:54.694539Z | 40.0 Hz, 5000 samples

    All available waveforms are ready!
    5 of event-based samples are successfully downloaded!
