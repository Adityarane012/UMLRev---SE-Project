import React, { useState } from 'react';

export default function IngestTab({
  githubUrl,
  setGithubUrl,
  loading,
  onIngestGitHub,
  onLoadBenchmark,
  onAnalyzeLocal,
  onUploadZip
}) {
  const [ingestMode, setIngestMode] = useState('github'); // 'github', 'local', 'zip', 'benchmark'
  const [localPath, setLocalPath] = useState('examples/tell_story');
  const [projectName, setProjectName] = useState('My Local Project');
  const [zipFile, setZipFile] = useState(null);
  const [zipName, setZipName] = useState('Uploaded Codebase');

  const sampleRepos = [
    { label: 'octocat/Spoon-Knife', url: 'https://github.com/octocat/Spoon-Knife' },
    { label: 'pallets/flask', url: 'https://github.com/pallets/flask' },
    { label: 'UMLRev Backend (Self)', url: 'local:backend' }
  ];

  const handleSelectSample = (repo) => {
    if (repo.url.startsWith('local:')) {
      setIngestMode('local');
      setLocalPath('backend');
      setProjectName('UMLRev Backend Core');
    } else {
      setIngestMode('github');
      setGithubUrl(repo.url);
    }
  };

  const handleLocalSubmit = (e) => {
    e.preventDefault();
    if (!localPath.trim()) return;
    if (onAnalyzeLocal) {
      onAnalyzeLocal(projectName.trim() || 'Local Project', localPath.trim());
    }
  };

  const handleZipSubmit = (e) => {
    e.preventDefault();
    if (!zipFile) return;
    if (onUploadZip) {
      onUploadZip(zipFile, zipName.trim() || 'Uploaded Project');
    }
  };

  return (
    <div className="glass-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.5rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '0.35rem' }}>
            Ingest Codebase & Reverse Engineer
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            Supports any public GitHub repository, local directories, ZIP archives, or standard benchmarks.
          </p>
        </div>

        {/* Ingest Mode Selector */}
        <div style={{ display: 'flex', background: 'rgba(11, 15, 25, 0.8)', padding: '0.25rem', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
          <button
            type="button"
            className={`tab-btn ${ingestMode === 'github' ? 'active' : ''}`}
            onClick={() => setIngestMode('github')}
            style={{ padding: '0.45rem 0.9rem', fontSize: '0.82rem' }}
          >
            GitHub Repo
          </button>
          <button
            type="button"
            className={`tab-btn ${ingestMode === 'local' ? 'active' : ''}`}
            onClick={() => setIngestMode('local')}
            style={{ padding: '0.45rem 0.9rem', fontSize: '0.82rem' }}
          >
            Local Path
          </button>
          <button
            type="button"
            className={`tab-btn ${ingestMode === 'zip' ? 'active' : ''}`}
            onClick={() => setIngestMode('zip')}
            style={{ padding: '0.45rem 0.9rem', fontSize: '0.82rem' }}
          >
            Upload ZIP
          </button>
          <button
            type="button"
            className={`tab-btn ${ingestMode === 'benchmark' ? 'active' : ''}`}
            onClick={() => setIngestMode('benchmark')}
            style={{ padding: '0.45rem 0.9rem', fontSize: '0.82rem' }}
          >
            Benchmark
          </button>
        </div>
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

      {/* Mode 1: GitHub URL Ingestion */}
      {ingestMode === 'github' && (
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
      )}

      {/* Mode 2: Local Directory Path Ingestion */}
      {ingestMode === 'local' && (
        <div style={{ background: 'rgba(15, 20, 32, 0.85)', border: '1px solid var(--border-focus)', borderRadius: '14px', padding: '1.75rem' }}>
          <h3 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '0.5rem' }}>Analyze Local Project Directory</h3>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', marginBottom: '1.25rem' }}>
            Provide any local project directory path on this machine to immediately parse AST symbols and cluster features.
          </p>
          <form onSubmit={handleLocalSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', maxWidth: '640px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-dim)', marginBottom: '0.4rem', fontWeight: 600 }}>
                Project Display Name
              </label>
              <input
                type="text"
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                style={{
                  width: '100%',
                  background: 'rgba(11, 15, 25, 0.9)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '8px',
                  padding: '0.65rem 1rem',
                  color: '#fff',
                  fontSize: '0.9rem',
                  outline: 'none'
                }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-dim)', marginBottom: '0.4rem', fontWeight: 600 }}>
                Local Folder Path (Absolute or Relative)
              </label>
              <input
                type="text"
                placeholder="e.g., examples/tell_story or backend or C:\path\to\codebase"
                value={localPath}
                onChange={(e) => setLocalPath(e.target.value)}
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
              disabled={loading || !localPath.trim()}
              style={{ alignSelf: 'flex-start', padding: '0.65rem 1.5rem' }}
            >
              {loading ? 'Analyzing Codebase...' : 'Scan & Analyze Directory'}
            </button>
          </form>
        </div>
      )}

      {/* Mode 3: ZIP Archive Upload */}
      {ingestMode === 'zip' && (
        <div style={{ background: 'rgba(15, 20, 32, 0.85)', border: '1px solid var(--border-focus)', borderRadius: '14px', padding: '1.75rem' }}>
          <h3 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '0.5rem' }}>Upload ZIP Code Archive</h3>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', marginBottom: '1.25rem' }}>
            Upload any compressed repository zip containing Java, Python, TypeScript, React, Go, or C# codebases.
          </p>
          <form onSubmit={handleZipSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', maxWidth: '640px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-dim)', marginBottom: '0.4rem', fontWeight: 600 }}>
                Project Name
              </label>
              <input
                type="text"
                value={zipName}
                onChange={(e) => setZipName(e.target.value)}
                style={{
                  width: '100%',
                  background: 'rgba(11, 15, 25, 0.9)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '8px',
                  padding: '0.65rem 1rem',
                  color: '#fff',
                  fontSize: '0.9rem',
                  outline: 'none'
                }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-dim)', marginBottom: '0.4rem', fontWeight: 600 }}>
                Select .zip File
              </label>
              <input
                type="file"
                accept=".zip"
                onChange={(e) => setZipFile(e.target.files?.[0] || null)}
                style={{
                  width: '100%',
                  background: 'rgba(11, 15, 25, 0.9)',
                  border: '1px dashed var(--border-subtle)',
                  borderRadius: '8px',
                  padding: '1rem',
                  color: '#cbd5e1',
                  fontSize: '0.85rem',
                  cursor: 'pointer'
                }}
              />
            </div>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading || !zipFile}
              style={{ alignSelf: 'flex-start', padding: '0.65rem 1.5rem' }}
            >
              {loading ? 'Extracting & Analyzing ZIP...' : 'Upload & Reverse Engineer'}
            </button>
          </form>
        </div>
      )}

      {/* Mode 4: IEEE Benchmark Quick-Load */}
      {ingestMode === 'benchmark' && (
        <div style={{ background: 'rgba(15, 20, 32, 0.85)', border: '1px solid var(--border-subtle)', borderRadius: '14px', padding: '1.75rem' }}>
          <h3 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '0.5rem' }}>IEEE Access Ground Truth Benchmark</h3>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
            Load the official Tell Story benchmark (<code>Enemy</code>, <code>Hero</code>, <code>Princess</code>, <code>Story</code>) to inspect automated clustering, evaluate F1/Precision/Recall against ground truth, and generate diagrams.
          </p>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={onLoadBenchmark}
            disabled={loading}
            style={{ padding: '0.75rem 1.75rem', fontWeight: 600 }}
          >
            {loading ? 'Loading Benchmark...' : 'Load Tell Story Benchmark'}
          </button>
        </div>
      )}
    </div>
  );
}
