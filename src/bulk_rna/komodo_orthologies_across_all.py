from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd


def generate_animal_orthology_by_sample_type_df(orthology_df: pd.DataFrame, animal: str, sample_type: str):
    base_filepath = Path(f'data/bulk_rna/animals/{animal}/edge_r/filtered/significant_logfc')
    hours = [4, 8, 24]

    res = orthology_df[[f'{animal}_stable_id',
                        f'{animal}_name']].copy()

    for hour in hours:
        filepath = base_filepath / f'{sample_type}_{hour}_logfc_up.csv'
        if filepath.exists():
            logfc_df = pd.read_csv(filepath, index_col=0)
            mask = logfc_df.index.isin(orthology_df[f'{animal}_stable_id'])

            logfc_df = logfc_df[mask][['logFC', 'QValue']]
            logfc_df = logfc_df.rename(columns={'logFC': f'{animal}_{sample_type}_{hour}_logFC',
                                                'QValue': f'{animal}_{sample_type}_{hour}_QValue'})
            res = res.merge(logfc_df, how='outer', left_on=f'{animal}_stable_id', right_index=True)

    logfc_columns = [col for col in res if col.endswith('_logFC')]
    indices_to_drop = res[res[logfc_columns].isna().all(axis=1)].index
    return res.drop(indices_to_drop)


def main():
    orthology_df = pd.read_csv('data/bulk_rna/orthology/one2one/one2one_across_all.csv')
    orthology_df = orthology_df.set_index('komodo_stable_id', drop=False)
    orthology_df.index.name = 'ref_komodo_stable_id'

    # the order of the animals is important!
    # it is based on the order of evolution
    animals = ['chicken_grcg6a', 'crocodile', 'turtle_painted', 'komodo']
    sample_types = ['pic', 'lps']

    for sample_type in sample_types:
        animals_orthology_df = pd.DataFrame(index=orthology_df.index)

        for animal in animals:
            animal_df = generate_animal_orthology_by_sample_type_df(orthology_df, animal, sample_type)

            if len(animal_df) == 0:
                continue

            diff = animal_df.columns.difference(animals_orthology_df.columns, sort=False)
            animals_orthology_df = animals_orthology_df.merge(
                animal_df[diff],
                how='outer',
                left_index=True,
                right_index=True
            )

        animals_orthology_df_filtered = animals_orthology_df.dropna(how='all')
        animals_orthology_df_filtered.to_csv(f'data/bulk_rna/orthology/one2one/komodo_orthologies_{sample_type}_logfc_qvalue.csv')


if __name__ == '__main__':
    main()
