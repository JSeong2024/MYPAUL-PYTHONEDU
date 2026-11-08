"""비구형 군집에서 KMeans와 DBSCAN의 차이."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "solutions"))
from advanced_02_density_clustering import load_data, compare_clusters

result = compare_clusters(load_data())
print(f"KMeans ARI: {result['kmeans_ari']:.3f}")
print(f"DBSCAN ARI: {result['dbscan_ari']:.3f}")
print(f"DBSCAN clusters: {result['dbscan_clusters']}")
print(f"DBSCAN noise count: {result['dbscan_noise']}")
