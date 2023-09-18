# Fusion of multiple normalized Event-Based Surveillance data

This program takes in input a set of normalized Event-Based Surveillance data and produces a single output file by performing an event fusion strategy. This fusion strategy is based on the normalized event entities provided by the EBS platforms. This specific branch of this repository is dedicated to the work conducted by INRAE/CIRAD and LIRMM in Montpellier for the specific end-user needs of [ESA](https://plateforme-esa.fr/fr) in the context of the [MOOD project](https://mood-h2020.eu/). Concretely, ESA aims to perform a more thorough surveillance of avian influenza cases for mammals.

* Nejat Arinik [nejat.arinik@inrae.fr](mailto:nejat.arinik@inrae.fr)
* Julien Rabatel [jrabatel@gmail.com](mailto:jrabatel@gmail.com)
* Mathieu Roche [mathieu.roche@cirad.fr](mailto:mathieu.roche@cirad.fr)


## Description

This set of `Python` scripts/modules is designed for fusing a set of normalized EBS data provided by several EBS platforms. In this context, we define an epidemiological event as the detection of the virus at a specific date and time and in a specific location.  In order to get the normalized events from the raw ones, you can use our dedicated [Github repository](https://github.com/arinik9/epidnews2event/tree/esa). The underlying event matching strategy is partially described in [Arınık'23]. You can also find some introductory slides in `event_similarity.pdf`.


## Data

For reproducibility purpose, we provide some samples from the data collected by PADI-web, ProMED, WAHIS, APHIS and APHA in the `in` folder. Hence, it is possible to run the source code with these samples. Please contact us for the complete datasets.


## Organization

* Folder `in`:

  * Folder `corpus-events`: this folder contains standardized and normalized event datasets from a set of EBS tools.
  
* Folder `out`: contains the files produced by our program.

* Folder `src`: 

  * Folder `event`: this folder contains event-related classes, such as Diseae, Location, Temporality, Host and Hosts. It also contains the implementations for event similarity.
  * Folder `event_matching`: the folder contains the implementations for event matching and event fusion.


## Installation

* Install Python (tested with Python 3.8.12)

* Install Python dependencies using the following command:

  ```
  pip install -r requirements.txt
  ```

* Download this project from Github: https://github.com/arinik9/compebs/tree/esa

* We have already put sample datasets in the `in/corpus-events` folder. For the complete data, please contact us.

* Update the variable `MAIN_FOLDER` in the file `src/users_consts.py` for your main directory absolute path (e.g. `<YOUR_FOLDER>/compebs`).




## How to run ?

* Go to the folder `src`.

* We run the file `main.py` inside the folder `src`. Or, you can configure the `PYTHONPATH` variable, if you do not want to run it from the folder `src`.



## References

* **[Arınık'23]** N. Arınık, R. Interdonato, M. Roche and M. Teisseire, [*An Evaluation Framework for Comparing Epidemic Intelligence Systems*](https://www.doi.org/10.1109/ACCESS.2023.3262462). in IEEE Access, vol. 11, pp. 31880-31901, 2023, doi: 10.1109/ACCESS.2023.3262462.

