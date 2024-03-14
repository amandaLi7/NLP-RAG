######################################################################
# Compare two systems using bootstrap resampling                     #
#  * by Graham Neubig                                                #
#  * minor modifications by Mathias Müller                           #
#                                                                    #
# See, e.g. the following paper for references                       #
#                                                                    #
# Statistical Significance Tests for Machine Translation Evaluation  #
# Philipp Koehn                                                      #
# http://www.aclweb.org/anthology/W04-3250                           #
#                                                                    #
######################################################################

import numpy as np
import regex
import string
from collections import Counter
from typing import Callable

EVAL_TYPE_ACC = "acc"
EVAL_TYPE_BLEU = "bleu"
EVAL_TYPE_BLEU_DETOK = "bleu_detok"
EVAL_TYPE_PEARSON = "pearson"
EVAL_TYPE_EM = 'em'
EVAL_TYPE_F1 = 'f1'
EVAL_TYPE_RECALL = 'recall'

EVAL_TYPES = [EVAL_TYPE_ACC,
              EVAL_TYPE_BLEU,
              EVAL_TYPE_BLEU_DETOK,
              EVAL_TYPE_PEARSON,
              EVAL_TYPE_EM,
              EVAL_TYPE_F1,
              EVAL_TYPE_RECALL]

def normalize_answer(s: str) -> str:
    def remove_articles(text):
        return regex.sub(r"\b(a|an|the)\b", " ", text)

    def white_space_fix(text):
        return " ".join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return "".join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))

def em(prediction, ground_truth, normalize_fn):
    return float(normalize_fn(prediction) == normalize_fn(ground_truth))


def f1_and_recall(prediction, ground_truth, normalize_fn):
    prediction_tokens = normalize_fn(prediction).split()
    ground_truth_tokens = normalize_fn(ground_truth).split()
    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common.values())

    if num_same == 0:
        return 0, 0
    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1, recall

# returns the f1 score and recall score for one question/answer
def f1_recall_score(prediction, ground_truths, normalize_fn: Callable[[str], str] = lambda x: x):
    result = [f1_and_recall(prediction, gt, normalize_fn) for gt in ground_truths]
    unzip = list(zip(*result))
    return max(unzip[0]), max(unzip[1])


def exact_match_score(prediction, ground_truths, normalize_fn: Callable[[str], str] = lambda x: x):
    return max([em(prediction, gt, normalize_fn) for gt in ground_truths])


def total_score(predictions, ground_truths):
    ref = ground_truths
    rag = predictions
    assert(len(rag) == len(ref))

    exact_match_sum = 0.0
    f1_sum = 0.0
    recall_sum = 0.0
    for pred, truth in zip(rag, ref):
        ground_truths = truth.split(';')
        exact_match_sum += exact_match_score(pred, ground_truths, normalize_answer)
        f1, recall = f1_recall_score(pred, ground_truths, normalize_answer)
        f1_sum += f1
        recall_sum += recall

    return exact_match_sum/len(rag), f1_sum/len(rag), recall_sum/len(rag)

def eval_preproc(data, eval_type='acc'):
  ''' Preprocess into the appropriate format for a particular evaluation type '''
  if type(data) == str:
    data = data.strip()
    if eval_type == EVAL_TYPE_BLEU:
      data = data.split()
    elif eval_type == EVAL_TYPE_PEARSON:
      data = float(data)
    elif eval_type == EVAL_TYPE_EM or eval_type == EVAL_TYPE_F1 or eval_type == EVAL_TYPE_RECALL:
      data = normalize_answer(data)
  return data

def eval_measure(gold, sys, eval_type='acc'):
  ''' Evaluation measure
  
  This takes in gold labels and system outputs and evaluates their
  accuracy. It currently supports:
  * Accuracy (acc), percentage of labels that match
  * Pearson's correlation coefficient (pearson)
  * BLEU score (bleu)
  * BLEU_detok, on detokenized references and translations, with internal tokenization

  :param gold: the correct labels
  :param sys: the system outputs
  :param eval_type: The type of evaluation to do (acc, pearson, bleu, bleu_detok)
  '''
  if eval_type == EVAL_TYPE_ACC:
    return sum([1 if g == s else 0 for g, s in zip(gold, sys)]) / float(len(gold))
  elif eval_type == EVAL_TYPE_BLEU:
    import nltk
    gold_wrap = [[x] for x in gold]
    return nltk.translate.bleu_score.corpus_bleu(gold_wrap, sys)
  elif eval_type == EVAL_TYPE_PEARSON:
    return np.corrcoef([gold, sys])[0,1]
  elif eval_type == EVAL_TYPE_BLEU_DETOK:
    import sacrebleu
    # make sure score is 0-based instead of 100-based
    return sacrebleu.corpus_bleu(sys, [gold]).score / 100.
  elif eval_type == EVAL_TYPE_EM:
    em, _, _ = total_score(sys, gold)
    return em
  elif eval_type == EVAL_TYPE_F1:
    _, f1, _ = total_score(sys, gold)
    return f1
  elif eval_type == EVAL_TYPE_RECALL:
    _, _, recall = total_score(sys, gold)
    return recall
  else:
    raise NotImplementedError('Unknown eval type in eval_measure: %s' % eval_type)

