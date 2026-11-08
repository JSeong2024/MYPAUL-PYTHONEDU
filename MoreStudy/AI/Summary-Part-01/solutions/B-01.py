"""B-01: validate a rectangular feature matrix and binary targets."""
import math
import sys
import numpy as np


def solve(source: str) -> str:
    lines = source.splitlines()
    try:
        n, d = map(int, lines[0].split())
        if not 1 <= n <= 1000 or not 1 <= d <= 20 or len(lines) != n + 1:
            raise ValueError('invalid shape')
        x, y = [], []
        for line in lines[1:]:
            parts = line.split()
            if len(parts) != d + 1 or parts[-1] not in ('0', '1'):
                raise ValueError('invalid row')
            row = [float(part) for part in parts[:-1]]
            if not all(math.isfinite(value) for value in row):
                raise ValueError('not finite')
            x.append(row)
            y.append(int(parts[-1]))
        X=np.asarray(x,dtype=np.float64)
        target=np.asarray(y,dtype=np.int64)
        assert X.shape==(n,d) and target.shape==(n,)
        return (f'SAMPLES {n}\nFEATURES {d}\n'
                f'TARGET_0 {y.count(0)}\nTARGET_1 {y.count(1)}')
    except (ValueError, IndexError, AssertionError, OverflowError):
        return 'INVALID'


if __name__ == '__main__':
    print(solve(sys.stdin.read()))
