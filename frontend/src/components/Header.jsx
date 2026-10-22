import React from 'react';

export default function Header({
  activeTab,
  setActiveTab,
  hasProjectData,
  projectData,
  backendOnline,
  isApproved,
  diffReport,
  evalResults,
  onOpenEval,
  currentUser,
  onOpenLoginModal
}) {
  // A stage counts as done only when the artefact it produces actually exists,
  // so the stepper reports real progress rather than which tabs were visited.
  const stages = [
    { key: 'ingest', label: 'Ingest', done: Boolean(projectData), locked: false },
    { key: 'features', label: 'Features', done: Boolean(isApproved), locked: !hasProjectData },
    { key: 'diff', label: 'Git Diff', done: Boolean(diffReport), locked: !hasProjectData },
    { key: 'explorer', label: 'Diagrams', done: Boolean(projectData?.diagrams?.length), locked: !hasProjectData },
    { key: 'eval', label: 'Metrics', done: Boolean(evalResults), locked: !hasProjectData }
  ];

  const online = backendOnline !== false;
  const statusLabel =
    backendOnline === null ? 'Contacting backend…' : online ? 'Backend online' : 'Backend unreachable';

  const featureCount = projectData?.features?.length;
  const classCount = projectData?.classes_count;

  return (
    <header className="app-header">
      <div className="brand-section">
        <div className="brand-logo">
          {/* A class box with an inherited child: the thing this tool produces. */}
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="1.9" strokeLinecap="round" strokeLinejoin="round">
            <rect x="8" y="2" width="12" height="7" rx="1.2"></rect>
            <line x1="8" y1="5.5" x2="20" y2="5.5"></line>
            <rect x="3" y="15" width="11" height="7" rx="1.2"></rect>
            <line x1="3" y1="18.5" x2="14" y2="18.5"></line>
            <path d="M14 9v3H8.5v3"></path>
          </svg>
        </div>
        <div style={{ minWidth: 0 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <h1 className="brand-title">UMLRev</h1>
            <span
              title={statusLabel}
              aria-label={statusLabel}
              style={{
                width: '8px',
                height: '8px',
                borderRadius: '50%',
                flexShrink: 0,
                backgroundColor: backendOnline === null ? '#64748b' : online ? '#10b981' : '#ef4444',
                boxShadow: online && backendOnline !== null ? '0 0 0 3px rgba(16, 185, 129, 0.15)' : 'none',
                animation: backendOnline === null ? 'umlrev-pulse-dot 1.4s ease-in-out infinite' : 'none'
              }}
            />
          </div>

          {/* Before a repo is loaded this is a tagline; after, it is the context
              worth reading — which repo, how big, how many features found. */}
          <div className="brand-subtitle">
            {projectData ? (
              <span style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', whiteSpace: 'nowrap' }}>
                <strong style={{ color: '#e2e8f0', fontWeight: 600 }}>{projectData.name}</strong>
                {Number.isFinite(classCount) && (
                  <>
                    <span style={{ color: 'var(--border-subtle)' }}>·</span>
                    <span>{classCount} classes</span>
                  </>
                )}
                {Number.isFinite(featureCount) && (
                  <>
                    <span style={{ color: 'var(--border-subtle)' }}>·</span>
                    <span>{featureCount} features</span>
                  </>
                )}
              </span>
            ) : (
              <span style={{ whiteSpace: 'nowrap' }}>Continuous Reverse Engineering</span>
            )}
          </div>
        </div>
      </div>

      {/* Pipeline stepper */}
      <nav className="stage-nav">
        {stages.map((stage, i) => {
          const current = activeTab === stage.key;
          const cls = ['stage-btn', current ? 'current' : '', stage.done && !current ? 'done' : ''].filter(Boolean).join(' ');
          return (
            <button
              key={stage.key}
              className={cls}
              disabled={stage.locked}
              title={stage.locked ? 'Ingest a repository first' : stage.label}
              onClick={() => {
                setActiveTab(stage.key);
                if (stage.key === 'eval' && onOpenEval) onOpenEval();
              }}
            >
              <span className="stage-num">{stage.done ? '✓' : i + 1}</span>
              <span className="stage-label">{stage.label}</span>
            </button>
          );
        })}
      </nav>

      {/* User Auth Profile (TC-01) */}
      <div
        className="profile-chip"
        onClick={onOpenLoginModal}
        title="Click to view authentication status or login"
      >
        {currentUser?.name || 'Aditya Rane'}
      </div>
    </header>
  );
}
