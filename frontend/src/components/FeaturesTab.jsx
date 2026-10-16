import React from 'react';

export default function FeaturesTab({ projectData, onSelectFeatureForExplorer, onGoToDiff }) {
  if (!projectData) return null;

  return (
    <div className="glass-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 700 }}>Stage 1: AI Feature Identification</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            The AI engine grouped the source classes into the following cohesive business features:
          </p>
        </div>
        <button
          className="btn btn-primary"
          onClick={onGoToDiff}
        >
          Inspect Git Changes →
        </button>
      </div>

      <div className="features-grid">
        {projectData.features.map((feat, idx) => (
          <div key={idx} className="feature-card">
            <div>
              <div className="feature-header">
                <h3 className="feature-title">{feat.name}</h3>
                <span className="confidence-pill">{(feat.confidence * 100).toFixed(1)}% Confidence</span>
              </div>
              <p className="feature-desc">{feat.description}</p>
              
              <div style={{ fontSize: '0.78rem', color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: 600 }}>
                Clustered Classes ({feat.classes.length})
              </div>
              <div className="class-tag-list">
                {feat.classes.map((cls, cIdx) => (
                  <span key={cIdx} className="class-tag">{cls.class_name}</span>
                ))}
              </div>
            </div>

            <div style={{ marginTop: '1.5rem', paddingTop: '1rem', borderTop: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between' }}>
              <button
                className="btn btn-secondary"
                style={{ padding: '0.4rem 0.85rem', fontSize: '0.8rem' }}
                onClick={() => onSelectFeatureForExplorer(idx)}
              >
                Get Diagram-as-Code
              </button>
              <span style={{ fontSize: '0.78rem', color: 'var(--accent-emerald)', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                ✓ Ready to Export
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
