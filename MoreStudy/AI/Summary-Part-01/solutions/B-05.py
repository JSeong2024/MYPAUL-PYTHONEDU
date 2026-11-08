"""B-05: one KMeans assignment/update step in 2-D."""
import sys


def solve(source: str) -> str:
    lines = source.strip().splitlines()
    centers = [tuple(map(float, lines[i].split())) for i in (0, 1)]
    n = int(lines[2])
    points = [tuple(map(float, line.split())) for line in lines[3:]]
    if n < 1 or len(points) != n or any(len(p) != 2 for p in centers + points):
        raise ValueError('invalid input')
    assignments, assigned = [], [[], []]
    for x, y in points:
        dist0 = (x-centers[0][0])**2+(y-centers[0][1])**2
        dist1 = (x-centers[1][0])**2+(y-centers[1][1])**2
        label = 0 if dist0 <= dist1 else 1
        assignments.append(label); assigned[label].append((x, y))
    new_centers = [(sum(p[0] for p in group)/len(group), sum(p[1] for p in group)/len(group))
                   if group else centers[i] for i, group in enumerate(assigned)]
    return ('ASSIGNMENTS ' + ' '.join(map(str, assignments)) + '\n' +
            '\n'.join(f'CENTER_{i} {cx:.4f} {cy:.4f}' for i, (cx, cy) in enumerate(new_centers)))


if __name__ == '__main__':
    print(solve(sys.stdin.read()))
