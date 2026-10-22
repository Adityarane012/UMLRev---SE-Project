import React from 'react';

export default function EvalTab({ evalResults, onRunEvaluation, onGoToExplorer }) {
  return (
    <div className="glass-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.5rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '0.5rem' }}>
            Stage 5: Empirical Accuracy & Quality Benchmarks
          </h2>
          <p style={{ color: 'var(--text-muted)' }}>
            Evaluates identified feature clusters against the ground truth documented in the IEEE paper.
          </p>
        </div>
        <button
          className="btn btn-secondary"
          onClick={onGoToExplorer}
          style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.5rem 1rem' }}
        >
          <span>←</span>
          <span>Back to Stage 4: Diagrams</span>
        </button>
      </div>

      {evalResults ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1.5rem' }}>
          <div style={{ background: 'rgba(17, 23, 38, 0.8)', padding: '1.75rem', borderRadius: '14px', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>Precision</div>
            <div style={{ fontSize: '2.5rem', fontWeight: 800, color: 'var(--accent-emerald)' }}>
              {(evalResults.precision * 100).toFixed(1)}%
            </div>
            <div style={{ fontSize: '0.78rem', color: 'var(--text-dim)', marginTop: '0.35rem' }}>
              True Positives / (TP + FP)
            </div>
          </div>

          <div style={{ background: 'rgba(17, 23, 38, 0.8)', padding: '1.75rem', borderRadius: '14px', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>Recall</div>
            <div style={{ fontSize: '2.5rem', fontWeight: 800, color: 'var(--accent-cyan)' }}>
              {(evalResults.recall * 100).toFixed(1)}%
            </div>
            <div style={{ fontSize: '0.78rem', color: 'var(--text-dim)', marginTop: '0.35rem' }}>
              True Positives / (TP + FN)
            </div>
          </div>

          <div style={{ background: 'rgba(17, 23, 38, 0.8)', padding: '1.75rem', borderRadius: '14px', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>F-Measure (F1)</div>
            <div style={{ fontSize: '2.5rem', fontWeight: 800, color: 'var(--accent-indigo)' }}>
              {evalResults.f1_score.toFixed(2)}
            </div>
            <div style={{ fontSize: '0.78rem', color: 'var(--text-dim)', marginTop: '0.35rem' }}>
              Harmonic mean of precision & recall
            </div>
          </div>
        </div>
      ) : (
        <button className="btn btn-primary" onClick={onRunEvaluation}>
          Run Ground Truth Evaluation
        </button>
      )}
    </div>
  );
}
