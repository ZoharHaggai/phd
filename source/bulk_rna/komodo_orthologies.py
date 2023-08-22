from itertools import product
from pathlib import Path

import pandas as pd


def get_animal_logfc_up_genes(animal: str):
    base_filepath = Path(f'data/bulk_rna/animals/{animal}/edge_r/filtered/significant_logfc')
    sample_types = ['pic', 'lps']
    hours = [4, 8, 24]

    res: set[str] = set()
    for sample_type, hour in product(sample_types, hours):
        filepath = base_filepath / f'{sample_type}_{hour}_logfc_up.csv'
        if filepath.exists():
            df = pd.read_csv(filepath, index_col=0)
            res.update(df.index)

    return res


def decode_stable_id(value: str) -> set[str]:
    match value:
        case str() if value.startswith('{') and value.endswith('}'):
            return eval(value)

        case str():
            return {value}

        case _:
            return set()


def main():
    animals = ['komodo', 'chicken_109', 'chicken_grcg6a', 'crocodile', 'turtle_painted']
    orthology_df = pd.read_csv('data/bulk_rna/orthology/komodo_orthologies.csv')
    orthology_df = orthology_df.set_index('komodo_stable_id', drop=False)
    orthology_df.index.name = 'ref_komodo_stable_id'

    filtered_orthology_df = pd.DataFrame(
        index=orthology_df.index,
        columns=[f'{animal}_stable_id' for animal in animals]
    )

    for animal in animals:
        animal_genes = get_animal_logfc_up_genes(animal)
        mask = orthology_df[f'{animal}_stable_id'].apply(
            lambda x: bool(animal_genes.intersection(decode_stable_id(x)))
        )
        filtered_orthology_df[f'{animal}_stable_id'] = orthology_df[f'{animal}_stable_id'][mask]

    filtered_orthology_df = filtered_orthology_df.dropna(how='all')
    filtered_orthology_df.to_csv('data/bulk_rna/orthology/komodo_orthologies_filtered.csv')


if __name__ == '__main__':
    main()
