import string
from collections import Counter
from typing import Callable, Tuple
import numpy as np
import regex


# Normalization and score functions from SQuAD evaluation script https://worksheets.codalab.org/rest/bundles/0x6b567e1cf2e041ec80d7098f031c5c9e/contents/blob/
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



# returns exact match probability over all answers, f1 score average, and recall score average over all Q/A pairs
def total_score(predictions_file, ground_truths_file):
    reference_answers = open(ground_truths_file, 'r')
    ref = reference_answers.readlines()

    rag_answers = open(predictions_file, 'r')
    rag = rag_answers.readlines()
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


def total_score_csv(predictions, ground_truths):
    assert(len(predictions) == len(ground_truths))
    exact_match_sum = 0.0
    f1_sum = 0.0
    recall_sum = 0.0
    for pred, truth_list in zip(predictions, ground_truths):
        ground_truths = str(truth_list).split(';')
        exact_match_sum += exact_match_score(pred, ground_truths, normalize_answer)
        f1, recall = f1_recall_score(pred, ground_truths, normalize_answer)
        f1_sum += f1
        recall_sum += recall
    return exact_match_sum / len(predictions), f1_sum / len(predictions), recall_sum / len(predictions)