# Comparing Epidemic Intelligence Tools

This Github repository is dedicated to our work, which has been published in IEEE Access [Arınık'23].

* Nejat Arinik [nejat.arinik@inrae.fr](mailto:nejat.arinik@inrae.fr)
* Roberto Interdonato [roberto.interdonato@cirad.fr](mailto:roberto.interdonato@cirad.fr)
* Mathieu Roche [mathieu.roche@cirad.fr](mailto:mathieu.roche@cirad.fr)
* Maguelonne Teisseire [maguelonne.teisseire@inrae.fr](mailto:maguelonne.teisseire@inrae.fr)


## Description

This set of `Python`/`R` scripts/modules is designed for comparing a set of EBS tools in terms of three aspects: 1) spatial analysis (how the events are geographically distributed), 2) temporal analysis (how the events are temporally distributed), 3) thematic entity analysis (what thematic entities are extracted from the events and how they are related to spatio-temporal analysis) and 4) news outlet analysis (what news sources play key role in epidemiological information disseminatation). For each aspect, we propose an appropriate visualisation for end-users. In this context, we define an epidemiological event as the detection of the virus at a specific date and time and in a specific location.

Moreover, in this work, the spatial and temporal scales are two important parameters. We propose to visualize the data in one of the two spatial scales: country and region (ADM1) levels
Likewise, we propose to visualize the data in one of the four temporal scales: week, bi-week, month and year.

It is worth emphasizing that each spatial entity is geocoded with [GeoNames](https://www.geonames.org/). To accurately plot the spatial distribution of events, we rely on the GeoNames identifier of these spatial entities, and not their centroid coordinates. For this reason, we manually assigned a GeoNames identifier for each spatial entity at country or region (ADM1) level. These information are found in the `in/map_shapefiles/world/gaul0_asap` and `in/map_shapefiles/world/ne_10m_admin_1_states_provinces` folders.


## Data

We illustrate the usefulness of the proposed methods with an Avian Influenza dataset. This dataset consists of the Avian Influenza events occurred between 2019 and 2021 and collected by the [PADI-Wwb](https://padi-web.cirad.fr) and [ProMED](https://promedmail.org), and [EMPRES-i](https://empres-i.apps.fao.org). Here, we use the EMPRES-i dataset as ground-truth to evaluate the events collected by PADI-web and ProMED. In total, we have $1515$, $338$ and $5229$ events from PADI-web, ProMED and EMPRES-i, respectively. All these events are standardized and normalized. The final dataset can be found on [Dataverse](https://entrepot.recherche.data.gouv.fr/dataset.xhtml?persistentId=doi:10.57745/Y3XROX) (`normalized_events.zip`).


## Organization

* Folder `in`:

  * Folder `events`: this folder contains standardized and normalized event datasets from a set of EBS tools.
  * Folder `map_shapefiles`: this folder contains the shapefiles for the whole world at country and region (ADM1) level.
  * Folder `news_outlets_geography`: this folder contains the details of the news outlets, particularly their spatial locations.
  * Folder `thematic_taxonomy`: this folder contains the taxonomy trees associated to the thematic entities (host and disease information). 

* Folder `in-bahdja`: this folder is supposed to contain input files for evaluating the event matching task. It is used by the file `src/main_eval_event_matching.py`.

  * Folder `events`: this folder contains standardized and normalized event datasets prepared by Bahdja Boudoua. These files can be found on [Dataverse](https://entrepot.recherche.data.gouv.fr/dataset.xhtml?persistentId=doi:10.57745/Y3XROX) (`eval_event_matching.zip`).
  * Folder `thematic_taxonomy`: this folder contains the taxonomy trees associated to the thematic entities (host and disease information). 

* Folder `out`: contains the files produced by our scripts

* Folder `src`: 

  * Folder `event`: this folder contains event-related classes, such as Diseae, Location, Temporality and Host. It also contains the implementations for event similarity.
  * Folder `event_matching`: the folder contains the implementations for event matching.
  * Folder `plot`: this folder contains a single script, which proposes several functions for map plotting.
  * Folder `spatial_analysis`: this folder contains the scripts performing the evaluation of the spatial focus of the events collected by different EBS tools
  * Folder `temporal_analysis`: this folder contains the scripts performing the evaluation of the temporal focus of the events collected by different EBS tools
  * Folder `thematic_analysis`: this folder contains the scripts performing the evaluation of the thematic focus of the events collected by different EBS tools
  * Folder `news_outlet_analysis`: this folder contains the scripts performing the evaluation of online news and press agencies, that we call in short news outlets, involving in the propagation of epidemiological information. The EBS tools rely on these news outlets to collect epidemiological data and it is of importance to analyze them.
  * Folder `hin`: this folder contains a single script, which creates an heterogeneous information network from an event dataset.
  * Folder `stats`: this folder contains the scripts for calculating ranking results and collecting quantitative evaluation results.
  * Folder `preprocessing`: this folder contains the scripts for preprocessing: mainly for geocoding.
  * Folder `eval`: this folder contains the scripts for evaluation tasks.


## Installation

* Install Python (tested with Python 3.8.12)

* Install Python dependencies using the following command:

  ```
  pip install -r requirements.txt
  ```
* Install R (tested with R 4.2.0)

* Install R dependencies using the following command:

  * install.packages("RColorBrewer")
  * install.packages("ComplexHeatmap")
  * install.packages("circlize")

* Download this project from Github: https://github.com/arinik9/compebs

* We have already put sample datasets in the `in/events` folder. For the complete data, you need to retrieve the data from [Dataverse](https://entrepot.recherche.data.gouv.fr/dataset.xhtml?persistentId=doi:10.57745/Y3XROX). Download, unzip the file `normalized_events.zip` and place the folders under `normalized_events/events` into the `in/events` folder.
  


## How to run ?

* Go to the folder `src`.

* We run the file `main.py` inside the folder `src`. Or, you can configure the `PYTHONPATH` variable, if you do not want to run it from the folder `src`.



## References

* **[Arınık'23]** N. Arınık, R. Interdonato, M. Roche and M. Teisseire, [*An Evaluation Framework for Comparing Epidemic Intelligence Systems*](https://www.doi.org/10.1109/ACCESS.2023.3262462). in IEEE Access, vol. 11, pp. 31880-31901, 2023, doi: 10.1109/ACCESS.2023.3262462.

