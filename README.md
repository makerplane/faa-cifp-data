[![faa-cifp-data](https://snapcraft.io/faa-cifp-data/badge.svg)](https://snapcraft.io/faa-cifp-data)


## Virtual VFR data for pyefis
This is the code used to build the faa-cifp-data snap that contains the CIFP data published by the FAA. 
The resulting snap includes the `FAACIFP18` file and an `index.bin` that is needed by pyefis Virtual VFR feature.
The `FAACIFP18` file is named `current.db` and the `index.bin` is named `current.bin`.
If published, at the time the snap is built, it will also include the next set of data named `next.db` and `next.bin`
A `metadata.yaml` file is also provided, it contains the expiration date of the `current.db` and if included the `next.db`
pyefis will read the metadata.yaml and load the `current.db` or `next.db` based on the current system date.


## Using the snap
### pyefis
Simply install the pyefis snap from the snapcraft.io store, this snap will be downloaded automatically and connected. You may need to edit your configuration files to update the path to the CIFP data.
Within your screen definition these settings will work when running the pyefis snap:
```
    metadata: /usr/share/makerplane/CIFP/metadata.yaml
```
It is safe to leave the `dbpath` and `indexpath` settings in place, if metadata.yaml exists it will be used, otherwise pyefis will try using `dbpath` and `indexpath`

### Consuming from your custom snap
If you want to include this within your custom snap you will first add a plug to your snapcraft.yaml:
```
plugs:
  faa-cifp-data:
    interface : content
    target: $SNAP/faa-cifp-data
    default-provider: faa-cifp-data
```

From within your snap the data is accessible at the path `$SNAP/faa-cifp-data/CIFP`
If you do not want to use `$SNAP` to reference the the data you can update your layout and add a symbolic link in your snapcraft.yaml:
```
layout:
  /my/custom/path/CIFP:
    symlink: $SNAP/faa-cifp-data/CIFP
```
Makerplane snaps that consume this content will use `/usr/share/makerplane/CIFP` for `/my/custom/path/CIFP`
If we implement other sets of FAA data such as DOF for obsticles, that data could be symlinked as `/usr/share/makerplane/DOF` providing a consistent predictable path for accessing data.


After building and installing your snap you will need to connect it to the faa-cifp-snap:
```
snap connect mynap:faa-cifp-data faa-cifp-data
```
Snaps published by makerplane, such as pyefis, will perform this step automatically.

Now you can access the data from within the snap using `/my/custom/path/CIFP`


