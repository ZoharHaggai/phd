from itertools import product
from pathlib import Path

import pandas as pd

basepath = Path(__file__).parent.parent.parent


def generate_unfiltered_summary(animals: list[str], sample_types: list[str], hours: list[int]):
    columns = [f'{sample_type}_{hour}h'
               for sample_type, hour in product(sample_types, hours)]
    result_df = pd.DataFrame(columns=columns, index=animals)
    result_df.index.name = 'animal'

    for animal, sample_type, hour in product(animals, sample_types, hours):
        filepath = basepath / (f'data/bulk_rna/{animal}/edge_r/unfiltered/output_{sample_type}/'
                               f'{sample_type}_{hour}.csv')
        if filepath.exists():
            df = pd.read_csv(filepath)
            result_df[f'{sample_type}_{hour}h'][animal] = len(df)

    output_path = basepath / f'data/bulk_rna/unfiltered_summary.csv'
    result_df.to_csv(output_path)


def generate_filtered_summary(animals: list[str], sample_types: list[str], hours: list[int]):
    columns = [f'{sample_type}_{hour}h'
               for sample_type, hour in product(sample_types, hours)]
    result_df = pd.DataFrame(columns=columns, index=animals)
    result_df.index.name = 'animal'

    for animal, sample_type, hour in product(animals, sample_types, hours):
        filepath = basepath / (f'data/bulk_rna/{animal}/edge_r/filtered/output_{sample_type}/'
                               f'{sample_type}_{hour}.csv')
        if filepath.exists():
            df = pd.read_csv(filepath)
            result_df[f'{sample_type}_{hour}h'][animal] = len(df)

    output_path = basepath / f'data/bulk_rna/filtered_summary.csv'
    result_df.to_csv(output_path)


def generate_filtered_significant_de_summary(animals: list[str], sample_types: list[str], hours: list[int], logfc_types: list[str]):
    columns = [f'{sample_type}_{hour}h_{sign}'
               for sample_type, hour, sign in product(sample_types, hours, logfc_types)]
    result_df = pd.DataFrame(columns=columns, index=animals)
    result_df.index.name = 'animal'

    for animal, sample_type, hour, logfc_type in product(animals, sample_types, hours, logfc_types):
        filepath = basepath / (f'data/bulk_rna/{animal}/edge_r/filtered/significant_logfc/'
                               f'{sample_type}_{hour}_logfc_{logfc_type}.csv')
        if filepath.exists():
            df = pd.read_csv(filepath)
            result_df[f'{sample_type}_{hour}h_{logfc_type}'][animal] = len(df)

    output_path = basepath / f'data/bulk_rna/filtered_significant_de_summary.csv'
    result_df.to_csv(output_path)


def main():
    animals = ['chicken_109', 'crocodile', 'turtle_painted', 'komodo']
    sample_types = ['pic', 'lps']
    hours = [4, 8, 24]
    logfc_types = ['up', 'down']

    print('generating unfiltered_summary...')
    generate_unfiltered_summary(animals, sample_types, hours)

    print('generating filtered_summary...')
    generate_filtered_summary(animals, sample_types, hours)

    print('generating filtered_significant_de_summary...')
    generate_filtered_significant_de_summary(animals, sample_types, hours, logfc_types)


if __name__ == '__main__':
    main()
