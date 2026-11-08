"""B-04: confusion counts at an inclusive decision threshold."""
import sys


def solve(source: str) -> str:
    lines = source.strip().splitlines()
    n_text, threshold_text = lines[0].split()
    n, threshold = int(n_text), float(threshold_text)
    if len(lines) != n+1 or n < 1 or not 0 <= threshold <= 1:
        raise ValueError('invalid input')
    tp = fp = fn = tn = 0
    for line in lines[1:]:
        actual_text, score_text = line.split()
        actual, score = int(actual_text), float(score_text)
        if actual not in (0, 1) or not 0 <= score <= 1:
            raise ValueError('invalid value')
        pred = int(score >= threshold)
        if actual == 1 and pred == 1: tp += 1
        elif actual == 0 and pred == 1: fp += 1
        elif actual == 1: fn += 1
        else: tn += 1
    precision = tp/(tp+fp) if tp+fp else 0.0
    recall = tp/(tp+fn) if tp+fn else 0.0
    f1 = 2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.0
    return (f'TP {tp}\nFP {fp}\nFN {fn}\nTN {tn}\n'
            f'PRECISION {precision:.4f}\nRECALL {recall:.4f}\nF1 {f1:.4f}')


if __name__ == '__main__':
    print(solve(sys.stdin.read()))
