import React from 'react';

export default function DiagramExplorer({
  projectData,
  selectedFeatureIdx,
  setSelectedFeatureIdx,
  selectedDiagramKind,
  setSelectedDiagramKind,
  codeTab,
  setCodeTab,
  zoomLevel,
  setZoomLevel,
  diagramRef,
  currentDiag,
  diagramStatus,
  onCopy,
  onGoToDiff,
  onGoToEval
}) {
  if (!projectData) return null;

  const handleDownload = (content, ext) => {
    if (!content) return;
    const currentFeature = projectData.features[selectedFeatureIdx];
    const featSlug = (currentFeature?.name || 'diagram').toLowerCase().replace(/[^a-z0-9_]/g, '_');
    const filename = `${featSlug}_${selectedDiagramKind.toLowerCase()}.${ext}`;
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="glass-card" style={{ padding: '1.5rem' }}>
      {/* Top Toolbar */}
      <div
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'space-between',
          alignItems: 'center',
          gap: '1rem',
          marginBottom: '1.5rem',
          paddingBottom: '1rem',
          borderBottom: '1px solid var(--border-subtle)'
        }}
      >
        {/* Feature Selector */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Feature Scope:</span>
          <select
            value={selectedFeatureIdx}
            onChange={(e) => setSelectedFeatureIdx(Number(e.target.value))}
            style={{
              background: 'rgba(17, 23, 38, 0.9)',
              color: 'white',
              border: '1px solid var(--border-subtle)',
              padding: '0.5rem 1rem',
              borderRadius: '8px',
              fontWeight: 600,
              outline: 'none',
              cursor: 'pointer'
            }}
          >
            {projectData.features.map((f, i) => (
              <option key={i} value={i}>
                {f.name} ({f.classes.length} classes)
              </option>
            ))}
          </select>
        </div>

        {/* Diagram Kind Toggle */}
        <div style={{ display: 'flex', background: 'rgba(11, 15, 25, 0.8)', padding: '0.25rem', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
          <button
            type="button"
            className={`tab-btn ${selectedDiagramKind === 'CLASS' ? 'active' : ''}`}
            onClick={() => setSelectedDiagramKind('CLASS')}
            style={{ padding: '0.4rem 1rem', fontSize: '0.82rem' }}
          >
            Class Diagram
          </button>
          <button
            type="button"
            className={`tab-btn ${selectedDiagramKind === 'SEQUENCE' ? 'active' : ''}`}
            onClick={() => setSelectedDiagramKind('SEQUENCE')}
            style={{ padding: '0.4rem 1rem', fontSize: '0.82rem' }}
          >
            Sequence Diagram
          </button>
        </div>

        {/* Code / Visual View Mode */}
        <div style={{ display: 'flex', background: 'rgba(11, 15, 25, 0.8)', padding: '0.25rem', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
          <button
            type="button"
            className={`tab-btn ${codeTab === 'visual' ? 'active' : ''}`}
            onClick={() => setCodeTab('visual')}
            style={{ padding: '0.4rem 0.85rem', fontSize: '0.82rem' }}
          >
            Visual Canvas
          </button>
          <button
            type="button"
            className={`tab-btn ${codeTab === 'mermaid' ? 'active' : ''}`}
            onClick={() => setCodeTab('mermaid')}
            style={{ padding: '0.4rem 0.85rem', fontSize: '0.82rem' }}
          >
            Mermaid Code
          </button>
          <button
            type="button"
            className={`tab-btn ${codeTab === 'plantuml' ? 'active' : ''}`}
            onClick={() => setCodeTab('plantuml')}
            style={{ padding: '0.4rem 0.85rem', fontSize: '0.82rem' }}
          >
            PlantUML Code
          </button>
        </div>

        {/* Syntax verdict for the generated Diagram-as-Code */}
        {diagramStatus && (
          <div
            title={diagramStatus.message}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              padding: '0.35rem 0.7rem',
              borderRadius: '20px',
              fontSize: '0.74rem',
              fontWeight: 600,
              whiteSpace: 'nowrap',
              color: diagramStatus.ok ? '#6ee7b7' : '#fca5a5',
              background: diagramStatus.ok ? 'rgba(6, 78, 59, 0.45)' : 'rgba(127, 29, 29, 0.45)',
              border: `1px solid ${diagramStatus.ok ? '#10b981' : '#ef4444'}`
            }}
          >
            <span>{diagramStatus.ok ? '✓' : '✕'}</span>
            <span>
              {diagramStatus.failed
                ? 'Mermaid parse failed'
                : diagramStatus.ok
                ? `Syntax verified · ${diagramStatus.mermaidLines} mmd / ${diagramStatus.pumlLines} puml lines`
                : 'PlantUML looks unbalanced'}
            </span>
          </div>
        )}

        {/* Action Buttons: Copy & Export */}
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          <button
            type="button"
            className="btn btn-secondary"
            style={{ padding: '0.45rem 0.85rem', fontSize: '0.8rem' }}
            onClick={() => {
              if (currentDiag) onCopy(currentDiag.svg_content, 'Mermaid');
            }}
          >
            Copy Mermaid
          </button>
          <button
            type="button"
            className="btn btn-primary"
            style={{ padding: '0.45rem 0.85rem', fontSize: '0.8rem' }}
            onClick={() => {
              if (currentDiag) onCopy(currentDiag.uml_text, 'PlantUML');
            }}
          >
            Copy PlantUML
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            style={{ padding: '0.45rem 0.85rem', fontSize: '0.8rem' }}
            onClick={() => currentDiag && handleDownload(currentDiag.uml_text, 'puml')}
            title="Download PlantUML source file"
          >
            ↓ .puml
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            style={{ padding: '0.45rem 0.85rem', fontSize: '0.8rem' }}
            onClick={() => currentDiag && handleDownload(currentDiag.svg_content, 'mmd')}
            title="Download Mermaid source file"
          >
            ↓ .mmd
          </button>
        </div>
      </div>

      {/* Stage Canvas */}
      <div className="diagram-stage" style={{ transform: `scale(${zoomLevel})`, transformOrigin: 'top center', transition: 'transform 0.2s ease' }}>
        <div className="diagram-controls">
          <button type="button" className="ctrl-btn" onClick={() => setZoomLevel((z) => Math.min(z + 0.15, 2.0))}>+</button>
          <button type="button" className="ctrl-btn" onClick={() => setZoomLevel((z) => Math.max(z - 0.15, 0.6))}>-</button>
          <button type="button" className="ctrl-btn" onClick={() => setZoomLevel(1)}>Reset</button>
        </div>

        {codeTab === 'visual' && (
          <div ref={diagramRef} style={{ width: '100%', display: 'flex', justifyContent: 'center' }}></div>
        )}

        {codeTab === 'mermaid' && (
          <div style={{ width: '100%' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem', color: 'var(--text-muted)', fontSize: '0.82rem' }}>
              <span>Mermaid markup:</span>
              <button
                type="button"
                className="btn btn-secondary"
                style={{ padding: '0.2rem 0.6rem', fontSize: '0.75rem' }}
                onClick={() => currentDiag && onCopy(currentDiag.svg_content, 'Mermaid')}
              >
                Copy All
              </button>
            </div>
            <pre
              style={{
                background: '#0a0d14',
                padding: '1.25rem',
                borderRadius: '10px',
                color: '#6ee7b7',
                fontSize: '0.88rem',
                lineHeight: '1.6',
                overflow: 'auto',
                border: '1px solid rgba(255,255,255,0.08)'
              }}
            >
              {currentDiag?.svg_content}
            </pre>
          </div>
        )}

        {codeTab === 'plantuml' && (
          <div style={{ width: '100%' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem', color: 'var(--text-muted)', fontSize: '0.82rem' }}>
              <span>PlantUML markup:</span>
              <button
                type="button"
                className="btn btn-secondary"
                style={{ padding: '0.2rem 0.6rem', fontSize: '0.75rem' }}
                onClick={() => currentDiag && onCopy(currentDiag.uml_text, 'PlantUML')}
              >
                Copy All
              </button>
            </div>
            <pre
              style={{
                background: '#0a0d14',
                padding: '1.25rem',
                borderRadius: '10px',
                color: '#93c5fd',
                fontSize: '0.88rem',
                lineHeight: '1.6',
                overflow: 'auto',
                border: '1px solid rgba(255,255,255,0.08)'
              }}
            >
              {currentDiag?.uml_text}
            </pre>
          </div>
        )}
      </div>

      {/* Bottom Navigation Bar */}
      <div
        style={{
          marginTop: '1.5rem',
          paddingTop: '1.25rem',
          borderTop: '1px solid var(--border-subtle)',
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'space-between',
          alignItems: 'center',
          gap: '1rem'
        }}
      >
        <button
          type="button"
          className="btn btn-secondary"
          onClick={onGoToDiff}
          style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.6rem 1.25rem' }}
        >
          <span>←</span>
          <span>Back to Stage 3: Git Diff</span>
        </button>

        <button
          type="button"
          className="btn btn-primary"
          onClick={onGoToEval}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            padding: '0.65rem 1.35rem',
            fontSize: '0.92rem',
            fontWeight: 600,
            background: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)',
            boxShadow: '0 4px 14px rgba(99, 102, 241, 0.35)'
          }}
        >
          <span>Proceed to Stage 5: Metrics & Eval</span>
          <span>→</span>
        </button>
      </div>
    </div>
  );
}
