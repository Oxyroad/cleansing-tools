# processing-tools

## Usage

Using tools from `scrape-tools` repo, get `database.db`, `tree_groups.csv`, `stations.csv` and `trees.csv`. Then run:

```sh
./prepare_files.sh
```

After that, you're ready to modify constants in `process.py` and run it. Consider `./process.py > out.json`. This file is quite useful for our frontend (check out `OxyApp` repository).
