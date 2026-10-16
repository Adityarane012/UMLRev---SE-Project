import React from 'react';

export default function Header({ activeTab, setActiveTab, hasProjectData, onOpenEval }) {
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
          <span>2. AI Feature Discovery</span>
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
    </header>
  );
}
