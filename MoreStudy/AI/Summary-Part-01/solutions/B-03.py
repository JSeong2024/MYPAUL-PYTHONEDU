"""B-03: simultaneous update from a single-sample squared loss."""
import sys


def solve(source: str) -> str:
    x, y, w, b, eta = map(float, source.split())
    if not 0 < eta <= 1:
        raise ValueError('invalid learning rate')
    err = w*x+b-y
    grad_w, grad_b = err*x, err
    new_w, new_b = w-eta*grad_w, b-eta*grad_b
    prediction = new_w*x+new_b
    return (f'GRAD_W {grad_w:.4f}\nGRAD_B {grad_b:.4f}\n'
            f'NEW_W {new_w:.4f}\nNEW_B {new_b:.4f}\nPREDICTION {prediction:.4f}')


if __name__ == '__main__':
    print(solve(sys.stdin.read()))
