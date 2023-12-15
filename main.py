# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import functions as f

def print_hi(name):
    database, names = f.load__csv_files_from_folder("data")
    data0 = f.DataFrameMetadataCreator(database[0])
    columns = data0.get_numerical_columns()
    print(data0.column_type)
    data0.create_column_embeddings()
    embediings = data0.column_embeddings


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
