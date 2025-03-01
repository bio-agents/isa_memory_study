# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from isaagents.isatab import load
from shutil import copytree
from glob import glob
from os.path import join, basename
from tqdm import tqdm
from sys import exit


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from data/raw into
        cleaned data ready to be measured (saved in data/interim).

        Cleaning: We iterate through our raw data MTBLS metadata and run
        ISA-Tab load onmeach to check for loading errors. If the study is not
        loadable, we exclude the study metadata from this analysis.
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
    if len(glob(join(output_filepath, 'MTBLS*'))) > 0:
        logging.info('Output directory {} already contains MTBLS studies. '
                     'Skipping writing to data/interim. If this is not '
                     'expected, do you need to "make clean" first?'.format(
                      output_filepath))
        exit(0)
    for study_dir in tqdm(glob(join(input_filepath, 'MTBLS*'))):
        study_id = basename(study_dir)
        try:
            load(study_dir)
            copytree(study_dir, '{}/{}'.format(output_filepath, study_id))
        except Exception:
            logging.info('Exluding {}'.format(study_dir))


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
