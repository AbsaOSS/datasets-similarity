from dataclasses import dataclass
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

TEST_PREFIX = "out_by_column_"


@dataclass
class Record:
    table1: str
    table2: str
    config: str
    score: float
    time: float

    table_pair = property(lambda self: f"{self.table1}___{self.table2}")


def read_file_stats(file: Path) -> tuple[float, float]:
    with open(file, "r") as f:
        lines = f.readlines()
    _, score = lines[0].split(":")
    _, time = lines[4].split(":")
    time = time.strip()
    time, _ = time.split(" ")
    return float(score), float(time)


def get_files():
    items = []
    for file in sorted(Path("out").iterdir()):
        name = file.name
        name = name.replace(TEST_PREFIX, "")
        config, tables = name.split("_", maxsplit=1)
        table1, table2 = tables.split("___")
        score, time = read_file_stats(file)
        items.append(Record(table1, table2, config, score, time))
    return items


def get_results(items):
    results = {}
    for file in items:
        if file.table_pair not in results:
            results[file.table_pair] = {"configs": [], "scores": [], "times": []}
        results[file.table_pair]["configs"].append(file.config)
        results[file.table_pair]["scores"].append(file.score)
        results[file.table_pair]["times"].append(file.time)
    return results


def plot_graph(data, name):
    # Example data
    configurations = data["configs"]
    scores = data["scores"]
    processing_times = data["times"]

    x = np.arange(len(configurations))
    width = 0.35
    fig, ax = plt.subplots()
    bars1 = ax.bar(x - width / 2, scores, width, label="Score")
    # bars2 = ax.bar(x + width / 2, processing_times, width, label='Processing Time')
    ax.set_xlabel("Configurations")
    ax.set_ylabel("Values")
    ax.set_title(name)
    ax.set_xticks(x)
    ax.set_xticklabels(configurations)
    ax.legend()

    plt.savefig(f"graphs/{name}.png", dpi=300, bbox_inches="tight")


files = get_files()
results = get_results(files)
for name, values in results.items():
    plot_graph(values, name)
