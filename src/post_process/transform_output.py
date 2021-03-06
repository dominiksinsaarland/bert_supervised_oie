import tokenization
import numpy as np
import argparse


# seems easy: https://machinelearningmastery.com/beam-search-decoder-natural-language-processing/


# beam search
def beam_search_decoder(data, k):
	sequences = [[list(), 1.0]]
	# walk over each step in sequence
	for row in data:
		all_candidates = list()
		# expand each current candidate
		for i in range(len(sequences)):
			seq, score = sequences[i]
			for j in range(len(row)):
				candidate = [seq + [j], score * -np.log(row[j])]
				all_candidates.append(candidate)
		# order all candidates by score
		ordered = sorted(all_candidates, key=lambda tup:tup[1])
		# select k best
		sequences = ordered[:k]
	return sequences


def get_test_examples(data_file, prediction_file, top_n_beam_search_results, bert_vocab_file, outfile):
	tokenizer =  tokenization.FullTokenizer(vocab_file=bert_vocab_file, do_lower_case=False)

	#lines = self._read_tsv(os.path.join(data_dir, "train.noisy.oie.conll "))
	examples = []
	words = []
	labels = []
	example_counter = 0
	guid = 0
	covered = set()
	# tokenize test set in the same way we tokenized it to label it
	with open(data_file) as infile:
		for i, line in enumerate(infile):
			if i == 0:
				continue
			line = line.strip()
			if not line:
				continue
			line = line.split("\t")
			if line[0] == "0" and words:
				l = ' '.join([label for label in labels if len(label) > 0])
				w = ' '.join([word for word in words if len(word) > 0])
				if w not in covered:
					examples.append((tokenization.convert_to_unicode(w),tokenization.convert_to_unicode(l),example_counter))
					example_counter += 1
				words=[]
				covered.add(w)
				labels = []

			word = line[1]
			label = line[-1]
			words.append(word)
			labels.append(label)
			


	all_labels = []
	all_tokens = []
	all_example_ids = []
	max_seq_length = 128
	label_map = ["A0-B", "A0-I", "A1-B", "A1-I", "A2-B", "A2-I", "A3-B", "A3-I", "A4-B", "A4-I", "A5-B", "A5-I", "O", "P-B", "P-I", "[CLS]", "X"]
	label_map = {i:x for i,x in enumerate(label_map)}

	# truncate and pad sequences to max length (we also predict padding tokens and cannot allow for a missmatch between token indices and prediction indices)
	for (textlist, labellist, example_counter) in examples:
		index = 0
		labels = ["X"]
		tokens = ["X"]
		index_to_label = {}
		for i,(word,label) in enumerate(zip(textlist.split(),labellist.split())):
			token = tokenizer.tokenize(word)
			tokens.extend(token)
			for i,_ in enumerate(token):
				if i==0:
					labels.append(label)
					index_to_label[index] = label
				else:
					labels.append("X")
					index_to_label[index] = "X"
		tokens.append("X")
		labels.append("X")
		if len(labels) >= max_seq_length - 2:
			labels = labels[0:(max_seq_length - 2)]
			tokens = tokens[0:(max_seq_length - 2)]
		elif len(labels) < max_seq_length:
			labels = labels + (["X"] * (max_seq_length - len(labels)))
			tokens = tokens + (["X"] * (max_seq_length - len(tokens)))
		all_labels.extend(labels)
		all_tokens.extend(tokens)
		all_example_ids.extend([example_counter] * len(labels))
	
	print ("first ten examples", all_tokens[:10])
	print ("first ten labels", all_labels[:10])
	print ("num tokens", len(all_tokens))
	print ("num labels", len(all_labels))
	#input("")
	counter = 0
	t = 0
	n = 0


	predicted = []
	prev_id = 0

	# read predictions file
	with open(prediction_file) as preds:
		for i, pred in enumerate(preds):
			if all_labels[counter] != "X":
				pred = pred.strip().split("\t")
				predicted.append((list(map(float, pred)), all_tokens[counter], all_labels[counter],all_example_ids[counter]))
				
			counter += 1

	prev = 0
	ex = []
	seqs = []
	toks = []
	# decode output with beam search decoder
	with open(outfile, "w") as out_file:
		for pred,token,true, ex_id in predicted:
			if ex_id != prev:
				prev += 1
				beam_searched =beam_search_decoder(seqs, int(top_n_beam_search_results))
				seqs=[]
				print (beam_searched)
				for i in beam_searched:
					for l,t in zip(i[0], toks):
						print (t, label_map[l])
						out_file.write(t + "\t" + label_map[l] + "\n")

				toks = []
				
			seqs.append(pred)
			toks.append(token)

			pred = label_map[np.argmax(pred)]
			print ("tok", token, "pred", pred, "true", true)


# python src/post_process/transform_output.py --data_file supervised-oie/data/test.oie.conll --predictions_file supervised_oie_bert_model_dir/test_results.tsv --top_n_beam_search_results 3 --bert_vocab_file cased_L-12_H-768_A-12/vocab.txt --outfile test_results_readable.tsv



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--data_file')
	parser.add_argument('--predictions_file')
	parser.add_argument('--top_n_beam_search_results')
	parser.add_argument('--bert_vocab_file')
	parser.add_argument('--outfile')
	args = parser.parse_args()
	get_test_examples(args.data_file, args.predictions_file, args.top_n_beam_search_results, args.bert_vocab_file, args.outfile)

