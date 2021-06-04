QuakeLabeler Tutorial
=====================

Overview
--------

Preparing training dataset is the first step of machine learning. However annotate
seismic label is a time consuming and tedious work. ``QuakeLabeler`` ``(QL)`` is your
best solution to automatic produce earthquake labels. To save your time for the next
brilliant AI method.

``QuakeLabeler`` runs in a very human way and it can help researchers to create
training data with little experience of making labels. The rendered datasets
is mainly prepared for the training procedure of subsequent machine learning
(deep learning) applications. For example:
    #. Earthquake detection;
    #. Phase picking;
    #. Waveform classification;
    #. Magnitude prediction.
    #. Earthquake location.

``QuakeLabeler`` is a Python package containing command-line interactive
tools to help you quick deploy your personal seismic datasets. ``QuakeLabeler``
provides one-stop service to convert raw seismic data into valuable training datasets
for machine learning through professional collection and annotation techniques.

Data Collection
+++++++++++++++

Artificial intelligence (AI) needs significant amount of high-quality training data.
In Seismology, we don't lack raw data. While for AI research, proper data can be difficult
and time-consuming to collect (revise from original seismic traces).

Different from other static seismic datasets, ``QL`` provides flexible tailored data.
``QL`` first retrieves raw seismic data from online data centres (i.e. IRIS). Then
transfer these data(seismograms) into standard training samples. Several signal pre-processing
methods are implemented to ensure the datasets to final reach user's demands.

Data Annotation
+++++++++++++++
With annotated data, models learn to handle complex scenarios. The higher the data accuracy,
the better the model performance. With a wide-range of data annotation tools, ``QL`` can
automatic create seismic labels according to user's input options. So you never need worry about
the export data format have trouble with your AI models.

Workflow
--------
``QuakeLabeler`` has a tight pipeline of functions. It automatically builds required seismic
datasets. Here are the main steps of the producing procedure:
    #. Define research region and time range
    #. Design dataset

        - Custom waveform formats
        - Custom dataset formats
        - Custom export formats

    #. Request data from online data center
    #. Signal processing
    #. Annotation
    #. Make dataset
    #. Export statistical results

Usage
-----
Start ``QuakeLabeler`` in any of your interactive shell (eg. in ``macOS``, open ``terminal``),
type::

    # get start QuakeLabeler
    QuakeLabeler

``QuakeLabeler`` will initialize and notify you select one of the running mode::

    (ql) hao@HaodeMacBook-Pro QuakeLabeler % QuakeLabeler
    Welcome to QuakeLabeler----Fast AI Earthquake Dataset Deployment Tool!
    QuakeLabeler provides multiple modes for different levels of Seismic AI researher

    [Beginner] mode -- well prepared case studies;
    [Advanced] mode -- produce earthquake samples based on Customized parameters.

    Please select a mode: [1/Beginner/2/Advanced]

Beginner Mode
-------------

If you have little knowledge of how to create training dataset, ``Beginner``
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
    Therefore you need to wait, also the script will notify this::

        Loading time varies on your network connections, search region scale, time range, etc. Please be patient, estimated time: 3 mins
        Request completed！！！
        1525 events have been found!

Once you are informed the events has been found. The script will run into next step.
``QL`` will ask you to input following settings to generate datasets::

    Please define your own expectation for Seismic labeled samples:

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
input the `key words which fit your preference. Note that for some question, you
can input multiple key words (e.g., `SACMAT` or `MAT_MiniSeed) ::

    # Leave blank if you wish to apply default options
    Do you want to add random noise: [y/n] n
    Select export file format: [SAC/MSEED/SEGY/NPZ/MAT]SAC
    Save as single trace or multiple-component seismic data? [y/n]
    Do you want to separate save traces as input and output? [y/n]
    Do you want to separate save arrival information as a CSV file? [y/n]
    Please input a folder name for your dataset (optional):
    Do you want to generate statistical charts after creating the dataset? [y/n]
.. tip ::
    As a beginner, feel free to skip the option you do not know how to select y
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

.. note ::
    If you use ``n`` option for `multiple-component seismic data`, then every ``Stream``
    will hold all available components from one station at the event time. See the above
    print information, the last Stream object has 6 available Trace(s) as one rendered sample.


Advanced Mode
-------------

If you are already an expert in machine learning. You can apply ``advanced`` mode to fill in
all customized options for your search fields. As simple as `beginner` mode, you can start in
your interactive shell with command::

    QuakeLabeler

