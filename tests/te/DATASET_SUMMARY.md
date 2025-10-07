# Telugu Voice Dataset Summary

## Dataset Overview
This dataset contains Telugu voice recordings from the Common Voice project, converted from MP3 to WAV format for training purposes.

## File Statistics
- Total audio files: 119
- Format: WAV (converted from MP3)
- Training samples: 107 (90%)
- Validation samples: 12 (10%)

## Directory Structure
```
tests/te/
├── clips/                 # Original MP3 files (119 files)
├── wav_clips/             # Converted WAV files (119 files)
├── metadata/
│   ├── metadata.csv       # Basic metadata (file names, durations)
│   ├── complete_metadata.csv  # Complete metadata with text content
│   ├── complete_metadata.json # Complete metadata in JSON format
│   ├── train_metadata.csv     # Training set metadata (90% of data)
│   └── val_metadata.csv       # Validation set metadata (10% of data)
├── clip_durations.tsv     # Original clip durations mapping
├── other.tsv              # Audio file to sentence mapping
└── validated_sentences.tsv # Validated sentence texts
```

## Metadata Fields
Each metadata file contains the following information:
- `file_name`: WAV filename
- `original_file`: Original MP3 filename
- `sentence_id`: Numeric ID extracted from filename
- `text`: Telugu text content of the audio
- `duration_ms`: Audio duration in milliseconds

## Sample Data
Here are some examples from the dataset:

1. File: `common_voice_te_43371640.wav`
   Text: "లింగ కృష్ణులందు లేదురా భేదంబు"
   Duration: 3600 ms

2. File: `common_voice_te_42974000.wav`
   Text: "ముందుచూపు లేని మూర్ఖుండు చెడిపోవు"
   Duration: 5688 ms

3. File: `common_voice_te_42973999.wav`
   Text: "బోసు వీరుని క్రాంతి"
   Duration: 4356 ms

## Data Processing
The dataset has been processed to:
1. Convert all MP3 files to WAV format for better compatibility with training tools
2. Extract and associate text content with each audio file
3. Calculate and include duration information for each audio file
4. Split the dataset into training and validation sets (90/10 split)
5. Provide metadata in both CSV and JSON formats for flexibility

## Usage
This dataset is ready for use in text-to-speech (TTS) training systems. The train/validation split allows for proper model evaluation during training.