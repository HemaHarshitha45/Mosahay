# Mosahay 

The project aims to aid industrialist who want to set up industry or hire workers of certain skill. It gives visualization of most suitable area by ensuring availiblity of skilled workers locally keeping in mind travel limitations of workers in current COVID19 situation.It uses a simple clustering algorithm for the purpose. Also if an entrepreneur wishes to setup industry around his/her area this tool enables to visualize the apt industry to set up given availiblity for workforce nearby. Currently this is implemented only on Uttar Pradesh state. It would later be expanded for other states along with other functionalities.

### Prerequisites

Conda environment is suggested for running the software.(Using normal python environment you might have issues with certain libraries)
To create environment:

```
conda create -n Mosahay_env python=3.7
```

For more details on visit the [Conda website](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

### Installing

Step up the conda environment as suggested in the prerequisites section. Activate the environment using the command:

```
conda activate Mosahay_env
```

Clone/download zip of the software.

All the dependencies can be found in requirements.txt and can be installed using the following command:

```
pip install -r requirements.txt
```

You are good to go and visualize !!

## Running the application

Navigate to src folder and run the application using the command:

```
bokeh serve --show ReleaseVersion1.0.py
```

## References

* [Bokeh](https://bokeh.org/) - The plotting used
* [Geopandas](https://geopandas.org/) - To work with geospatial data


