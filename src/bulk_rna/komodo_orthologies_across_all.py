from pathlib import Path

import pandas as pd

BULK_RNA_DATA_DIR = Path('data/bulk_rna')

ONE2ONE_ORTHOLOGY_PATH = BULK_RNA_DATA_DIR / 'orthology/one2one'
ONE2ONE_ACROSS_ALL_PATH = ONE2ONE_ORTHOLOGY_PATH / 'one2one_across_all.csv'

ANIMALS_DATA_PATH = BULK_RNA_DATA_DIR / 'animals'


def get_animal_significant_logfc_path(animal):
    return ANIMALS_DATA_PATH / f'{animal}/edge_r/filtered/significant_logfc'


def generate_animal_orthology_df_by_sample_type(orthology_df: pd.DataFrame, animal: str, sample_type: str):
    base_filepath = get_animal_significant_logfc_path(animal)
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

    logfc_columns = [col for col in res if col.endswith(('_logFC', '_QValue'))]
    res = res.dropna(subset=logfc_columns, how='all')
    return res


def main():
    orthology_df = pd.read_csv(ONE2ONE_ACROSS_ALL_PATH)
    orthology_df = orthology_df.set_index('komodo_stable_id', drop=False)
    orthology_df.index.name = 'ref_komodo_stable_id'

    # the order of the animals is important!
    # it is based on the order of evolution
    animals = ['chicken_grcg6a', 'crocodile', 'turtle_painted', 'komodo']
    sample_types = ['pic', 'lps']

    for sample_type in sample_types:
        animals_orthology_df = pd.DataFrame(index=orthology_df.index)

        for animal in animals:
            animal_df = generate_animal_orthology_df_by_sample_type(orthology_df, animal, sample_type)
            if animal_df.empty:
                continue

            animals_orthology_df = animals_orthology_df.merge(animal_df,
                                                              how='outer',
                                                              left_index=True,
                                                              right_index=True)

        animals_orthology_df_filtered = animals_orthology_df.dropna(how='all')
        animals_orthology_df_filtered.to_csv(
            ONE2ONE_ORTHOLOGY_PATH /
            f'komodo_orthologies_{sample_type}_logfc_qvalue.csv'
        )


if __name__ == '__main__':
    main()
