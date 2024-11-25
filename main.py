from time import perf_counter

from similarity_runner.src.impl.cli import CLI

t1 = perf_counter()

cli = CLI()
cli.run()

t2 = perf_counter()
print(f"Time taken: {t2 - t1} seconds")

