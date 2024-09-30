import sys

from models.connector_models import ConnectorSettings
from models.user_models import SimilaritySettings, MetadataSettings
import runner as r

if __name__ == "__main__":
    try:
        directory = sys.argv[1]
        run_type = sys.argv[2] # all, metadata, similarity
        settings = SimilaritySettings()
        settings.connector = ConnectorSettings(file_type=("csv", "parquet"), files_paths=[], directory_paths=directory)
        settings.metadata = MetadataSettings(all=True, kinds=True, types=True, embeddings=True)
        settings.run_type = run_type
        r.run(settings)
    except IndexError:
        print("Add path to directory")
