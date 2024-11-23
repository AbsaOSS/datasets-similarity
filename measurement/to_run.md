# IMDB

## 2 exactly the same tables expected result distance 0

```bash
python main.py -c measurement/configs/by_column/config1 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/imdb.csv
```

```bash
python main.py -c measurement/configs/by_column/config2 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/imdb.csv
```

```bash
python main.py -c measurement/configs/by_column/config3 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/imdb.csv
```

```bash
python main.py -c measurement/configs/by_type/config1 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/imdb.csv
```

```bash
python main.py -c measurement/configs/by_type/config2 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/imdb.csv
```

```bash
python main.py -c measurement/configs/by_type/config3 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/imdb.csv
```

## one table and its half expected result distance 0-0.5

```bash
python main.py -c measurement/configs/by_column/config1 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/imdb_halfA.csv
```

```bash
python main.py -c measurement/configs/by_column/config2 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/imdb_halfA.csv
```

```bash
python main.py -c measurement/configs/by_column/config3 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/imdb_halfA.csv
```

```bash
python main.py -c measurement/configs/by_type/config1 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/imdb_halfA.csv
```

```bash
python main.py -c measurement/configs/by_type/config2 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/imdb_halfA.csv
```

```bash
python main.py -c measurement/configs/by_type/config3 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/imdb_halfA.csv
```

## two different halfs expected result distance 0-0.5

```bash
python main.py -c measurement/configs/by_column/config1 filesystem --filetypes csv --files_paths measurement/data/imdb_halfB.csv,measurement/data/imdb_halfA.csv
```

```bash
python main.py -c measurement/configs/by_column/config2 filesystem --filetypes csv --files_paths measurement/data/imdb_halfB.csv,measurement/data/imdb_halfA.csv
```

```bash
python main.py -c measurement/configs/by_column/config3 filesystem --filetypes csv --files_paths measurement/data/imdb_halfB.csv,measurement/data/imdb_halfA.csv
```

```bash
python main.py -c measurement/configs/by_type/config1 filesystem --filetypes csv --files_paths measurement/data/imdb_halfB.csv,measurement/data/imdb_halfA.csv
```

```bash
python main.py -c measurement/configs/by_type/config2 filesystem --filetypes csv --files_paths measurement/data/imdb_halfB.csv,measurement/data/imdb_halfA.csv
```

```bash
python main.py -c measurement/configs/by_type/config3 filesystem --filetypes csv --files_paths measurement/data/imdb_halfB.csv,measurement/data/imdb_halfA.csv
```

## original table with diff in 20 rows from 1000 expected result distance 0

```bash
python main.py -c measurement/configs/by_column/config1 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/imdb_diff_rows20.csv
```

```bash
python main.py -c measurement/configs/by_column/config2 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/imdb_diff_rows20.csv
```

```bash
python main.py -c measurement/configs/by_column/config3 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/imdb_diff_rows20.csv
```

```bash
python main.py -c measurement/configs/by_type/config1 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/imdb_diff_rows20.csv
```

```bash
python main.py -c measurement/configs/by_type/config2 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/imdb_diff_rows20.csv
```

```bash
python main.py -c measurement/configs/by_type/config3 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/imdb_diff_rows20.csv
```




## 2 completaly different tables expected result distance 0.7 and higer

```bash
python main.py -c measurement/configs/by_column/config1 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/winequality.csv
```

```bash
python main.py -c measurement/configs/by_column/config2 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/winequality.csv
```

```bash
python main.py -c measurement/configs/by_column/config3 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/winequality.csv
```

```bash
python main.py -c measurement/configs/by_type/config1 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/winequality.csv
```

```bash
python main.py -c measurement/configs/by_type/config2 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/winequality.csv
```

```bash
python main.py -c measurement/configs/by_type/config3 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/winequality.csv
```




## 2 simillar tables expected result distance < 0.5

```bash
python main.py -c measurement/configs/by_column/config1 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/similar_to_imdb_netflix.csv
```

