import React from 'react';

export default function StatusAlert({ statusMsg, copyFeedback, loading }) {
  if (!statusMsg && !copyFeedback) return null;
  const isError = Boolean(statusMsg && (statusMsg.toLowerCase().includes('error') || statusMsg.toLowerCase().includes('failed') || statusMsg.toLowerCase().includes('invalid')));

  let bg = 'rgba(99, 102, 241, 0.12)';
  let border = 'rgba(99, 102, 241, 0.3)';
  let color = '#c7d2fe';

  if (copyFeedback) {
    bg = 'rgba(16, 185, 129, 0.15)';
    border = 'rgba(16, 185, 129, 0.4)';
    color = '#6ee7b7';
  } else if (isError) {
    bg = 'rgba(239, 68, 68, 0.15)';
    border = 'rgba(239, 68, 68, 0.4)';
    color = '#fca5a5';
  }

  return (
    <div
      style={{
        background: bg,
        border: `1px solid ${border}`,
        borderRadius: '12px',
        padding: '0.85rem 1.25rem',
        marginBottom: '1.5rem',
        color: color,
        fontSize: '0.9rem',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
        <span>{isError ? '⚠️' : (copyFeedback ? '✓' : 'ℹ️')}</span>
        <span>{copyFeedback || statusMsg}</span>
      </div>
      {loading && <span style={{ animation: 'spin 1s linear infinite' }}>⏳</span>}
    </div>
  );
}
