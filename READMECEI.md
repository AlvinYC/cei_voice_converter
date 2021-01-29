# corpus
VCTK from [https://datashare.is.ed.ac.uk/handle/10283/3443](https://datashare.is.ed.ac.uk/handle/10283/3443) (10.94g)

## flac2wav
original format converted code from https://gist.github.com/danrossi/5fe77e8b36768a6371572b5735a447b2(don't support folder) \
modify to support arbitory folder on /preprocess/flac2wav.py

```
python flace2wav input_flac_folder output_wav_folder
mkdir vctk_mic1
mkdir vtck_mic2
find ./output_wav_folder/ -name '*mic1*' | xargs cp -t ./vctk_mic1
find ./output_wav_folder/ -name '*mic2*' | xargs cp -t ./vctk_mic2
cd vctk_mic1
// sudo apt-get install rename
rename 's/_mic1//' *.wav
cd vctk_mic2
rename 's/_mic2//' *.wav
```

## after flac2wav
if flac2wav output folder is VCTK_0.92_wav, it will be
```
.
├── speaker-info.txt -> ../VCTK_0.92_flac/speaker-info.txt
├── txt -> ../VCTK_0.92_flac/txt/
├── update.txt -> ../VCTK_0.92_flac/update.txt
├── wav48 -> ./wav48_mic1/
├── wav48_mic1
├── wav48_mic2
└── wav48_silence_trimmed
``` 


## VCTK

- English   	 33 // ['p225', 'p226', 'p227', 'p228', 'p229', ...]    // p225_001 Please call Stella.
- Scottish  	 19
- NorthernIrish	  6
- Irish     	  9
- Indian    	  3  // ['p248', 'p251', 'p376'] // p248_001: Please call Stella.
- Welsh     	  1  // ['p253'](375 sentens) // p253_001: Please call Stella.
- Unknown   	  1 // ['p280']](410 sentens)  // p280_001: Please call Stella.
- American  	 22
- Canadian  	  8
- SouthAfrican	  4
- Australian	  2
- NewZealand	  1
- British   	  1 // ['s5'] // s5_001: Please call Stella.


## Preprocess 1

```
mak_dataset_vctk.py ./.data/ ./output/vctk_mic1.h5py 0.9
// output: avctk_mic1.h5py almost 7GB
```

## Preprocess 2
```
make_single_samples.py ./output/vctk_mic1.h5py ./output/vctk_mic1.json 5000000 128 ./preprocess/en_speaker_used.txt
// output: vctk_mic1.json almost 300MB
```

```json
    {
        "speaker": 15,
        "i": "256/195",
        "t": 13
    },
    {
        "speaker": 19,
        "i": "273/271",
        "t": 67
    },
```
