# SatColorLUT
A python script to generate color lookup table for heightmaps based on
earth DEM and true color data.

## License

This project is licensed under the GNU General Public License v3.0.

## Usage

To generate the trivariate (elevation, gradient components) colormaps
use the python script `python3 generate_clut.py`:

``` bash
python3 generate_clut.py
```

To use the colormap on a test heightmap use the python script `python3
generate_clut.py`:

``` bash
python3 apply_clut.py
```

Visit https://worldview.earthdata.nasa.gov to retrieve DEM and true
color data of the earth surface.
