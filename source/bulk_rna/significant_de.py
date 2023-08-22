from itertools import product
from pathlib import Path

import pandas as pd


def generate_logfc_files(animal: str, sample_type: str, hour: int):
    base_filepath = Path(f'data/bulk_rna/animals/{animal}/edge_r/filtered')
    input_filepath = base_filepath / f'output_{sample_type}/{sample_type}_{hour}.csv'
    output_folderpath = base_filepath / 'significant_logfc'

    if not input_filepath.exists():
        print(f'{animal}_{input_filepath.stem} does not exists, skipping')
        return
    print(f'generating {animal}_{input_filepath.stem}')

    df = pd.read_csv(input_filepath, index_col=0)

    pvalue_sig = df[df['PValue'] < 0.05]
    logfc_up = pvalue_sig[pvalue_sig['logFC'] >= 0]
    logfc_down = pvalue_sig[pvalue_sig['logFC'] < 0]

    output_folderpath.mkdir(exist_ok=True)
    logfc_up.to_csv(output_folderpath / f'{sample_type}_{hour}_logfc_up.csv')
    logfc_down.to_csv(output_folderpath / f'{sample_type}_{hour}_logfc_down.csv')


def main():
    animals = ['chicken_109', 'chicken_grcg6a', 'crocodile', 'turtle_painted', 'komodo']
    sample_types = ['pic', 'lps']
    hours = [4, 8, 24]

    for animal, sample_type, hour in product(animals, sample_types, hours):
        generate_logfc_files(animal, sample_type, hour)


if __name__ == '__main__':
    main()
