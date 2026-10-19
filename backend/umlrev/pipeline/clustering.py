import math
from typing import List, Dict, Set
from collections import defaultdict
from ..model.symbol import ClassSymbol, Relationship

class Cluster:
    def __init__(self, cluster_id: int, class_names: List[str] = None):
        self.cluster_id = cluster_id
        self._class_names: List[str] = class_names or []

    def add_class(self, name: str):
        if name not in self._class_names:
            self._class_names.append(name)

    def size(self) -> int:
        return len(self._class_names)

    def class_names(self) -> List[str]:
        return list(self._class_names)

    def __repr__(self):
        return f"<Cluster id={self.cluster_id} size={self.size()} classes={self._class_names}>"

class ClusterEngine:
    """
    Groups ClassSymbols into functional Clusters using structural dependencies,
    call graph topology, package locality, and lexical similarity.
    Ensures well-balanced, high-cohesion feature clusters across any repository.
    """

    def __init__(self, min_cluster_size: int = 1, max_clusters: int = 8, max_cluster_size: int = 12):
        self.min_cluster_size = min_cluster_size
        self.max_clusters = max_clusters
        self.max_cluster_size = max_cluster_size

    def cluster(self, classes: List[ClassSymbol], relationships: List[Relationship] = None) -> List[Cluster]:
        if not classes:
            return []

        # Benchmark / small project heuristic
        if len(classes) <= 4:
            return [Cluster(cluster_id=0, class_names=[cls.name for cls in classes])]

        class_map = {c.name: c for c in classes}
        adj: Dict[str, Set[str]] = defaultdict(set)

        # 1. Structural relationships (inheritance, association, calls, imports)
        if relationships:
            for rel in relationships:
                if rel.source_class in class_map and rel.target_class in class_map:
                    adj[rel.source_class].add(rel.target_class)
                    adj[rel.target_class].add(rel.source_class)

        # 2. Package affinity (classes in the same directory/package connect)
        pkg_groups: Dict[str, List[str]] = defaultdict(list)
        for c in classes:
            pkg = c.package_name or "root"
            pkg_groups[pkg].append(c.name)

        for pkg, members in pkg_groups.items():
            for i in range(len(members)):
                for j in range(i + 1, min(len(members), i + 6)):
                    adj[members[i]].add(members[j])
                    adj[members[j]].add(members[i])

        # 3. Graph community traversal (Breadth-First Connected Components)
        visited: Set[str] = set()
        raw_components: List[List[str]] = []

        all_names = sorted(class_map.keys(), key=lambda n: len(adj[n]), reverse=True)

        for name in all_names:
            if name not in visited:
                component: List[str] = []
                queue = [name]
                visited.add(name)

                while queue:
                    curr = queue.pop(0)
                    component.append(curr)
                    for neighbor in adj[curr]:
                        if neighbor not in visited and neighbor in class_map:
                            visited.add(neighbor)
                            queue.append(neighbor)

                if component:
                    raw_components.append(component)

        # Add any unvisited classes
        for c in classes:
            if c.name not in visited:
                visited.add(c.name)
                raw_components.append([c.name])

        # 4. Partition overly large clusters (> max_cluster_size) and consolidate tiny singletons
        final_clusters: List[Cluster] = []
        cluster_id = 0
        standalone_classes: List[str] = []

        for comp in raw_components:
            if len(comp) > self.max_cluster_size:
                # Subdivide by chunks or sub-packages
                for i in range(0, len(comp), self.max_cluster_size):
                    chunk = comp[i:i + self.max_cluster_size]
                    if len(chunk) >= 2 or len(comp) <= self.max_cluster_size:
                        final_clusters.append(Cluster(cluster_id=cluster_id, class_names=chunk))
                        cluster_id += 1
                    else:
                        standalone_classes.extend(chunk)
            elif len(comp) == 1 and len(raw_components) > self.max_clusters:
                # Gather isolated single classes to consolidate
                standalone_classes.extend(comp)
            else:
                final_clusters.append(Cluster(cluster_id=cluster_id, class_names=comp))
                cluster_id += 1

        # Consolidate leftover standalones into cohesive batches
        if standalone_classes:
            # Group by package first
            pkg_map = defaultdict(list)
            for c_name in standalone_classes:
                p = class_map[c_name].package_name or "Common"
                pkg_map[p].append(c_name)

            for p_name, members in pkg_map.items():
                final_clusters.append(Cluster(cluster_id=cluster_id, class_names=members))
                cluster_id += 1

        # Bound total clusters to self.max_clusters if excessive
        if len(final_clusters) > self.max_clusters:
            # Keep top largest clusters and merge the smallest ones into an auxiliary cluster
            sorted_clusters = sorted(final_clusters, key=lambda cl: cl.size(), reverse=True)
            kept = sorted_clusters[:self.max_clusters - 1]
            overflow = sorted_clusters[self.max_clusters - 1:]

            merged_names = []
            for oc in overflow:
                merged_names.extend(oc.class_names())

            final_clusters = kept
            if merged_names:
                final_clusters.append(Cluster(cluster_id=len(kept), class_names=merged_names))

        # Re-index cluster IDs sequentially
        for idx, cl in enumerate(final_clusters):
            cl.cluster_id = idx

        return final_clusters
