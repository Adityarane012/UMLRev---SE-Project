import React from 'react';

export default function EvalTab({ evalResults, groundTruth, onRunEvaluation, onGoToExplorer }) {
  const card = {
    background: 'rgba(17, 23, 38, 0.8)',
    padding: '1.25rem 1.5rem',
    borderRadius: '14px',
    border: '1px solid var(--border-subtle)'
  };
  const term = { color: '#c7d2fe', fontWeight: 600 };
  const countBox = (label, value, color) => (
    <div style={{ textAlign: 'center', minWidth: '96px' }}>
      <div style={{ fontSize: '1.6rem', fontWeight: 800, color }}>{value}</div>
      <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)', marginTop: '0.15rem' }}>{label}</div>
    </div>
  );

  return (
    <div className="glass-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.5rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '0.5rem' }}>
            Stage 5: Pipeline Regression Benchmark
          </h2>
          <p style={{ color: 'var(--text-muted)' }}>
            Checks the discovered feature clusters against a known reference mapping, to confirm the
            pipeline still reproduces a result it is expected to reproduce.
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
        <>
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

        {/* Everything needed to read the three numbers above. */}
        <div style={{ marginTop: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>

          <div style={{ ...card, borderColor: '#b45309', background: 'rgba(120, 53, 15, 0.22)' }}>
            <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.5rem', color: '#fcd34d' }}>
              What this score does not show
            </h3>
            <p style={{ fontSize: '0.86rem', color: '#fde68a', lineHeight: 1.65, marginTop: 0, marginBottom: '0.6rem' }}>
              This is a regression check, not a measure of general accuracy. Read the number with three
              things in mind:
            </p>
            <ul style={{ fontSize: '0.84rem', color: '#fde68a', lineHeight: 1.7, margin: 0, paddingLeft: '1.1rem' }}>
              <li>
                The reference project holds one feature and four tightly coupled classes, which leaves
                almost no room for a false positive or a false negative. A perfect score here is close
                to the expected outcome rather than a demanding result.
              </li>
              <li>
                The feature labeller carries a keyword branch that returns the name
                <em> Tell Story</em> for this project's vocabulary, so on this benchmark the name is
                recalled rather than derived. The clustering is genuinely automatic; the label is not.
              </li>
              <li>
                Matching a discovered feature name to a reference one is a lenient substring test, so
                the score is driven far more by the class grouping than by the chosen name.
              </li>
            </ul>
            <p style={{ fontSize: '0.84rem', color: '#fde68a', lineHeight: 1.65, marginBottom: 0, marginTop: '0.6rem' }}>
              Treat a passing score as evidence that extraction and clustering still work end to end.
              Establishing accuracy would need reference mappings for several projects with multiple
              features each.
            </p>
          </div>

          <div style={card}>
            <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.5rem' }}>
              What is being measured
            </h3>
            <p style={{ fontSize: '0.86rem', color: 'var(--text-muted)', lineHeight: 1.65, margin: 0 }}>
              Stages 1–4 let the pipeline decide, without being told, which classes belong together as a
              feature. Stage 5 compares that decision against a reference answer a human already wrote
              down. The unit of comparison is a single <span style={term}>feature → class assignment</span>:
              claiming <em>Hero</em> belongs to <em>Tell Story</em> is one assignment, scored on its own.
              Every assignment the pipeline makes falls into exactly one of three buckets.
            </p>
          </div>

          <div style={{ ...card, display: 'flex', alignItems: 'center', justifyContent: 'space-around', flexWrap: 'wrap', gap: '1rem' }}>
            {countBox('True Positives — correctly assigned', evalResults.true_positives, 'var(--accent-emerald)')}
            {countBox('False Positives — wrongly assigned', evalResults.false_positives, '#f59e0b')}
            {countBox('False Negatives — missed', evalResults.false_negatives, '#ef4444')}
            {countBox('Features in reference', evalResults.ground_truth_features, 'var(--text-muted)')}
            {countBox('Features discovered', evalResults.predicted_features, 'var(--text-muted)')}
          </div>

          <div style={card}>
            <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.5rem' }}>
              How to read each metric
            </h3>
            <ul style={{ fontSize: '0.86rem', color: 'var(--text-muted)', lineHeight: 1.75, margin: 0, paddingLeft: '1.1rem' }}>
              <li>
                <span style={term}>Precision</span> — of everything the pipeline claimed, how much was right.
                It falls when the tool invents assignments, so it is the guard against an over-eager
                clusterer that sweeps unrelated classes into a feature.
              </li>
              <li>
                <span style={term}>Recall</span> — of everything it should have found, how much it did.
                It falls when the tool misses assignments, so it is the guard against a timid clusterer
                that only reports what is obvious.
              </li>
              <li>
                <span style={term}>F-Measure (F1)</span> — the harmonic mean, which stays low unless
                <em> both</em> are high. A tool can trivially score 100% on either one alone: claim almost
                nothing and precision soars; claim everything and recall soars. F1 is the number that
                cannot be gamed that way, which is why it is the headline result.
              </li>
            </ul>
          </div>

          <div style={card}>
            <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.5rem' }}>
              Reference answer used for this score
            </h3>
            <p style={{ fontSize: '0.86rem', color: 'var(--text-muted)', lineHeight: 1.65, marginTop: 0, marginBottom: '0.75rem' }}>
              Taken from the IEEE Access paper, whose own UMLRev required an engineer to annotate these
              features by hand. A score is only meaningful when the analysed repository is the one below.
            </p>
            {groundTruth && Object.entries(groundTruth).map(([featureName, classes]) => (
              <div key={featureName} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '0.4rem' }}>
                <span style={{ ...term, fontSize: '0.85rem' }}>{featureName}</span>
                <span style={{ color: 'var(--text-dim)' }}>→</span>
                {classes.map((c) => (
                  <code
                    key={c}
                    style={{
                      background: 'rgba(30, 41, 59, 0.9)',
                      border: '1px solid var(--border-subtle)',
                      borderRadius: '5px',
                      padding: '0.1rem 0.45rem',
                      fontSize: '0.78rem',
                      color: '#93c5fd'
                    }}
                  >
                    {c}
                  </code>
                ))}
              </div>
            ))}
            <p style={{ fontSize: '0.8rem', color: 'var(--text-dim)', margin: '0.75rem 0 0 0', lineHeight: 1.6 }}>
              Scored against: <span style={term}>{evalResults.repository}</span>. Analysing a different
              repository compares its classes to the mapping above and will legitimately score near zero —
              that reflects a mismatched reference, not a failure of the pipeline.
            </p>
          </div>

        </div>
        </>
      ) : (
        <button className="btn btn-primary" onClick={onRunEvaluation}>
          Run Ground Truth Evaluation
        </button>
      )}
    </div>
  );
}