def eval_with_paired_bootstrap(gold, sys1, sys2,
                               num_samples=10000, sample_ratio=0.5,
                               eval_type='acc'):
  ''' Evaluate with paired boostrap

  This compares two systems, performing a significance tests with
  paired bootstrap resampling to compare the accuracy of the two systems.
  
  :param gold: The correct labels
  :param sys1: The output of system 1
  :param sys2: The output of system 2
  :param num_samples: The number of bootstrap samples to take
  :param sample_ratio: The ratio of samples to take every time
  :param eval_type: The type of evaluation to do (acc, pearson, bleu, bleu_detok)
  '''
  assert(len(gold) == len(sys1))
  assert(len(gold) == len(sys2))
  
  # Preprocess the data appropriately for they type of eval
  gold = [eval_preproc(x, eval_type) for x in gold]
  sys1 = [eval_preproc(x, eval_type) for x in sys1]
  sys2 = [eval_preproc(x, eval_type) for x in sys2]

  sys1_scores = []
  sys2_scores = []
  wins = [0, 0, 0]
  n = len(gold)
  ids = list(range(n))

  for i in range(num_samples):
    # Subsample the gold and system outputs
    reduced_ids = np.random.choice(ids,int(len(ids)*sample_ratio),replace=True)
    reduced_gold = [gold[i] for i in reduced_ids]
    reduced_sys1 = [sys1[i] for i in reduced_ids]
    reduced_sys2 = [sys2[i] for i in reduced_ids]
    # Calculate accuracy on the reduced sample and save stats
    sys1_score = eval_measure(reduced_gold, reduced_sys1, eval_type=eval_type)
    sys2_score = eval_measure(reduced_gold, reduced_sys2, eval_type=eval_type)
    if sys1_score > sys2_score:
      wins[0] += 1
    elif sys1_score < sys2_score:
      wins[1] += 1
    else:
      wins[2] += 1
    sys1_scores.append(sys1_score)
    sys2_scores.append(sys2_score)

  # Print win stats
  wins = [x/float(num_samples) for x in wins]
  print('Win ratio: sys1=%.3f, sys2=%.3f, tie=%.3f' % (wins[0], wins[1], wins[2]))
  if wins[0] > wins[1]:
    print('(sys1 is superior with p value p=%.3f)\n' % (1-wins[0]))
  elif wins[1] > wins[0]:
    print('(sys2 is superior with p value p=%.3f)\n' % (1-wins[1]))

  # Print system stats
  sys1_scores.sort()
  sys2_scores.sort()
  print('sys1 mean=%.3f, median=%.3f, 95%% confidence interval=[%.3f, %.3f]' %
          (np.mean(sys1_scores), np.median(sys1_scores), sys1_scores[int(num_samples * 0.025)], sys1_scores[int(num_samples * 0.975)]))
  print('sys2 mean=%.3f, median=%.3f, 95%% confidence interval=[%.3f, %.3f]' %
          (np.mean(sys2_scores), np.median(sys2_scores), sys2_scores[int(num_samples * 0.025)], sys2_scores[int(num_samples * 0.975)]))

if __name__ == "__main__":
  # execute only if run as a script
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('gold', help='File of the correct answers')
  parser.add_argument('sys1', help='File of the answers for system 1')
  parser.add_argument('sys2', help='File of the answers for system 2')
  parser.add_argument('--eval_type', help='The evaluation type (acc/pearson/bleu/bleu_detok)', type=str, default='acc', choices=EVAL_TYPES)
  parser.add_argument('--num_samples', help='Number of samples to use', type=int, default=10000)
  args = parser.parse_args()
  
  with open(args.gold, 'r') as f:
    gold = f.readlines() 
  with open(args.sys1, 'r') as f:
    sys1 = f.readlines() 
  with open(args.sys2, 'r') as f:
    sys2 = f.readlines() 
  eval_with_paired_bootstrap(gold, sys1, sys2, eval_type=args.eval_type, num_samples=args.num_samples)