Select ``2`` or ``Advanced`` to enter::

    # type 2 also works
    Advanced

``QL`` will initiate advanced mode once it received valid input::

    Initialize Advanced Mode...
    Alternative region options are provided. Please select your preferred input function:

    Please select one :  [STN/GLOBAL/RECT/CIRC/FE/POLY]
                         [STN]: Stations are restricted to specific station code(s);
                         [GLOBAL]: Stations are not restricted by region (i.e. all available stations);
                         [RECT]: Rectangular search of stations (recommended);
                         [CIRC]: Circular search of stations(recommended);
                         [FE]: Flinn-Engdahl region search of stations;
                         [POLY]: Customized polygon search.
.. note ::

    ``QL`` provides multiple ways to select your research region. You can select one best fit your
    study case. In general, we will use ``RECT`` to search in a rectangular region or use ``STN``
    to input certain stations which you concerned. Note that large region usually need long time for
    computing.

Once you enter a specific mode, ``QL`` will run related function to ask you input your regional parameters.
Let's take ``RECT`` function for instance, ``QL`` will request 4 parameters of the rectangular region::

    Please enter the latitudes(-90 ~ 90) at the bottom and top, the longitudes(-180 ~ 180) on the left and the right of the rectangular boundary.

    Input rectangular bottom latitude: 31
    Input rectangular top latitude: 46
    Input rectangular left longitude: -128
    Input rectangular right longitude: -114

When you finish input, ``QL`` will display you input parameters to confirm there is no type-in error::

    The input region is:
    searchshape: RECT
    bot_lat: 31
    top_lat: 46
    left_lon: -128
    right_lon: -114

    Input parameters confirm?  [y/n]
    y

Once you setup research region, you can set time range in the same way::

    Please enter time range:

    Input start year (1900-):
    2010
    Input start month(1-12):
    1
    Input start day (1-31):
    7
    Input start time(00:00:00-23:59:59):
    01:00:00
    Input end year (1900-):
    2010
    Input end month(1-12):
    1
    Input end day (1-31):
    10
    Input end time(00:00:00-23:59:59):
    03:00:00
    start_year: 2010
    start_month: 1
    start_day: 7
    start_time: 01:00:00
    end_year: 2010
    end_month: 1
    end_day: 10
    end_time: 03:00:00

    Input parameters confirm?  [y/n]
    y

Apart from research region and time range, the following input are optional,
e.g., you can select magnitude range or specific
magnitude type which you interest in. You can skip these questions, ``QL`` will
use default options::

    Enter event magnitude limits (optional, enter blank space for default sets)
    Input minimum magnitude (0.0-9.0 or blank space for skip this set):

    Input maximum magnitude (0.0-9.0 or blank space for skip this set):

    Enter specific magnitude types. Please note: the selected magnitude type will search for all possible magnitudes in that category:
                       E.g. MB will search for mb, mB, Mb, mb1mx, etc
                       Available input:
                       <Any>|<MB>|<MS>|<MW>|<ML>|<MD> or blank space for skip this set

After the above specific definitions, subsequent options are same as ``beginner`` mode.
User will go through all questions to define their dataset ::

    How many samples do you wish to create? [1- ] (input MAX for all available waveform):5000
    Do you want fixed sample length? [y/n] (default: y):y
    Enter sample length (how many sample points do you wish in a trace)?(default 5000): 5000
    Select label type: [simple/specific]?
    [simple]: P/S;
    [specific]: P/Pn/Pb/S/Sn, etc.
    specific
    Enter a fixed sampling rate(i.e.: 100.0) or skip for keep original sampling rate:
    Select filter function for preprocess? [0/1/2/3]:
    [0]: Do not apply filter function;
    [1]: Butterworth-Lowpass;
    [2]: Butterworth-Highpass;
    [3]: Butterworth-Bandpass. 0
    Do you want to detrend the waveforms ? [y/n]n
    Would you like random input? [y/n]y
    Do you want to add random noise: [y/n] n
    Select export file format: [SAC/MSEED/SEGY/NPZ/MAT]SAC
    Save as single trace or multiple-component seismic data? [y/n]y
    Do you want to separate save traces as input and output? [y/n]y
    Do you want to separate save arrival information as a CSV file? [y/n]y
    Please input a folder name for your dataset (optional): NewDataset
    Do you want to generate statistical charts after creating the dataset? [y/n]y

.. note ::

    - Time varies based on the dataset volume.
    - Only use pre-processing options if it's necessary.
