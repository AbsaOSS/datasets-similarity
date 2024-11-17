# Structure
- folder [comparing_all_tables](comparing_all_tables)
- file [Comparator](Comparator.py)
- file [ComparatorByColumns](ComparatorByColumn.py)
- file [Types](Types.py)
- file [DataframeMetadata](DataFrameMetadata.py)
- file [DataframeMetadataCreator](DataFrameMetadataCreator.py)
## folder comparing_all_tables
This folder contains two files categorical.ipynb and comparing.py.
File comparing.py contains the first version of Comparator.
Comparator compares all the tables together,
so it is constructed by nested loops.
It is very complicated, it has not a good design, and
we do not recommend to use it. 

File `categorical.ipynb` shows usage of `comparing.py`.

## file Comparator.py
File contains Comparator class, ComparatorType classes and DistanceFunction
Comparator is part of the pipeline that is shown below
![img_2.png](similarity_framework/docs/pipeline1.png)
You can see the visualization of the Comparator implementation
in the picture below.
The user sets several specific comparators for comparator
(for example, bool, string and category)
Each comparator will be executed.
Specific comparator creates a number of distance tables for all bool columns. 
Then these tables are merged by counting average for each cell.
That will create one distance table for bool this table will be passed to
Distance function together with a weight and table ratio, and it will count number.
All numbers will be passed to Euclidean distance and the overall distance will be computed.
![img.png](similarity_framework/docs/Comparator.png)

This comparator is used in `main.py`, `test.ipynb` and `test_comparator.py`

### File test.ipynb
The file test.ipynb contains usage example of MetadataCreator class and 
Comparator class. It also shows heatmaps and accuracy scores.


## file ComparatorByColumns
This file contains the second implementation which was described 
in [README.md](../README.md/#approach). The pipeline is in the picture below.
![img_3.png](similarity_framework/docs/pipeline2.png)
You can see the visualization of the ComparatorByColumns implementation
in the picture below.
The user again sets several specific comparators for comparator.
But in this implementation,
we distinguish between two super types: table comparator and column comparator.
Each comparator will be executed. 

**Table comparator** compares information for whole table, for example size of tables.
Table comparators create a list of numbers, each one compare some
property and then add the resulting number to the list.

**Column comparator** compares column properties it could be a bool, string or embeddings comparator.
Each comparator is executed for each tuple of columns (Table1 column1 + Table2 column2).
Each comparator creates a number, these numbers will be merged to resulting number by weighted average.
The resulting number will be added to matrix _all Table1 columns_ **x** _all Table2 columns_.

This matrix will be passed to Distance function and it will count number.
All numbers from table comparator and number from column comparator will 
be passed to Euclidean distance and the overall distance will be computed.

![img.png](similarity_framework/docs/ComparatorByColumn.png)

## File Types.py 
The file Types.py includes a Type class and functions
that can be used to determine the type of each column in a dataset.

## File DataFrameMetadata.py
Contains Metadata Class and CategoricalMetadata class

## File DataFrameMetadataCreator.py
Contains MetadataCreator to create Metadata
## Datasets_Description.ipynb
Write info about data (kind, string, categorical) into data/DataShow.md
## These files will be removed in the future
- functions.ipynb,
- playground.ipynb
- functions.py

