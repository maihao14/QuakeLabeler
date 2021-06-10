QuakeLabeler Tutorial
=====================

Overview
--------

Preparing a training dataset is the first step of any machine learning application. In earthquake
seismology, the training dataset often times takes the form of seismic phase labels (e.g., P wave, S wave, etc.). However, labeling seismic waveforms is a time-consuming and tedious task. ``QuakeLabeler`` ``(QL)`` is your best solution to automatically generate seismic waveform labels from large datasets. To save your time for the next brilliant AI method.

``QuakeLabeler`` runs interactively and can help researchers create training data with little prior experience in making labels. The output dataset is then ready for the training step in machine various learning applications, for example:

    #. Earthquake detection;
    #. Phase picking;
    #. Waveform classification;
    #. Magnitude prediction.
    #. Earthquake location.

``QuakeLabeler`` is a Python package containing command-line interactive tools to help you quickly generate your personal seismic datasets. ``QuakeLabeler`` provides a one-stop service to convert raw seismic data into valuable training datasets for machine learning through professional collection and annotation techniques.

Data Collection
+++++++++++++++
Artificial intelligence (AI) techniques require large amounts of high-quality training data. In seismology, we don't lack raw data. However, turning raw waveform data into labels can be difficult
and time-consuming.

In contrast to other static seismic datasets, ``QL`` provides flexible and tailored training data. ``QL`` first retrieves raw seismic waveforms from online data centres (i.e. IRIS DMC) and saves them to disk, then converts these data (seismograms) into standard training samples. Several signal pre-processing methods are available to ensure the datasets meet users' requirements. 

Data Annotation
+++++++++++++++
With labeled data, models learn to handle complex scenarios. The higher the data accuracy, the better the model performance. With a wide range of data labeling tools, ``QL`` can automatically create seismic labels according to users' input options. So you never need to worry about data formatting problems with your AI models.

Workflow
--------
``QuakeLabeler`` has a tight pipeline of functions. It automatically builds required seismic datasets. Here are the main steps of the procedure:

    #. Define research region and time range
    #. Design dataset

        - Custom waveform format
        - Custom dataset format
        - Custom export format

    #. Request data from online data centers
    #. Signal pre-processing
    #. Annotation (labeling)
    #. Compile dataset
    #. Export results and statistics

Usage
-----
Start ``QuakeLabeler`` in any interactive shell of your choice (eg. in ``macOS``, open ``terminal``),
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

If you have little knowledge of how to create a training dataset, select the ``Beginner`` mode ::

    # you can either input: 1 or beginner.
    Beginner

In the ``Beginner`` mode, you can choose a pre-assembled data set from a selection of several study regions::

    Initializing Beginner Mode...
    Select one of the following cases:  [1/2/3/4]
                       [1] 2010 Cascadia subduction zone seismicity
                       [2] 2011 Tōhoku earthquake and tsunami
                       [3] 2016 Oklahoma induced earthquakes
                       [4] 2018 Earthquakes in Southern California
                       [0] Re-direct to Advanced mode.

For example, you can enter ``1`` to create training data based on 2010 Cascadia subduction zone seismicity; ``QL`` will automatically search event information from default online data center (``IRIS``)::

    1

.. note::
    Requesting event information (catalog) from online data center can take time.
    The script will notify you about this::

        Loading time varies based on your network connection, search region scale, time range, etc. Please be patient, estimated time: 3 mins
        Request completed!
        1525 events have been found

Once you are informed the events have been found, the script will proceed to the next step. ``QL`` will ask you to specify the following settings to generate the datasets::

    Please define your own expectation for Seismic labeled samples:

    How many samples do you wish to create? [1- ] (input MAX for all available waveform):

The first question concerns the total number (volume) of samples that you wish to create. For basic machine learning methods, you could enter::

    5000

For deep learning applications, those techniques usually need more than 10,000 samples to avoid overfitting. ``QL`` does not have a maximum volume limit, however processing time can be significant for large datasets.

.. caution::
    You need to make sure your local drive has enough disk space to save your datasets.

The following questions all run in the same way, where you only need to type in your desired options::

    Do you want fixed sample length? [y/n] (default: y):y

    Enter sample length (how many sample points do you wish in a trace)?(default 5000):

    Select label type: [simple/specific]?
    [simple]: P/S;
    [specific]: P/Pn/Pb/S/Sn,etc.

    Enter a fixed sampling rate (e.g.: 100.0) or skip to keep original sampling rate:
    Select filter for preprocessing [0/1/2/3]:
    [0]: Do not apply filter;
    [1]: Butterworth Lowpass;
    [2]: Butterworth Highpass;
    [3]: Butterworth Bandpass.

    Do you want to detrend the waveforms? [y/n]

    Would you like random input? [y/n]n
    Input waveforms start at: __ seconds before arrival.

