
<!-- toc -->
- [What is Datasets Similarity?](#what-is-datasets-similarity)
  - [Structure](#structure)
  - [Column2Vec](#column2Vec)
- [How to run](#how-to-run)
- [How to run tests](#how-to-run-tests)
- [How to contribute](#how-to-contribute)
<!-- tocstop -->

## What is Datasets Similarity?
Datasets Similarity is project 
## Structure
- **Source code** is in folder [similarity](similarity).
- **Source code for column2Vec** is in folder [column2Vec](column2Vec).
- **Tests** are in folder [test](test)
- **Data** are stored in folders [**data**](data) and [**data_validation**](data_validation).
- **Main folder** contains: folder .github, files .gitignore, CONTRIBUTING.MD, LICENSE, README.md, requirements.txt and main.py

---
**.github** folder contains github workflows.

**column2Vec** folder contains all files for [column2Vec](#column2Vec) feature.
More about structure of this folder in [here](column2Vec/README.md/#structure).

**Datasets** for testing are stored in [**data**](data) and [**data_validation**](data_validation)
Corresponding link, name and eventual description for each dataset is
stored in DatasetDescription.md in belonging folder ([**data**](data/DatasetDescriptin.md), [**data_validation**](data_validation/DatasetDescription.md)). 
Both folders contain file DataShow.md with metadata information for each dataset.

### Column2Vec
## How to run

## How to run tests
> Tests are in folder [*test*](test). 

For running tests you have to switch to tests folder and then run test by using pytest.
```bash
cd test

pytest types_test.py #test name to run 
```

Or you can run all the test by running this:
```bash
 python -m unittest
 #or
 pytest
```
**Please be aware that some tests in the test_column2Vec 
module may take a long time.**

## How to contribute
Please see our [**Contribution Guidelines**](CONTRIBUTING.md).
