/**
 * REST API client for UMLRev backend.
 */

const API_BASE = '';

export async function login(username, password) {
  const res = await fetch(`${API_BASE}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  if (!res.ok) throw new Error('Authentication failed');
  return res.json();
}

export async function getHealth() {
  const res = await fetch(`${API_BASE}/api/health`);
  if (!res.ok) throw new Error('Backend unreachable');
  return res.json();
}

export async function getAuthMe() {
  const res = await fetch(`${API_BASE}/api/auth/me`);
  if (!res.ok) throw new Error('Failed to retrieve user profile');
  return res.json();
}

export async function ingestGitHub(githubUrl) {
  const res = await fetch(`${API_BASE}/api/projects/github`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ github_url: githubUrl.trim() })
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'GitHub ingestion failed');
  return data;
}

export async function createProject(name, localPath) {
  const formData = new FormData();
  formData.append('name', name);
  if (localPath) formData.append('local_path', localPath);

  const res = await fetch(`${API_BASE}/api/projects/create`, {
    method: 'POST',
    body: formData
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Project creation failed');
  return data;
}

export async function uploadZip(file, name = 'Uploaded Project') {
  const formData = new FormData();
  formData.append('name', name);
  formData.append('file', file);

  const res = await fetch(`${API_BASE}/api/projects/upload-zip`, {
    method: 'POST',
    body: formData
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'ZIP upload failed');
  return data;
}

export async function analyzeProject(projectId) {
  const res = await fetch(`${API_BASE}/api/projects/${projectId}/analyze`, {
    method: 'POST'
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Analysis failed');
  return data;
}

export async function getFeatures(projectId) {
  const res = await fetch(`${API_BASE}/api/projects/${projectId}/features`);
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to fetch features');
  return data;
}

export async function updateFeatures(projectId, updatedFeatures) {
  const res = await fetch(`${API_BASE}/api/projects/${projectId}/features`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updatedFeatures)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to update features');
  return data;
}

export async function getDiagrams(projectId) {
  const res = await fetch(`${API_BASE}/api/projects/${projectId}/diagrams`);
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Failed to fetch diagrams');
  return data;
}

export async function analyzeDiff(projectId, commitHash) {
  const res = await fetch(`${API_BASE}/api/projects/${projectId}/analyze-diff`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ commit_hash: commitHash || null })
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Diff analysis failed');
  return data;
}

export async function evaluateProject(projectId, groundTruth) {
  const res = await fetch(`${API_BASE}/api/projects/${projectId}/evaluate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ground_truth: groundTruth })
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Evaluation failed');
  return data;
}
