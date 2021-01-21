SFILE="./.data/p225_001.wav"
MODEL="./output/model_out/my_model"
#GIDX="1"
#python test.py -hps ./vctk.json -m ./output/model_out/my_model -s ./.data/p225_001.wav -t 3 -o ./output/generate_voice/my_output.wav -sr 16000
for idx in {1..20}
do 
    python test.py -hps ./vctk.json -m $MODEL -s $SFILE -t $idx -o ./output/generate_voice/my_output_$idx.wav -sr 16000
done