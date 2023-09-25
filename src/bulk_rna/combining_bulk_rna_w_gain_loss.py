from itertools import product
from pathlib import Path

import pandas as pd

BULK_RNA_PATH = Path('data/bulk_rna')
GAIN_LOSS_PATH = Path('data/gain_loss')
GENE_DIFFERENCE_PATH = Path('data/gene_difference')


def create_combined_df(ref: str, animal: str, sample_type: str, hour: int):
    bulk_rna_df_path = BULK_RNA_PATH / f'animals/{animal}/edge_r/filtered/significant_logfc/{sample_type}_{hour}_logfc_up.csv'
    if not bulk_rna_df_path.exists():
        return None

    df_animal = pd.read_csv(bulk_rna_df_path, index_col=0)
    df_ref = pd.read_csv(GAIN_LOSS_PATH / f'gene_difference/{ref}/{ref}_reptile_df_plus.csv', index_col=0)

    df_combined = df_ref.merge(df_animal, left_index=True, right_index=True, how='inner')

    values_to_keep = ['Gene Name',
                      'Chrysemys picta bellii',
                      'Crocodylus porosus',
                      'Varanus komodoensis',
                      'logFC',
                      'PValue']
    df_combined = df_combined[values_to_keep]
    df_combined = df_combined.sort_index()
    df_combined.index.name = 'Gene Id'

    return df_combined


def main():
    animals = ['chicken_109',
               'chicken_grcg6a',
               'crocodile',
               'turtle_painted',
               'komodo']
    sample_types = ['pic', 'lps']
    hours = [4, 8, 24]
    refs = ['gallus', 'human', 'lizard', 'komodo']

    for ref, animal, sample_type, hour in product(refs, animals, sample_types, hours):
        df = create_combined_df(ref, animal, sample_type, hour)
        if df is not None and len(df) > 0:
            path = GENE_DIFFERENCE_PATH / f'{ref}/{animal}_{sample_type}_{hour}h_diff_df.csv'
            path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(path)


if __name__ == '__main__':
    main()
