import React, { useState } from 'react';

export default function FeaturesTab({
  projectData,
  onSelectFeatureForExplorer,
  onGoToDiff,
  onApproveFeatures,
  isApproved
}) {
  const [editingIdx, setEditingIdx] = useState(null);
  const [editName, setEditName] = useState('');
  const [editDesc, setEditDesc] = useState('');
  const [editClasses, setEditClasses] = useState('');
  const [saveSuccessMsg, setSaveSuccessMsg] = useState('');

  if (!projectData) return null;

  const handleStartEdit = (idx) => {
    const feat = projectData.features[idx];
    setEditingIdx(idx);
    setEditName(feat.name);
    setEditDesc(feat.description || '');
    setEditClasses(feat.classes.map((c) => (typeof c === 'string' ? c : c.class_name)).join(', '));
  };

  const handleSaveEdit = async () => {
    if (editingIdx === null) return;
    const updatedFeatures = projectData.features.map((f, i) => {
      if (i !== editingIdx) {
        return {
          name: f.name,
          description: f.description || '',
          confidence: f.confidence || 0.9,
          classes: f.classes.map((c) => (typeof c === 'string' ? c : c.class_name))
        };
      }
      const parsedClasses = editClasses
        .split(',')
        .map((s) => s.trim())
        .filter(Boolean);
      return {
        name: editName.trim() || f.name,
        description: editDesc.trim(),
        confidence: 1.0,
        classes: parsedClasses.length > 0 ? parsedClasses : f.classes.map((c) => (typeof c === 'string' ? c : c.class_name))
      };
    });

    if (onApproveFeatures) {
      await onApproveFeatures(updatedFeatures);
      setSaveSuccessMsg(`Modified & approved '${editName}' successfully.`);
      setTimeout(() => setSaveSuccessMsg(''), 4000);
    }
    setEditingIdx(null);
  };

  const handleApproveAll = async () => {
    const formatted = projectData.features.map((f) => ({
      name: f.name,
      description: f.description || '',
      confidence: f.confidence || 1.0,
      classes: f.classes.map((c) => (typeof c === 'string' ? c : c.class_name))
    }));
    if (onApproveFeatures) {
      await onApproveFeatures(formatted);
      setSaveSuccessMsg('All candidate features formally approved by developer.');
      setTimeout(() => setSaveSuccessMsg(''), 4000);
    }
  };

  return (
    <div className="glass-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.5rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.35rem' }}>
            <h2 style={{ fontSize: '1.5rem', fontWeight: 700 }}>AI Feature Review & Approval (TC-03)</h2>
            {isApproved && (
              <span
                style={{
                  background: 'rgba(16, 185, 129, 0.15)',
                  border: '1px solid #10b981',
                  color: '#10b981',
                  fontSize: '0.78rem',
                  padding: '0.2rem 0.65rem',
                  borderRadius: '20px',
                  fontWeight: 600
                }}
              >
                ✓ Approved by Developer
              </span>
            )}
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            Review AI-suggested feature clusters, modify naming and class scopes, and approve the architecture before generating UML.
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <button
            type="button"
            className="btn btn-primary"
            onClick={handleApproveAll}
            style={{ padding: '0.55rem 1.25rem', fontSize: '0.85rem' }}
          >
            ✓ Approve Feature List
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={onGoToDiff}
            style={{ padding: '0.55rem 1.25rem', fontSize: '0.85rem' }}
          >
            Inspect Git Changes →
          </button>
        </div>
      </div>

      {saveSuccessMsg && (
        <div style={{ padding: '0.75rem 1rem', background: 'rgba(16, 185, 129, 0.15)', border: '1px solid #10b981', borderRadius: '8px', color: '#10b981', fontSize: '0.88rem', marginBottom: '1.25rem' }}>
          {saveSuccessMsg}
        </div>
      )}

      {/* Edit Feature Modal / Box */}
      {editingIdx !== null && (
        <div style={{ background: 'rgba(15, 23, 42, 0.95)', border: '1px solid var(--border-focus)', borderRadius: '12px', padding: '1.5rem', marginBottom: '1.75rem' }}>
          <h3 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '1rem', color: '#60a5fa' }}>
            Modify Feature Suggestion #{editingIdx + 1}
          </h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '1rem', maxWidth: '700px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-dim)', marginBottom: '0.35rem', fontWeight: 600 }}>
                Feature Name
              </label>
              <input
                type="text"
                value={editName}
                onChange={(e) => setEditName(e.target.value)}
                style={{ width: '100%', background: 'rgba(11, 15, 25, 0.9)', border: '1px solid var(--border-subtle)', borderRadius: '6px', padding: '0.6rem 0.85rem', color: '#fff', fontSize: '0.9rem', outline: 'none' }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-dim)', marginBottom: '0.35rem', fontWeight: 600 }}>
                Description
              </label>
              <textarea
                rows={2}
                value={editDesc}
                onChange={(e) => setEditDesc(e.target.value)}
                style={{ width: '100%', background: 'rgba(11, 15, 25, 0.9)', border: '1px solid var(--border-subtle)', borderRadius: '6px', padding: '0.6rem 0.85rem', color: '#fff', fontSize: '0.88rem', outline: 'none', resize: 'vertical' }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-dim)', marginBottom: '0.35rem', fontWeight: 600 }}>
                Clustered Classes (Comma-separated)
              </label>
              <input
                type="text"
                value={editClasses}
                onChange={(e) => setEditClasses(e.target.value)}
                style={{ width: '100%', background: 'rgba(11, 15, 25, 0.9)', border: '1px solid var(--border-subtle)', borderRadius: '6px', padding: '0.6rem 0.85rem', color: '#fff', fontSize: '0.9rem', outline: 'none' }}
              />
            </div>
            <div style={{ display: 'flex', gap: '0.75rem', marginTop: '0.5rem' }}>
              <button
                type="button"
                className="btn btn-primary"
                onClick={handleSaveEdit}
                style={{ padding: '0.45rem 1.15rem', fontSize: '0.85rem' }}
              >
                Save & Retain Edits
              </button>
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => setEditingIdx(null)}
                style={{ padding: '0.45rem 1.15rem', fontSize: '0.85rem' }}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Features Grid */}
      <div className="features-grid">
        {projectData.features.map((feat, idx) => (
          <div key={idx} className="feature-card">
            <div>
              <div className="feature-header">
                <h3 className="feature-title">{feat.name}</h3>
                <span className="confidence-pill">{(feat.confidence * 100).toFixed(1)}% Confidence</span>
              </div>
              <p className="feature-desc">{feat.description}</p>
              
              <div style={{ fontSize: '0.78rem', color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: 600, marginTop: '0.75rem' }}>
                Clustered Classes ({feat.classes.length})
              </div>
              <div className="class-tag-list">
                {feat.classes.map((cls, cIdx) => (
                  <span key={cIdx} className="class-tag">
                    {typeof cls === 'string' ? cls : cls.class_name}
                  </span>
                ))}
              </div>
            </div>

            <div style={{ marginTop: '1.5rem', paddingTop: '1rem', borderTop: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button
                  type="button"
                  className="btn btn-secondary"
                  style={{ padding: '0.35rem 0.75rem', fontSize: '0.78rem' }}
                  onClick={() => handleStartEdit(idx)}
                >
                  ✎ Edit Suggestion
                </button>
                <button
                  type="button"
                  className="btn btn-primary"
                  style={{ padding: '0.35rem 0.75rem', fontSize: '0.78rem' }}
                  onClick={() => onSelectFeatureForExplorer(idx)}
                >
                  View Diagrams →
                </button>
              </div>
              <span style={{ fontSize: '0.78rem', color: 'var(--accent-emerald)', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                ✓ Synthesized
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
