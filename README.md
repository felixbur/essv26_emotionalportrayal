# essv26_emotionalportrayal

Nkululeko Scripts and results for a paper to be submitted to ESSV 2026

The scripts should be called from above a folder (a parent of)
*experiments/essv26_emotionalportrayal*
or the pathes in all csv and ini files need to be adjusted.


 i did the following steps:

## 1: write data import script
* convert original data to nkululeko format
* expects the original data in a folder called *data* 
run
```
python process_database.py
```
* results in a csv dataframe with 30 samples

## 2: format audio data
* convert all to 16kHz mono channel wav format
```
python -m nkululeko.resample --config experiments/essv26_emotionalportrayal/tag_data/exp.ini
```

## 3: segment data
* do voice activity segmentation on all data
```
python -m nkululeko.segment --config experiments/essv26_emotionalportrayal/tag_data/exp.ini
```
* results in a new dataframe: segmented.csv with 518 samples

## 4: predict text for segments
* because the samples are now chunked, we need new trascriptions.
* I used whisper (through nkululeko)
```
python -m nkululeko.predict --config experiments/essv26_emotionalportrayal/tag_data/exp_segs.ini
```
* with 
```
[PREDICT]
targets = ['text']
```

## 5: train a categorical acoustic emotion model
* we agreed on the target emotion labels ["happy", "angry", "sad", "scared", "neutral"]
* I trained a model based on the German Emodb database and the Italian Emovo database.
```
python -m nkululeko.nkululeko --config experiments/essv26_emotionalportrayal/emomodel/exp.ini
```

## 6: predict acoustic emotions for the segments
* I used the model from step 5 tp predict acoustic expression:
```
python -m nkululeko.demo --config experiments/essv26_emotionalportrayal/emomodel/exp.ini --list experiments/essv26_emotionalportrayal/tag_data/segments.csv --outfile segmented_acoustic-labels.csv
```

## 7: predict linguistic emotions for the segments
* I used the *joeddav/xlm-roberta-large-xnli* model to predict linguistic expressions for the segmented data
```
python -m nkululeko.predict --config experiments/essv26_emotionalportrayal/tag_data/exp_segs.ini
```
* with 
```
[PREDICT]
targets = ['textclassification']
textclassifier.candidates = ["happy", "angry", "sad", "scared", "neutral"]
```
