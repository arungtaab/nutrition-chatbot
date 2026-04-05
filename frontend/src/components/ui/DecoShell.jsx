/**
 * Organic editorial stage: jewel spine, soft smoke blobs, paper grain,
 * slow sunburst. Decorative layers are aria-hidden; motion respects
 * prefers-reduced-motion.
 */
export function DecoShell({ children }) {
  return (
    <div className="deco-root">
      <div className="deco-blobs" aria-hidden="true" />
      <div className="deco-sunburst" aria-hidden="true" />
      <div className="deco-vignette" aria-hidden="true" />
      <div className="deco-paper-wash" aria-hidden="true" />
      <div className="deco-grain" aria-hidden="true" />
      <div className="deco-content">{children}</div>
    </div>
  );
}
