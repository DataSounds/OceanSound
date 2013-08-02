[![Stories in Ready](https://badge.waffle.io/datasounds/oceansound.png)](http://waffle.io/datasounds/oceansound)

OceanSound
==========

Get the music from oceancolor images, through MODIS satellite

Instalation
-----------
OceanSound requires an **pyhdf** instalation, to deal with HDF4 [(HDF-EOS)](http://hdfeos.org/).
Despite **pyhdf** is a deprecated package it still works, but you have to manualy install it.  
Follow the steps [here](http://pysclint.sourceforge.net/pyhdf/install.html)!

And finally to listen your data you can install OceanSound with pip.

```bash
pip install OceanSound
```

Usage
-----
After installation, OceanSound program is enabled on your terminal.
You should pass one of acceptable parameters and generate your music.

```bash
OceanSound --indir dir/where/are/*.hdf --outdir dir/to/save/output.midi
```

Our Project
-----------
OceanSound deals with Satellite MODIS chlorophyll, but if you are interested by extracting music from your data take a 
look at [DataSounds](http://www.datasounds.org) and access the [code](https://github.com/DataSounds/DataSounds)!
