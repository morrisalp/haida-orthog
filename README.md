# haida-orthog

## Installation

```
pip install -r requirements.txt
```

## Running

```
streamlit run src/app.py
```

## TODO

* Add unit tests
* Handle Unicode normalization correctly
* Syllable boundaries and doubling in Lachler=>Enrico
* Enrico=>Lachler:
  * Predicting tone
  * ts/ch/j
  * Removing doubling
* Conventions for common morphemes: e.g. hal (Lachler) vs. 'la (Enrico)