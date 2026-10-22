import React from 'react';

export default function Header({
  activeTab,
  setActiveTab,
  hasProjectData,
  onOpenEval,
  currentUser,
  onOpenLoginModal
}) {
  return (
    <header className="app-header">
      <div className="brand-section">
        <div className="brand-logo">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
            <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
            <polyline points="2 17 12 22 22 17"></polyline>
            <polyline points="2 12 12 17 22 12"></polyline>
          </svg>
        </div>
        <div>
          <h1 className="brand-title">UMLRev</h1>
          <div className="brand-subtitle">
            <span>● Continuous Reverse Engineering & Diagram-as-Code</span>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <nav className="nav-tabs">
        <button
          className={`tab-btn ${activeTab === 'ingest' ? 'active' : ''}`}
          onClick={() => setActiveTab('ingest')}
        >
          <span>1. Ingest Repo</span>
        </button>
        <button
          className={`tab-btn ${activeTab === 'features' ? 'active' : ''}`}
          onClick={() => setActiveTab('features')}
          disabled={!hasProjectData}
        >
          <span>2. Feature Discovery</span>
        </button>
        <button
          className={`tab-btn ${activeTab === 'diff' ? 'active' : ''}`}
          onClick={() => setActiveTab('diff')}
          disabled={!hasProjectData}
        >
          <span>3. Git Diff Analysis</span>
        </button>
        <button
          className={`tab-btn ${activeTab === 'explorer' ? 'active' : ''}`}
          onClick={() => setActiveTab('explorer')}
          disabled={!hasProjectData}
        >
          <span>4. Diagram-as-Code</span>
        </button>
        <button
          className={`tab-btn ${activeTab === 'eval' ? 'active' : ''}`}
          onClick={() => {
            setActiveTab('eval');
            if (onOpenEval) onOpenEval();
          }}
          disabled={!hasProjectData}
        >
          <span>5. Metrics & Eval</span>
        </button>
      </nav>

      {/* User Auth Profile (TC-01) */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginLeft: 'auto' }}>
        <div
          onClick={onOpenLoginModal}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.6rem',
            background: 'rgba(255, 255, 255, 0.05)',
            border: '1px solid var(--border-subtle)',
            borderRadius: '20px',
            padding: '0.35rem 0.85rem',
            cursor: 'pointer',
            transition: 'border-color 0.2s ease'
          }}
          title="Click to view authentication status or login"
        >
          <div
            style={{
              width: '8px',
              height: '8px',
              borderRadius: '50%',
              backgroundColor: currentUser?.token ? '#10b981' : '#f59e0b'
            }}
          />
          <div style={{ display: 'flex', flexDirection: 'column', textAlign: 'left', lineHeight: '1.2' }}>
            <span style={{ fontSize: '0.78rem', fontWeight: 600, color: '#f1f5f9' }}>
              {currentUser?.name || 'Aditya Rane (B129)'}
            </span>
            <span style={{ fontSize: '0.68rem', color: 'var(--text-muted)' }}>
              {currentUser?.role || 'Software Developer'}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
}
