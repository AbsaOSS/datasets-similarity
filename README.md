
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
### Structure
**Datasets** for testing are stored in [**data**](data) and [**data_validation**](data_validation)
Corresponding link, name and eventual description for each dataset is
stored in DatasetDescription.md in belonging folder. 
Both folders contain file DataShow.md with metadata information for each dataset.

**column2Vec** folder contains all files for [column2Vec](#column2Vec) feature.
More about structure of this folder in [here](column2Vec/README.md/#structure),

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
```

## How to contribute
Please see our [**Contribution Guidelines**](CONTRIBUTING.md).
