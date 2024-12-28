# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

import fileinput
import os.path
from glob import glob

import pandas as pd  # type: ignore


def load_data(input_directory):
    """Loads data from all input dirs"""
    seq = []
    files = glob(f"{input_directory}/**/*.txt", recursive=True)

    with fileinput.input(files=files) as f:
        for line in f:
            seq.append((f.filename(), line))

    return seq


def map_data(seq):
    """Maps the sequence of dir/filename to the correct df"""

    train_data, test_data = [], []

    for k, v in seq:
        target = (
            "neutral"
            if "neutral" in k
            else "negative" if "negative" in k else "positive"
        )
        data = {"phrase": v, "target": target}
        if "train" in k:
            train_data.append(data)
        else:
            test_data.append(data)

    train_dataset = pd.DataFrame(train_data)
    test_dataset = pd.DataFrame(test_data)

    return train_dataset, test_dataset


def _create_ouptput_directory(output_directory):
    if os.path.exists(output_directory):
        for file in glob(f"{output_directory}/*"):
            os.remove(file)
        os.rmdir(output_directory)
    os.makedirs(output_directory)


def _save_output(output_directory, filename, df):
    df.to_csv(f"files/{output_directory}/{filename}.csv")


def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```
    """

    seq = load_data("files/input")
    train, test = map_data(seq)

    _create_ouptput_directory("files/output")
    _save_output("output", "train_dataset", train)
    _save_output("output", "test_dataset", test)

    return 1


pregunta_01()
