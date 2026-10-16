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
  const [codeTab, setCodeTab] = useState('visual'); // 'visual', 'mermaid', 'plantuml'
  const [evalResults, setEvalResults] = useState(null);

  const diagramRef = useRef(null);

  // 1. Ingest via GitHub URL
  const handleIngestGitHub = async (e) => {
    e?.preventDefault();
    if (!githubUrl.trim()) return;

    setLoading(true);
    setStatusMsg(`Cloning and analyzing repository: ${githubUrl}...`);
    try {
      const data = await api.ingestGitHub(githubUrl);
      setProjectData(data);
      if (data.recent_commits && data.recent_commits.length > 0) {
        setSelectedCommit(data.recent_commits[0].hash);
      }
      setStatusMsg(`Analyzed repository: ${data.name}. Found ${data.features.length} features.`);
      setActiveTab('features');
    } catch (err) {
      console.error(err);
      setStatusMsg(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // 2. Load Local Benchmark
  const handleLoadBenchmark = async () => {
    setLoading(true);
    setStatusMsg('Loading Tell Story benchmark project...');
    try {
      const createData = await api.createProject('Tell Story Benchmark', 'examples/tell_story');
      const analyzeData = await api.analyzeProject(createData.project_id);
      const diagData = await api.getDiagrams(createData.project_id);

      setProjectData({
        ...createData,
        ...analyzeData,
        diagrams: diagData.diagrams
      });
      setStatusMsg('Benchmark loaded and analyzed successfully.');
      setActiveTab('features');
    } catch (err) {
      console.error(err);
      setStatusMsg('Failed to connect to backend API on port 8000.');
    } finally {
      setLoading(false);
    }
  };

  // 3. Analyze Git Diff / Changes
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

  // 4. Render Mermaid Diagram
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
          if (diagramRef.current) {
            diagramRef.current.innerHTML = svg;
          }
        })
        .catch((err) => {
          console.warn('Mermaid render error:', err);
          if (diagramRef.current) {
            diagramRef.current.innerHTML = `<pre style="color:#ef4444; padding:1rem;">Rendering fallback:\n${currentDiagram.svg_content}</pre>`;
          }
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
      const data = await api.evaluateProject(projectData.project_id, {
        'Tell Story': ['Enemy', 'Hero', 'Princess', 'Story']
      });
      setEvalResults(data);
    } catch (e) {
      console.error(e);
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
        onOpenEval={handleRunEvaluation}
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
            onLoadBenchmark={handleLoadBenchmark}
          />
        )}

        {/* Tab 2: AI Features */}
        {activeTab === 'features' && (
          <FeaturesTab
            projectData={projectData}
            onSelectFeatureForExplorer={(idx) => {
              setSelectedFeatureIdx(idx);
              setActiveTab('explorer');
            }}
            onGoToDiff={() => setActiveTab('diff')}
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
            onRunEvaluation={handleRunEvaluation}
            onGoToExplorer={() => setActiveTab('explorer')}
          />
        )}
      </main>
    </div>
  );
}
