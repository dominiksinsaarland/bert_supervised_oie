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


