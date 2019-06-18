# supervised OIE with BERT

Preliminary experiments for supervised open extraction using BERT and a viterbi decoder

# requirements


### Requirements
* Python 3.6
* TensorFlow
* BERT


# installation

* Download and install Anaconda (https://www.anaconda.com/)
* Create a Python Environment and activate it:
```bash 
conda create -n bert_open_oie python=3.6
source activate bert_open_oie
```

* download BERT cased English model
```bash 
wget https://storage.googleapis.com/bert_models/2018_10_18/cased_L-12_H-768_A-12.zip
unzip cased_L-12_H-768_A-12.zip
rm cased_L-12_H-768_A-12.zip
```

* install requirements
```bash 
pip install -r requirments.txt
```

* clone data repo

git clone https://github.com/gabrielStanovsky/supervised-oie.git



* train model

train a model and save in output_dir (here: supervised_oie_bert_model_dir)

```bash 
CUDA_VISIBLE_DEVICES=0 python src/model/run_supervised_oie.py --init_checkpoint=cased_L-12_H-768_A-12/bert_model.ckpt --task_name=oie \
--do_train=true --do_eval=false --do_predict=true --data_dir=supervised-oie/data/ \
--vocab_file=cased_L-12_H-768_A-12/vocab.txt --bert_config_file=cased_L-12_H-768_A-12/bert_config.json \
--output_dir=supervised_oie_bert_model_dir --do_lower_case=false --train_batch_size=32 \
--max_seq_length=128 --learning_rate=5e-5 --num_train_epochs=3
```


