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
        file_df[parent_folder] = file_df[parent_folder].astype('int')  # u welcome honey munch

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
    basepath = Path('data')
    animal_basepaths = basepath.glob('genes/*/')

    for animal_basepath in animal_basepaths:
        animal_name = animal_basepath.stem
        print(animal_name)
        df = generate_animal_genes_df(animal_basepath)
        if df is not None:
            df.to_csv(f'data/{animal_name}.csv')


## saroof alaih bby ##
## at matzhika <3 ##
if __name__ == '__main__':
    main()
