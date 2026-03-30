/**
 * Warm, slow mist layers (CSS-only). Respects prefers-reduced-motion.
 */
export function SoftSmokeBackground({ children, className = "" }) {
  return (
    <div className={`soft-smoke-root ${className}`.trim()}>
      <div className="soft-smoke-layer" aria-hidden="true">
        <div className="soft-smoke-blob soft-smoke-blob--1" />
        <div className="soft-smoke-blob soft-smoke-blob--2" />
        <div className="soft-smoke-blob soft-smoke-blob--3" />
      </div>
      <div className="soft-smoke-content">{children}</div>
    </div>
  );
}