It's worth mentioning that there are 2 different formats to generate sample segments:

    #. Random Input: Arrival time will be set on random position of the waveform;
    #. Input waveform start at __ seconds before arrival.

For other questions, you can leave them all blank to use ``default`` parameters, or input the keywords that match your preference. Note that for some questions, you can input multiple keywords (e.g., `SACMAT` or `MAT_MiniSeed`) ::

    # Leave blank if you wish to apply default options
    Do you want to add random noise: [y/[n]] n
    Select export file format: [SAC/MSEED/SEGY/NPZ/MAT] SAC
    Save as single trace or multiple-component seismic data? [y/[n]]
    Do you want to separately save traces as input and output? [y/[n]]
    Do you want to separately save arrival information as a CSV file? [[y]/n]
    Please input a folder name for your dataset (optional):
    Do you want to generate statistical charts after creating the dataset? [[y]/n]

.. tip ::
    As a beginner, feel free to keep default options

Once you are done with the questions, ``QL`` will automatic deploy customized datasets::

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

If you are already an expert in machine learning, you can select the ``Advanced`` mode to fill in all customized options for your search fields::

    QuakeLabeler

Select ``2`` or ``Advanced`` to enter::

    # typing 2 also works
    Advanced

``QL`` will initiate the advanced mode once it receives valid inputs::

    Initializing Advanced Mode...
    Alternative spatial search options are available. Please select your preferred search method:

    Please select one :  [STN/GLOBAL/RECT/CIRC/FE/POLY]
                         [STN]: Stations are restricted to specific station code(s);
                         [GLOBAL]: Stations are not restricted by region (i.e. all available stations);
                         [RECT]: Rectangular search of stations (recommended);
                         [CIRC]: Circular search of stations (recommended);
                         [FE]: Flinn-Engdahl region search of stations;
                         [POLY]: Customized polygon search.

Once you select a specific search method, ``QL`` will run the corresponding functions to collect your search parameters. For instance, let's consider the ``RECT`` option. ``QL`` will request 4 parameters of the rectangular grid search::

    Please enter the South and North coordinates (-90 ~ 90) defining the bottom and top of the rectangular grid, then the West and East coordinates (-180 ~ 180) defining left and right sides of the grid.

    Input rectangular bottom latitude: 31
    Input rectangular top latitude: 46
    Input rectangular left longitude: -128
    Input rectangular right longitude: -114

After the search parameter are collected, ``QL`` will display the input parameters to confirm there is no type-in error::

    The input region is:
    searchshape: RECT
    bot_lat: 31
    top_lat: 46
    left_lon: -128
    right_lon: -114

    Confirm input parameters?  [y/n]
    y

Once the spatial search is completed, you can select a specific time range in a similar way::

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

    Confirm input parameters?  [y/n]
    y

Additional, optional, input parameters can also be specified. For instance, you can select a specific magnitude range or magnitude type. If these parameters are not specified, ``QL`` will use default options::

    Enter event magnitude limits (optional, enter blank space for default sets)
    Input minimum magnitude (0.0-9.0 or blank space for skip this set):

    Input maximum magnitude (0.0-9.0 or blank space for skip this set):

    Enter specific magnitude types. Please note: the selected magnitude type will search for all possible magnitudes in that category:
                       E.g. MB will search for mb, mB, Mb, mb1mx, etc
                       Available input:
                       <Any>|<MB>|<MS>|<MW>|<ML>|<MD> or blank space for skip this set

Following these optional parameters, the options are the same as those in the ``beginner`` mode. Users will go through all questions to define their dataset ::

    How many samples do you wish to create? [1- ] (input MAX for all available waveform):5000
    Do you want fixed sample length? [y/n] (default: y):y
    Enter sample length (how many sample points do you wish in a trace)? (default 5000): 5000
    Select label type: [simple/specific]?
    [simple]: P/S;
    [specific]: P/Pn/Pb/S/Sn, etc.
    specific
    Enter a fixed sampling rate(i.e.: 100.0) or skip for keep original sampling rate:
    Select filter for preprocessing [0/1/2/3]:
    [0]: Do not apply filter;
    [1]: Butterworth Lowpass;
    [2]: Butterworth Highpass;
    [3]: Butterworth Bandpass. 0
    Do you want to detrend the waveforms ? [y/n]n
    Would you like random input? [y/n]y
    Do you want to add random noise: [y/n] n
    Select export file format: [SAC/MSEED/SEGY/NPZ/MAT]SAC
    Save as single trace or multiple-component seismic data? [y/n]y
    Do you want to separately save traces as input and output? [y/n]y
    Do you want to separately save arrival information as a CSV file? [y/n]y
    Please input a folder name for your dataset (optional): NewDataset
    Do you want to generate statistical charts after creating the dataset? [y/n]y

.. note ::

    - Processing time varies based on the volume of the dataset.
    - Only use pre-processing options if necessary.
