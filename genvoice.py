#! /usr/bin/env nix-shell
#! nix-shell -i python3 -p python3 -p piper-tts -p sox
import csv
from subprocess import run
from subprocess import DEVNULL
from concurrent.futures import ThreadPoolExecutor
from tempfile import NamedTemporaryFile
from os import cpu_count
from os import makedirs
from os.path import join
from os.path import isfile

# File Name: 123456.wav (up to 6 characters plus .wav)
# Sample Rate: 32 kHz (or 16 Khz, 8Khz)
# Bits / Sample: 16 (or 8)
# Tracks: 1, mono
# Compression Codec: PCM
# Note: The maximum number of sound files that EdgeTX can properly display in the sound select dropdown is 799. Therefore, the maximum number of files in this folder should not exceed 799.


def tts(msg: str, output_file: str) -> None:
    # piper is not deterministic, don't create big git changes
    if isfile(filepath):
        return

    print(msg)

    # https://manual.edgetx.org/color-radios/radio-settings/sd-card#sounds
    with NamedTemporaryFile(suffix=".wav") as f:
        tmp = f.name
        f.close()

        run(
            ["piper", "-m", "en_US-amy-medium.onnx", "--output_file", tmp],
            input=msg.encode(),
            check=True,
            stdout=DEVNULL,
            stderr=DEVNULL,
        )
        run(
            ["sox", tmp, "-r", "32000", output_file],
            check=True,
            stdout=DEVNULL,
            stderr=DEVNULL,
        )


pool = ThreadPoolExecutor(max_workers=cpu_count())
# "String ID","Source text","Translation","Context","Path","Filename"

with open("en-US.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        path = join("SOUNDS", "en", row["Path"])
        makedirs(path, exist_ok=True)

        # apparently not true, there are filenames that are longer in the csv
        #if len(row["Filename"]) > 10:
        #    raise ValueError("filename {Filename} must be 6 chars not counting extension or .".format(**row))

        filepath = join(path, row["Filename"])
        pool.submit(tts, row["Translation"] or row["Source text"], filepath)


pool.shutdown(wait=True)