```bash
python main.py -c measurement/configs/by_column/config2 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/similar_to_imdb_netflix.csv
```

```bash
python main.py -c measurement/configs/by_column/config3 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/similar_to_imdb_netflix.csv
```

```bash
python main.py -c measurement/configs/by_type/config1 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/similar_to_imdb_netflix.csv
```

```bash
python main.py -c measurement/configs/by_type/config2 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/similar_to_imdb_netflix.csv
```

```bash
python main.py -c measurement/configs/by_type/config3 filesystem --filetypes csv --files_paths measurement/data/imdb.csv,measurement/data/similar_to_imdb_netflix.csv
```

# Wine

## 2 exactly the same tables expected result distance 0

```bash
python main.py -c measurement/configs/by_column/config1 filesystem --filetypes csv --files_paths measurement/data/winequality.csv,measurement/data/winequality.csv
```

```bash
python main.py -c measurement/configs/by_column/config2 filesystem --filetypes csv --files_paths measurement/data/winequality.csv,measurement/data/winequality.csv
```

```bash
python main.py -c measurement/configs/by_column/config3 filesystem --filetypes csv --files_paths measurement/data/winequality.csv,measurement/data/winequality.csv
```

```bash
python main.py -c measurement/configs/by_type/config1 filesystem --filetypes csv --files_paths measurement/data/winequality.csv,measurement/data/winequality.csv
```

```bash
python main.py -c measurement/configs/by_type/config2 filesystem --filetypes csv --files_paths measurement/data/winequality.csv,measurement/data/winequality.csv
```

```bash
python main.py -c measurement/configs/by_type/config3 filesystem --filetypes csv --files_paths measurement/data/winequality.csv,measurement/data/winequality.csv
```

## one table and its half expected result distance 0-0.5

```bash
python main.py -c measurement/configs/by_column/config1 filesystem --filetypes csv --files_paths measurement/data/winequality.csv,measurement/data/winequality_halfA.csv
```

```bash
python main.py -c measurement/configs/by_column/config2 filesystem --filetypes csv --files_paths measurement/data/winequality.csv,measurement/data/winequality_halfA.csv
```

```bash
python main.py -c measurement/configs/by_column/config3 filesystem --filetypes csv --files_paths measurement/data/winequality.csv,measurement/data/winequality_halfA.csv
```

```bash
python main.py -c measurement/configs/by_type/config1 filesystem --filetypes csv --files_paths measurement/data/winequality.csv,measurement/data/winequality_halfA.csv
```

```bash
python main.py -c measurement/configs/by_type/config2 filesystem --filetypes csv --files_paths measurement/data/winequality.csv,measurement/data/winequality_halfA.csv
```

```bash
python main.py -c measurement/configs/by_type/config3 filesystem --filetypes csv --files_paths measurement/data/winequality.csv,measurement/data/winequality_halfA.csv
```

## two different halfs expected result distance 0-0.5

```bash
python main.py -c measurement/configs/by_column/config1 filesystem --filetypes csv --files_paths measurement/data/winequality_halfA.csv,measurement/data/winequality_halfB.csv
```

```bash
python main.py -c measurement/configs/by_column/config2 filesystem --filetypes csv --files_paths measurement/data/winequality_halfA.csv,measurement/data/winequality_halfB.csv
```

```bash
python main.py -c measurement/configs/by_column/config3 filesystem --filetypes csv --files_paths measurement/data/winequality_halfA.csv,measurement/data/winequality_halfB.csv
```

```bash
python main.py -c measurement/configs/by_type/config1 filesystem --filetypes csv --files_paths measurement/data/winequality_halfA.csv,measurement/data/winequality_halfB.csv
```

```bash
python main.py -c measurement/configs/by_type/config2 filesystem --filetypes csv --files_paths measurement/data/winequality_halfA.csv,measurement/data/winequality_halfB.csv
```

```bash
python main.py -c measurement/configs/by_type/config3 filesystem --filetypes csv --files_paths measurement/data/winequality_halfA.csv,measurement/data/winequality_halfB.csv
```