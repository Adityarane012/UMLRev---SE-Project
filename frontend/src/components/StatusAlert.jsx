import React, { useState, useEffect } from 'react';

export default function StatusAlert({ statusMsg, copyFeedback, loading }) {
  const [elapsedSeconds, setElapsedSeconds] = useState(0);

  // Timer & countdown management
  useEffect(() => {
    let interval = null;
    if (loading) {
      setElapsedSeconds(0);
      interval = setInterval(() => {
        setElapsedSeconds((prev) => prev + 1);
      }, 1000);
    } else {
      setElapsedSeconds(0);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [loading, statusMsg]);

  if (!statusMsg && !copyFeedback) return null;

  const isError = Boolean(
    statusMsg &&
      (statusMsg.toLowerCase().includes('error') ||
        statusMsg.toLowerCase().includes('failed') ||
        statusMsg.toLowerCase().includes('invalid'))
  );

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

  // Determine estimated total duration and pipeline stage based on operation
  const lowerMsg = (statusMsg || '').toLowerCase();
  let estimatedTotal = 16;
  let currentStepText = 'Processing codebase...';

  if (lowerMsg.includes('cloning') || lowerMsg.includes('github')) {
    estimatedTotal = 18;
    if (elapsedSeconds < 5) {
      currentStepText = 'Step 1/4: Fetching & cloning Git repository objects...';
    } else if (elapsedSeconds < 10) {
      currentStepText = 'Step 2/4: Scanning AST syntax trees & extracting classes/methods...';
    } else if (elapsedSeconds < 15) {
      currentStepText = 'Step 3/4: Semantic clustering & feature discovery...';
    } else {
      currentStepText = 'Step 4/4: Synthesizing interactive UML Class & Sequence diagrams...';
    }
  } else if (lowerMsg.includes('scanning local') || lowerMsg.includes('local path') || lowerMsg.includes('local project')) {
    estimatedTotal = 8;
    if (elapsedSeconds < 3) {
      currentStepText = 'Step 1/3: Reading local directory & parsing AST models...';
    } else if (elapsedSeconds < 6) {
      currentStepText = 'Step 2/3: Semantic clustering & feature analysis...';
    } else {
      currentStepText = 'Step 3/3: Generating UML diagrams...';
    }
  } else if (lowerMsg.includes('zip') || lowerMsg.includes('archive') || lowerMsg.includes('uploading')) {
    estimatedTotal = 10;
    if (elapsedSeconds < 3) {
      currentStepText = 'Step 1/3: Extracting ZIP archive contents...';
    } else if (elapsedSeconds < 7) {
      currentStepText = 'Step 2/3: Scanning AST symbols & classes...';
    } else {
      currentStepText = 'Step 3/3: Synthesizing UML diagrams...';
    }
  }

  const remainingSeconds = Math.max(0, estimatedTotal - elapsedSeconds);
  const formatTime = (sec) => {
    const mins = Math.floor(sec / 60);
    const secs = sec % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  // Progress percentage calculation (smoothly approaches 95% if taking longer than estimated)
  let progressPct = 0;
  if (loading) {
    if (elapsedSeconds < estimatedTotal) {
      progressPct = Math.round((elapsedSeconds / estimatedTotal) * 90);
    } else {
      progressPct = Math.min(96, 90 + Math.round((elapsedSeconds - estimatedTotal) * 1.5));
    }
  }

  return (
    <>
      <style>{`
        @keyframes umlrev-spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        @keyframes umlrev-pulse-dot {
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.4; transform: scale(0.85); }
        }
      `}</style>

      <div
        style={{
          position: 'relative',
          overflow: 'hidden',
          background: bg,
          border: `1px solid ${border}`,
          borderRadius: '12px',
          padding: '0.85rem 1.25rem',
          marginBottom: '1.5rem',
          color: color,
          fontSize: '0.9rem',
          boxShadow: '0 4px 12px rgba(0,0,0,0.18)',
          transition: 'all 0.25s ease'
        }}
      >
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '1rem',
            flexWrap: 'wrap'
          }}
        >
          {/* Left: Clean SVG Icon & Status Message + Subtitle Step */}
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem', flex: 1, minWidth: '260px' }}>
            <div style={{ marginTop: '2px', flexShrink: 0 }}>
              {isError ? (
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f87171" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>
                  <line x1="12" y1="9" x2="12" y2="13"/>
                  <line x1="12" y1="17" x2="12.01" y2="17"/>
                </svg>
              ) : copyFeedback ? (
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#34d399" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                  <polyline points="22 4 12 14.01 9 11.01"/>
                </svg>
              ) : (
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#818cf8" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="12" y1="16" x2="12" y2="12"/>
                  <line x1="12" y1="8" x2="12.01" y2="8"/>
                </svg>
              )}
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.2rem' }}>
              <span style={{ fontWeight: 500, wordBreak: 'break-word', lineHeight: 1.4 }}>
                {copyFeedback || statusMsg}
              </span>

              {/* Dynamic Next Step / Pipeline Stage */}
              {loading && (
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.45rem',
                    fontSize: '0.78rem',
                    color: '#93c5fd',
                    fontWeight: 500
                  }}
                >
                  <span
                    style={{
                      display: 'inline-block',
                      width: '6px',
                      height: '6px',
                      borderRadius: '50%',
                      background: '#38bdf8',
                      animation: 'umlrev-pulse-dot 1.5s infinite ease-in-out'
                    }}
                  />
                  <span>{currentStepText}</span>
                </div>
              )}
            </div>
          </div>

          {/* Right: Modern Timer & Estimated Countdown Pill (NO EMOJI) */}
          {loading && (
            <div
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.65rem',
                padding: '0.35rem 0.8rem',
                borderRadius: '8px',
                background: 'rgba(15, 23, 42, 0.75)',
                border: '1px solid rgba(99, 102, 241, 0.35)',
                boxShadow: '0 2px 8px rgba(0, 0, 0, 0.3)'
              }}
            >
              {/* Clean Animated SVG Spinner (Replaces emoji) */}
              <svg
                style={{
                  width: '15px',
                  height: '15px',
                  animation: 'umlrev-spin 0.9s linear infinite',
                  color: '#818cf8',
                  flexShrink: 0
                }}
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
              >
                <circle cx="12" cy="12" r="10" stroke="currentColor" strokeOpacity="0.2" />
                <path d="M12 2a10 10 0 0 1 10 10" strokeLinecap="round" />
              </svg>

              {/* Elapsed Timer */}
              <span
                style={{
                  fontFamily: 'monospace',
                  fontSize: '0.82rem',
                  color: '#e2e8f0',
                  fontWeight: 600
                }}
              >
                {formatTime(elapsedSeconds)}
              </span>

              <span style={{ color: 'rgba(255, 255, 255, 0.25)', fontSize: '0.75rem' }}>|</span>

              {/* Estimated Countdown / Time Left */}
              <span
                style={{
                  fontSize: '0.78rem',
                  fontWeight: 600,
                  color: remainingSeconds > 0 ? '#38bdf8' : '#34d399'
                }}
              >
                {remainingSeconds > 0 ? `Est. ~${remainingSeconds}s left` : 'Finalizing step...'}
              </span>
            </div>
          )}
        </div>

        {/* Subtle Progress Bar along the bottom */}
        {loading && (
          <div
            style={{
              position: 'absolute',
              bottom: 0,
              left: 0,
              right: 0,
              height: '3px',
              background: 'rgba(255, 255, 255, 0.08)'
            }}
          >
            <div
              style={{
                height: '100%',
                width: `${progressPct}%`,
                background: 'linear-gradient(90deg, #6366f1 0%, #06b6d4 100%)',
                boxShadow: '0 0 8px rgba(6, 182, 212, 0.6)',
                transition: 'width 0.8s ease'
              }}
            />
          </div>
        )}
      </div>
    </>
  );
}
