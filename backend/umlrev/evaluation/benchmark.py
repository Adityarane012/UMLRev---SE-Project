from typing import List, Dict, Any, Set, Tuple
from .ground_truth import GroundTruth
from ..model.feature import Feature

class EvaluationService:
    """
    Evaluates identified features against Ground Truth to calculate
    Precision, Recall, and F1-Score (F-measure).
    """

    def evaluate(self, ground_truth: GroundTruth, predicted_features: List[Feature]) -> Dict[str, Any]:
        gt_pairs: Set[Tuple[str, str]] = set()
        for f_name, c_list in ground_truth.mapping.items():
            for c in c_list:
                gt_pairs.add((f_name.lower().strip(), c.lower().strip()))

        pred_pairs: Set[Tuple[str, str]] = set()
        for feat in predicted_features:
            for c in feat.class_names:
                # Find best matching ground truth feature name by token overlap
                best_match = feat.name.lower().strip()
                for gt_f in ground_truth.get_features():
                    if any(token in gt_f.lower() for token in feat.name.lower().split()):
                        best_match = gt_f.lower().strip()
                        break
                pred_pairs.add((best_match, c.lower().strip()))

        # Calculate True Positives, False Positives, False Negatives
        tp = len(gt_pairs.intersection(pred_pairs))
        fp = len(pred_pairs - gt_pairs)
        fn = len(gt_pairs - pred_pairs)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return {
            "repository": ground_truth.repo_name,
            "ground_truth_features": len(ground_truth.mapping),
            "predicted_features": len(predicted_features),
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4)
        }
