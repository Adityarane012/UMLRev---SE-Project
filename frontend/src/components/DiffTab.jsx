import React from 'react';

export default function DiffTab({
  projectData,
  selectedCommit,
  setSelectedCommit,
  loading,
  onAnalyzeDiff,
  diffReport,
  onGoToExplorer
}) {
  if (!projectData) return null;

  return (
    <div className="glass-card">
      <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '0.5rem' }}>
        Stage 2: Git Diff & Change Analysis
      </h2>
      <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
        Select a commit or recent change. The AI engine will pinpoint affected classes and generate diff-highlighted UML diagrams.
      </p>

      {(!projectData.recent_commits || projectData.recent_commits.length === 0) && (
        <div
          style={{
            background: 'rgba(59, 130, 246, 0.1)',
            border: '1px solid rgba(59, 130, 246, 0.35)',
            borderRadius: '10px',
            padding: '1rem 1.25rem',
            marginBottom: '1.5rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.85rem'
          }}
        >
          <span style={{ fontSize: '1.4rem' }}>ℹ️</span>
          <div>
            <div style={{ fontWeight: 600, color: '#93c5fd', fontSize: '0.92rem', marginBottom: '0.2rem' }}>
              Standalone project without commit history
            </div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.84rem', lineHeight: '1.4' }}>
              This codebase was loaded as a standalone directory or ZIP archive without an active Git repository. Baseline architecture analysis will compare changes against the active source snapshot (HEAD).
            </div>
          </div>
        </div>
      )}

      {/* Commit Selector Bar */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '0.75rem',
          background: 'rgba(15, 20, 32, 0.75)',
          padding: '1.25rem',
          borderRadius: '10px',
          marginBottom: '1.5rem',
          border: '1px solid var(--border-subtle)'
        }}
      >
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem', alignItems: 'center' }}>
          <span style={{ fontSize: '0.88rem', color: 'var(--text-muted)' }}>Target Commit:</span>
          <select
            value={selectedCommit}
            onChange={(e) => setSelectedCommit(e.target.value)}
            style={{
              flex: 1,
              background: 'rgba(11, 15, 25, 0.9)',
              color: '#fff',
              border: '1px solid var(--border-subtle)',
              padding: '0.5rem 1rem',
              borderRadius: '8px',
              fontWeight: 500,
              outline: 'none'
            }}
          >
            {projectData.recent_commits && projectData.recent_commits.length > 0 ? (
              projectData.recent_commits.map((c, i) => (
                <option key={i} value={c.hash}>
                  [{c.hash}] {c.message} ({c.author})
                </option>
              ))
            ) : (
              <option value="HEAD">HEAD (Latest repository state)</option>
            )}
          </select>

          <button
            className="btn btn-primary"
            onClick={onAnalyzeDiff}
            disabled={loading}
          >
            {loading ? 'Analyzing...' : 'Analyze Commit Changes'}
          </button>
        </div>
        <div style={{ fontSize: '0.8rem', color: 'var(--text-dim)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span>💡</span>
          <span>
            <strong>Optimal selection:</strong> Choose commits with <code>feat:</code>, <code>fix:</code>, or code changes (e.g., <code>.py</code>, <code>.java</code>) to highlight impacted classes on UML diagrams. Pure docs or asset commits do not touch classes.
          </span>
        </div>
      </div>

      {/* Diff Report Card */}
      {diffReport ? (
        <div
          style={{
            background: 'rgba(18, 24, 40, 0.8)',
            border: '1px solid var(--border-focus)',
            borderRadius: '12px',
            padding: '1.5rem',
            marginTop: '1rem'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--accent-cyan)' }}>
              Feature Affected: {diffReport.feature_name}
            </h3>
            <span className="confidence-pill" style={{ background: 'rgba(6, 182, 212, 0.15)', color: 'var(--accent-cyan)' }}>
              {diffReport.change_type}
            </span>
          </div>
          <p style={{ color: 'var(--text-main)', fontSize: '0.92rem', marginBottom: '1rem' }}>
            {diffReport.description}
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
            <div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-dim)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '0.4rem' }}>
                Impacted Classes
              </div>
              <div className="class-tag-list">
                {diffReport.impacted_classes && diffReport.impacted_classes.length > 0 ? (
                  diffReport.impacted_classes.map((cls, i) => (
                    <span
                      key={i}
                      className="class-tag"
                      style={{
                        background: 'rgba(16, 185, 129, 0.15)',
                        borderColor: 'rgba(16, 185, 129, 0.3)',
                        color: '#6ee7b7'
                      }}
                    >
                      ● {cls}
                    </span>
                  ))
                ) : (
                  <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem', fontStyle: 'italic' }}>
                    None (Documentation, configuration, or media assets only)
                  </span>
                )}
              </div>
            </div>

            <div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-dim)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '0.4rem' }}>
                Changed Files in Commit
              </div>
              <div className="class-tag-list">
                {diffReport.changed_files.map((f, i) => (
                  <span key={i} className="class-tag" style={{ color: '#cbd5e1' }}>
                    {f}
                  </span>
                ))}
              </div>
            </div>
          </div>

          <div style={{ marginTop: '1.5rem', display: 'flex', justifyContent: 'flex-end' }}>
            <button
              className="btn btn-primary"
              onClick={onGoToExplorer}
            >
              View Updated Diagram-as-Code →
            </button>
          </div>
        </div>
      ) : (
        <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
          Click "Analyze Commit Changes" above to isolate the exact feature and classes touched by this commit.
        </div>
      )}
    </div>
  );
}
