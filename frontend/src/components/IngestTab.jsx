import React from 'react';

export default function IngestTab({
  githubUrl,
  setGithubUrl,
  loading,
  onIngestGitHub,
  onLoadBenchmark
}) {
  return (
    <div className="glass-card">
      <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '0.5rem' }}>
        Ingest GitHub Repository or Benchmark
      </h2>
      <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>
        Provide any GitHub repository URL. The system will clone, inspect commit history, extract AST symbols, and synthesize Diagram-as-Code models.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '1.5rem' }}>
        {/* Option A: GitHub Live URL Ingestion */}
        <div
          style={{
            background: 'rgba(15, 20, 32, 0.85)',
            border: '1px solid var(--border-focus)',
            borderRadius: '14px',
            padding: '1.75rem',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between'
          }}
        >
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
              <h3 style={{ fontSize: '1.15rem', fontWeight: 600 }}>GitHub Repository</h3>
            </div>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', marginBottom: '1.25rem' }}>
              Clone a public GitHub repository to extract AST symbols and generate Mermaid and PlantUML diagrams.
            </p>

            <form onSubmit={onIngestGitHub} style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              <input
                type="url"
                placeholder="https://github.com/owner/repository"
                value={githubUrl}
                onChange={(e) => setGithubUrl(e.target.value)}
                style={{
                  background: 'rgba(11, 15, 25, 0.9)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '8px',
                  padding: '0.75rem 1rem',
                  color: '#fff',
                  fontSize: '0.9rem',
                  outline: 'none'
                }}
              />
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading || !githubUrl.trim()}
              >
                {loading ? 'Cloning and Analyzing...' : 'Fetch and Analyze Repository'}
              </button>
            </form>
          </div>
        </div>

        {/* Option B: Benchmark Project */}
        <div
          style={{
            background: 'rgba(15, 20, 32, 0.85)',
            border: '1px solid var(--border-subtle)',
            borderRadius: '14px',
            padding: '1.75rem',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between'
          }}
        >
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
              <h3 style={{ fontSize: '1.15rem', fontWeight: 600 }}>Benchmark Case Study</h3>
            </div>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', marginBottom: '1.25rem' }}>
              Load the IEEE Access paper benchmark (<code>Story</code>, <code>Hero</code>, <code>Enemy</code>, <code>Princess</code>) to test feature detection and diagram output.
            </p>
          </div>
          <button
            className="btn btn-secondary"
            onClick={onLoadBenchmark}
            disabled={loading}
          >
            Load Tell Story Benchmark
          </button>
        </div>
      </div>
    </div>
  );
}
