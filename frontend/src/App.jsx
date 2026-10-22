import React, { useState, useEffect, useRef } from 'react';
import mermaid from 'mermaid';

import Header from './components/Header';
import StatusAlert from './components/StatusAlert';
import IngestTab from './components/IngestTab';
import FeaturesTab from './components/FeaturesTab';
import DiffTab from './components/DiffTab';
import DiagramExplorer from './components/DiagramExplorer';
import EvalTab from './components/EvalTab';
import * as api from './services/api';

// The reference answer Stage 5 scores against: the feature-to-class mapping the
// IEEE Access paper documents for its "Tell Story" benchmark project.
const GROUND_TRUTH = {
  'Tell Story': ['Enemy', 'Hero', 'Princess', 'Story']
};

mermaid.initialize({
  startOnLoad: false,
  theme: 'dark',
  securityLevel: 'loose',
  fontFamily: 'Outfit, sans-serif'
});

export default function App() {
  const [activeTab, setActiveTab] = useState('ingest');
  const [projectData, setProjectData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState('');
  const [githubUrl, setGithubUrl] = useState('');
  const [selectedCommit, setSelectedCommit] = useState('');
  const [diffReport, setDiffReport] = useState(null);
  const [selectedFeatureIdx, setSelectedFeatureIdx] = useState(0);
  const [selectedDiagramKind, setSelectedDiagramKind] = useState('CLASS'); // CLASS or SEQUENCE
  const [zoomLevel, setZoomLevel] = useState(1);
  const [copyFeedback, setCopyFeedback] = useState('');
  // Result of parsing the current diagram, so the UI can vouch for the generated code.
  const [diagramStatus, setDiagramStatus] = useState(null);
  // Whether the backend is actually answering, surfaced as the header's live dot.
  const [backendOnline, setBackendOnline] = useState(null);
  const [codeTab, setCodeTab] = useState('visual'); // 'visual', 'mermaid', 'plantuml'
  const [evalResults, setEvalResults] = useState(null);
  const [isApproved, setIsApproved] = useState(false);

  // User Authentication State (TC-01)
  const [currentUser, setCurrentUser] = useState({
    username: 'aditya',
    name: 'Aditya Rane',
    token: 'token-session'
  });
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [loginUsername, setLoginUsername] = useState('aditya');
  const [loginPassword, setLoginPassword] = useState('password123');
  const [loginError, setLoginError] = useState('');

  const diagramRef = useRef(null);

  // Check backend health & identity profile on mount
  useEffect(() => {
    api.getAuthMe()
      .then((data) => {
        if (data.username) {
          setCurrentUser((prev) => ({
            ...prev,
            username: data.username,
            name: data.name
          }));
        }
      })
      .catch(() => {
        // Fallback to local default session
      });
  }, []);

  // Poll backend reachability so the header dot reports something real.
  useEffect(() => {
    let cancelled = false;
    const ping = () =>
      api
        .getHealth()
        .then(() => !cancelled && setBackendOnline(true))
        .catch(() => !cancelled && setBackendOnline(false));
    ping();
    const id = setInterval(ping, 15000);
    return () => {
      cancelled = true;
      clearInterval(id);
    };
  }, []);

  // 1. Ingest via GitHub URL (TC-02)
  const handleIngestGitHub = async (e) => {
    e?.preventDefault();
    if (!githubUrl.trim()) return;

    setLoading(true);
    setStatusMsg(`Cloning and analyzing repository: ${githubUrl}...`);
    try {
      const data = await api.ingestGitHub(githubUrl);
      setProjectData(data);
      setIsApproved(false);
      setSelectedFeatureIdx(0);
      if (data.recent_commits && data.recent_commits.length > 0) {
        setSelectedCommit(data.recent_commits[0].hash);
      }
      setStatusMsg(`Analyzed repository: ${data.name}. Discovered ${data.features.length} cohesive features across ${data.classes_count} classes.`);
      setActiveTab('features');
    } catch (err) {
      console.error(err);
      setStatusMsg(`Repository Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // 2. Ingest via Local Directory Path
  const handleAnalyzeLocal = async (name, path) => {
    setLoading(true);
    setStatusMsg(`Scanning local repository at '${path}'...`);
    try {
      const createData = await api.createProject(name, path);
      const analyzeData = await api.analyzeProject(createData.project_id);
      const diagData = await api.getDiagrams(createData.project_id);

      setProjectData({
        ...createData,
        ...analyzeData,
        diagrams: analyzeData.diagrams || (diagData && diagData.diagrams) || []
      });
      setIsApproved(false);
      setSelectedFeatureIdx(0);
      setStatusMsg(`Local project '${name}' analyzed successfully. Discovered ${analyzeData.features.length} features.`);
      setActiveTab('features');
    } catch (err) {
      console.error(err);
      setStatusMsg(`Local Path Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // 3. Ingest via ZIP File Upload
  const handleUploadZip = async (file, name) => {
    setLoading(true);
    setStatusMsg(`Uploading and extracting ZIP archive: ${file.name}...`);
    try {
      const data = await api.uploadZip(file, name);
      setProjectData(data);
      setIsApproved(false);
      setSelectedFeatureIdx(0);
      setStatusMsg(`ZIP archive extracted and analyzed. Discovered ${data.features.length} features.`);
      setActiveTab('features');
    } catch (err) {
      console.error(err);
      setStatusMsg(`ZIP Upload Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // 4. Load IEEE Access Benchmark
  const handleLoadBenchmark = async () => {
    setLoading(true);
    setStatusMsg('Loading IEEE Access Tell Story benchmark...');
    try {
      const createData = await api.createProject('Tell Story Benchmark', 'examples/tell_story');
      const analyzeData = await api.analyzeProject(createData.project_id);
      let diagData = null;
      try {
        diagData = await api.getDiagrams(createData.project_id);
      } catch (e) {
        // Fallback to diagrams in analyzeData
      }

      setProjectData({
        ...createData,
        ...analyzeData,
        diagrams: analyzeData.diagrams || (diagData && diagData.diagrams) || []
      });
      setIsApproved(false);
      setSelectedFeatureIdx(0);
      setStatusMsg('Benchmark loaded and analyzed successfully.');
      setActiveTab('features');
    } catch (err) {
      console.error(err);
      setStatusMsg(`Benchmark Error: ${err.message || 'Failed to load benchmark'}`);
    } finally {
      setLoading(false);
    }
  };

  // 5. Developer Feature Review & Approval (TC-03)
  const handleApproveFeatures = async (updatedFeatures) => {
    if (!projectData) return;
    setLoading(true);
    try {
      const res = await api.updateFeatures(projectData.project_id, updatedFeatures);
      setProjectData((prev) => ({
        ...prev,
        features: res.features,
        diagrams: res.diagrams || prev.diagrams
      }));
      setIsApproved(true);
      setStatusMsg('Feature architecture approved by developer. Diagram models re-synchronized.');
    } catch (err) {
      console.error(err);
      setStatusMsg(`Approval Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // 6. Analyze Git Diff / Changes
  const handleAnalyzeDiff = async () => {
    if (!projectData) return;
    setLoading(true);
    setStatusMsg(`Analyzing changes for commit ${selectedCommit || 'HEAD'}...`);
    try {
      const data = await api.analyzeDiff(projectData.project_id, selectedCommit);
      setDiffReport(data.diff_report);
      setProjectData((prev) => ({
        ...prev,
        diagrams: data.diagrams
      }));
      setStatusMsg(`Identified '${data.diff_report.feature_name}' with ${data.modified_classes.length} modified classes.`);
    } catch (err) {
      console.error(err);
      setStatusMsg(`Diff analysis error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // 7. Render Mermaid Diagram (TC-04)
  useEffect(() => {
    if (!projectData || !projectData.diagrams) return;

    const currentFeature = projectData.features[selectedFeatureIdx];
    if (!currentFeature) return;

    const currentDiagram = projectData.diagrams.find(
      (d) => d.feature_name === currentFeature.name && d.kind === selectedDiagramKind
    );

    if (currentDiagram && diagramRef.current) {
      const renderId = `mermaid-${Date.now()}`;
      mermaid
        .render(renderId, currentDiagram.svg_content)
        .then(({ svg }) => {
          const puml = currentDiagram.uml_text || '';
          const pumlOk =
            puml.includes('@startuml') &&
            puml.includes('@enduml') &&
            (puml.match(/{/g) || []).length === (puml.match(/}/g) || []).length;
          setDiagramStatus({
            ok: pumlOk,
            mermaidLines: currentDiagram.svg_content.split('\n').length,
            pumlLines: puml.split('\n').length,
            message: pumlOk
              ? 'Mermaid parsed and rendered; PlantUML blocks balanced'
              : 'Mermaid parsed, but PlantUML markers/braces look unbalanced'
          });
          if (diagramRef.current) {
            diagramRef.current.innerHTML = svg;
          }
        })
        .catch((err) => {
          console.warn('Mermaid render error:', err);
          if (!diagramRef.current) return;

          // Surface the parser's own message and point at the offending source line,
          // so a failed render is diagnosable instead of just a wall of red code.
          const message = String((err && err.message) || err);
          const lineNo = Number(message.match(/line[: ]+(\d+)/i)?.[1]);
          const srcLines = currentDiagram.svg_content.split('\n');
          setDiagramStatus({ ok: false, failed: true, message: message.split('\n')[0] });
          const escape = (t) =>
            String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

          const numbered = srcLines
            .map((line, i) => {
              const n = i + 1;
              const body = `${String(n).padStart(4, ' ')} | ${escape(line)}`;
              return n === lineNo
                ? `<span style="background:#7f1d1d; color:#fecaca; display:block;">${body}  &lt;&lt;&lt; here</span>`
                : body;
            })
            .join('\n');

          diagramRef.current.innerHTML = `
            <div style="padding:1rem; background:#0f172a; border:1px solid #ef4444; border-radius:8px;">
              <div style="color:#fca5a5; font-weight:700; margin-bottom:0.5rem;">
                Mermaid could not render this diagram
              </div>
              <pre style="color:#fecaca; white-space:pre-wrap; margin:0 0 0.85rem 0;">${escape(message)}</pre>
              <details>
                <summary style="color:#94a3b8; cursor:pointer; margin-bottom:0.5rem;">
                  Show generated Mermaid source (${srcLines.length} lines)
                </summary>
                <pre style="color:#cbd5e1; margin:0; overflow:auto; max-height:420px;">${numbered}</pre>
              </details>
            </div>`;
        });
    }
  }, [projectData, selectedFeatureIdx, selectedDiagramKind, activeTab, codeTab]);

  // Copy Diagram-as-Code to Clipboard
  const handleCopy = (text, typeName) => {
    navigator.clipboard.writeText(text);
    setCopyFeedback(`Copied ${typeName} markup to clipboard.`);
    setTimeout(() => setCopyFeedback(''), 3000);
  };

  // Run ground truth evaluation
  const handleRunEvaluation = async () => {
    if (!projectData) return;
    try {
      const data = await api.evaluateProject(projectData.project_id, GROUND_TRUTH);
      setEvalResults(data);
    } catch (e) {
      console.error(e);
    }
  };

  // Login Form Submission (TC-01)
  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setLoginError('');
    try {
      const res = await api.login(loginUsername, loginPassword);
      setCurrentUser({
        username: res.username,
        name: res.username === 'aditya' ? 'Aditya Rane' : res.username,
        token: res.token
      });
      setShowLoginModal(false);
      setStatusMsg(`Authenticated as ${res.username}. Dashboard unlocked.`);
    } catch (err) {
      setLoginError(err.message || 'Login failed. Check credentials.');
    }
  };

  const getCurrentDiagram = () => {
    if (!projectData || !projectData.features || !projectData.diagrams) return null;
    const currentFeature = projectData.features[selectedFeatureIdx];
    if (!currentFeature) return null;
    return projectData.diagrams.find(
      (d) => d.feature_name === currentFeature.name && d.kind === selectedDiagramKind
    );
  };

  const currentDiag = getCurrentDiagram();

  return (
    <div className="app-container">
      {/* Header & Tabs */}
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        hasProjectData={Boolean(projectData)}
        projectData={projectData}
        backendOnline={backendOnline}
        isApproved={isApproved}
        diffReport={diffReport}
        evalResults={evalResults}
        onOpenEval={handleRunEvaluation}
        currentUser={currentUser}
        onOpenLoginModal={() => setShowLoginModal(true)}
      />

      {/* Main Content Area */}
      <main className="main-content">
        {/* Status / Alert Banner */}
        <StatusAlert
          statusMsg={statusMsg}
          copyFeedback={copyFeedback}
          loading={loading}
        />

        {/* Tab 1: Ingest */}
        {activeTab === 'ingest' && (
          <IngestTab
            githubUrl={githubUrl}
            setGithubUrl={setGithubUrl}
            loading={loading}
            onIngestGitHub={handleIngestGitHub}
          />
        )}

        {/* Tab 2: Feature Discovery */}
        {activeTab === 'features' && (
          <FeaturesTab
            projectData={projectData}
            onSelectFeatureForExplorer={(idx) => {
              setSelectedFeatureIdx(idx);
              setActiveTab('explorer');
            }}
            onGoToDiff={() => setActiveTab('diff')}
            onApproveFeatures={handleApproveFeatures}
            isApproved={isApproved}
          />
        )}

        {/* Tab 3: Git Diff Analysis */}
        {activeTab === 'diff' && (
          <DiffTab
            projectData={projectData}
            selectedCommit={selectedCommit}
            setSelectedCommit={setSelectedCommit}
            loading={loading}
            onAnalyzeDiff={handleAnalyzeDiff}
            diffReport={diffReport}
            onGoToExplorer={() => setActiveTab('explorer')}
          />
        )}

        {/* Tab 4: Diagram Explorer */}
        {activeTab === 'explorer' && (
          <DiagramExplorer
            projectData={projectData}
            selectedFeatureIdx={selectedFeatureIdx}
            setSelectedFeatureIdx={setSelectedFeatureIdx}
            selectedDiagramKind={selectedDiagramKind}
            setSelectedDiagramKind={setSelectedDiagramKind}
            codeTab={codeTab}
            setCodeTab={setCodeTab}
            zoomLevel={zoomLevel}
            setZoomLevel={setZoomLevel}
            diagramRef={diagramRef}
            currentDiag={currentDiag}
            diagramStatus={diagramStatus}
            onCopy={handleCopy}
            onGoToDiff={() => setActiveTab('diff')}
            onGoToEval={() => {
              setActiveTab('eval');
              handleRunEvaluation();
            }}
          />
        )}

        {/* Tab 5: Evaluation */}
        {activeTab === 'eval' && (
          <EvalTab
            evalResults={evalResults}
            groundTruth={GROUND_TRUTH}
            onRunEvaluation={handleRunEvaluation}
            onGoToExplorer={() => setActiveTab('explorer')}
          />
        )}
      </main>

      {/* Login Modal (TC-01) */}
      {showLoginModal && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'rgba(0, 0, 0, 0.75)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
            backdropFilter: 'blur(4px)'
          }}
        >
          <div
            style={{
              background: '#0f172a',
              border: '1px solid var(--border-focus)',
              borderRadius: '14px',
              padding: '2rem',
              width: '100%',
              maxWidth: '420px',
              boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.5)'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 700 }}>Developer Authentication</h3>
              <button
                type="button"
                onClick={() => setShowLoginModal(false)}
                style={{ background: 'transparent', border: 'none', color: '#94a3b8', fontSize: '1.25rem', cursor: 'pointer' }}
              >
                ✕
              </button>
            </div>

            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
              Experiment 9 (TC-01) Test Harness: Authenticate as registered developer to access project workspaces and reverse engineering tools.
            </p>

            {loginError && (
              <div style={{ padding: '0.6rem 0.85rem', background: 'rgba(239, 68, 68, 0.15)', border: '1px solid #ef4444', borderRadius: '6px', color: '#ef4444', fontSize: '0.82rem', marginBottom: '1rem' }}>
                {loginError}
              </div>
            )}

            <form onSubmit={handleLoginSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-dim)', marginBottom: '0.35rem', fontWeight: 600 }}>
                  Username / ID
                </label>
                <input
                  type="text"
                  value={loginUsername}
                  onChange={(e) => setLoginUsername(e.target.value)}
                  style={{ width: '100%', background: '#020617', border: '1px solid var(--border-subtle)', borderRadius: '6px', padding: '0.65rem 0.85rem', color: '#fff', fontSize: '0.9rem', outline: 'none' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-dim)', marginBottom: '0.35rem', fontWeight: 600 }}>
                  Password
                </label>
                <input
                  type="password"
                  value={loginPassword}
                  onChange={(e) => setLoginPassword(e.target.value)}
                  style={{ width: '100%', background: '#020617', border: '1px solid var(--border-subtle)', borderRadius: '6px', padding: '0.65rem 0.85rem', color: '#fff', fontSize: '0.9rem', outline: 'none' }}
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '0.5rem' }}>
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => {
                    setLoginUsername('aditya');
                    setLoginPassword('password123');
                  }}
                  style={{ padding: '0.45rem 0.85rem', fontSize: '0.8rem' }}
                >
                  Quickfill (Aditya)
                </button>
                <button
                  type="submit"
                  className="btn btn-primary"
                  style={{ padding: '0.55rem 1.35rem', fontSize: '0.88rem' }}
                >
                  Authenticate →
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
