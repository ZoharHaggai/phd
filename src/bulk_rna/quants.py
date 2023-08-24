import re
import pandas as pd
from pathlib import Path


def generate_animal_genes_df(basepath: Path):
    filepaths = basepath.glob('**/*.genes.sf')
    df = None

    for filepath in filepaths:
        parent_folder = filepath.parent.stem
        file_df = pd.read_csv(filepath, delimiter='\t', index_col='Name')
        file_df = file_df.rename(columns={'NumReads': parent_folder})
        file_df[parent_folder] = file_df[parent_folder].astype('int')

        if df is None:
            df = file_df[[parent_folder]]

        else:
            df = df.merge(file_df[[parent_folder]],
                          left_on='Name',
                          right_on='Name')

    if df is not None:
        df.index = df.index.map(lambda v: re.sub(r'\.\d+$', '', v))
    return df


def main():
    basepath = Path('data/bulk_rna/animals')
    # animals = ['chicken_grcg6a', 'chicken_109', 'crocodile', 'turtle_painted', 'komodo']  
    animals = ['chicken_grcg6a']

    for animal in animals:
        animal_basepath = basepath / animal
        animal_genes_dir = animal_basepath / 'genes'
        print(animal)

        df = generate_animal_genes_df(animal_genes_dir)
        if df is not None:
            df.to_csv(animal_basepath / 'quants.csv')


if __name__ == '__main__':
    main()
