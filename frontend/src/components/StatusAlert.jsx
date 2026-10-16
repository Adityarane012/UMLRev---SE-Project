import React from 'react';

export default function StatusAlert({ statusMsg, copyFeedback, loading }) {
  if (!statusMsg && !copyFeedback) return null;

  return (
    <div
      style={{
        background: copyFeedback ? 'rgba(16, 185, 129, 0.15)' : 'rgba(99, 102, 241, 0.12)',
        border: `1px solid ${copyFeedback ? 'rgba(16, 185, 129, 0.4)' : 'rgba(99, 102, 241, 0.3)'}`,
        borderRadius: '12px',
        padding: '0.85rem 1.25rem',
        marginBottom: '1.5rem',
        color: copyFeedback ? '#6ee7b7' : '#c7d2fe',
        fontSize: '0.9rem',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}
    >
      <span>{copyFeedback || statusMsg}</span>
      {loading && <span style={{ animation: 'spin 1s linear infinite' }}>...</span>}
    </div>
  );
}
