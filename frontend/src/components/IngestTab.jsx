import React from 'react';

export default function IngestTab({
  githubUrl,
  setGithubUrl,
  loading,
  onIngestGitHub
}) {
  const sampleRepos = [
    { label: 'octocat/Spoon-Knife', url: 'https://github.com/octocat/Spoon-Knife' },
    { label: 'pallets/flask', url: 'https://github.com/pallets/flask' }
  ];

  const handleSelectSample = (repo) => setGithubUrl(repo.url);

  return (
    <div className="glass-card">
      <div style={{ marginBottom: '1.5rem' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '0.35rem' }}>
          Ingest Codebase & Reverse Engineer
        </h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
          Clone and reverse engineer any public GitHub repository.
        </p>
      </div>

      {/* Quick Preset Repositories Banner */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', flexWrap: 'wrap', marginBottom: '1.75rem', padding: '0.75rem 1rem', background: 'rgba(255, 255, 255, 0.03)', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
        <span style={{ fontSize: '0.8rem', color: 'var(--text-dim)', fontWeight: 600 }}>Quick Presets:</span>
        {sampleRepos.map((r, i) => (
          <button
            key={i}
            type="button"
            onClick={() => handleSelectSample(r)}
            style={{
              background: 'rgba(30, 41, 59, 0.8)',
              border: '1px solid var(--border-subtle)',
              borderRadius: '6px',
              padding: '0.25rem 0.65rem',
              color: '#93c5fd',
              fontSize: '0.78rem',
              cursor: 'pointer',
              fontWeight: 500
            }}
          >
            {r.label}
          </button>
        ))}
      </div>

      <div style={{ background: 'rgba(15, 20, 32, 0.85)', border: '1px solid var(--border-focus)', borderRadius: '14px', padding: '1.75rem' }}>
        <h3 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '0.5rem' }}>Clone & Analyze Remote GitHub Repository</h3>
        <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', marginBottom: '1.25rem' }}>
          Clones the latest commits, parses multi-language AST symbols (Java, Python, JS/TS, React, C#, Go, C++), and detects cohesive business features.
        </p>
        <form onSubmit={onIngestGitHub} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', maxWidth: '640px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-dim)', marginBottom: '0.4rem', fontWeight: 600 }}>
              GitHub Repository URL
            </label>
            <input
              type="text"
              placeholder="https://github.com/owner/repository"
              value={githubUrl}
              onChange={(e) => setGithubUrl(e.target.value)}
              style={{
                width: '100%',
                background: 'rgba(11, 15, 25, 0.9)',
                border: '1px solid var(--border-subtle)',
                borderRadius: '8px',
                padding: '0.75rem 1rem',
                color: '#fff',
                fontSize: '0.9rem',
                outline: 'none'
              }}
            />
          </div>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading || !githubUrl.trim()}
            style={{ alignSelf: 'flex-start', padding: '0.65rem 1.5rem' }}
          >
            {loading ? 'Cloning & Analyzing Repository...' : 'Fetch & Reverse Engineer'}
          </button>
        </form>
      </div>
    </div>
  );
}
