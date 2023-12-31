# Diphone-synthesis
Master's project of speech synthesis using diphones' concatenation wtih Praat.

## Requirements

Make sure parselmouth and textgrids libs are installed.
```
pip install praat-parselmouth
pip install praat-textgrids
```

## Usage

First, clone this repository :
```
git clone https://github.com/valentinefleith/SpeechSynthesis.git
```

Then run the script using the following command :

```
python3 src/main.py wav-files/Logatomes.wav wav-files/Logatomes.TextGrid
open wav-files/synthese.wav
```
