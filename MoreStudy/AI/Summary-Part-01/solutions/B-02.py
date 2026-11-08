"""B-02: compare linear prediction with a train-only mean baseline."""
import math
import sys


def solve(source: str) -> str:
    lines = source.splitlines()
    try:
        w, b = map(float, lines[0].split())
        k = int(lines[1]); train = list(map(float, lines[2].split()))
        n = int(lines[3]); rows = [list(map(float, line.split())) for line in lines[4:]]
        if not 1 <= k <= 1000 or not 1 <= n <= 1000 or len(train) != k or len(rows) != n or any(len(row) != 2 for row in rows):
            raise ValueError('invalid length')
        if not all(math.isfinite(v) for v in [w, b, *train, *(v for row in rows for v in row)]):
            raise ValueError('invalid value')
        baseline = sum(train) / k
        errors = [w*x + b-y for x, y in rows]
        model_mae = sum(abs(e) for e in errors)/n
        model_mse = sum(e*e for e in errors)/n
        baseline_mae = sum(abs(baseline-y) for _, y in rows)/n
        best = 'MODEL' if model_mae < baseline_mae else 'BASELINE' if model_mae > baseline_mae else 'TIE'
        return f'MODEL_MAE {model_mae:.4f}\nMODEL_MSE {model_mse:.4f}\nBASELINE_MAE {baseline_mae:.4f}\nBEST {best}'
    except (ValueError, IndexError):
        return 'INVALID'


if __name__ == '__main__':
    print(solve(sys.stdin.read()))
