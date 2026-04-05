/** Asymmetric editorial rule — brass diamond + unequal rails. */
export function SectionDecoDivider() {
  return (
    <div className="deco-divider" role="separator" aria-hidden="true">
      <span className="deco-divider-line" />
      <span className="deco-divider-diamond" />
      <span className="deco-divider-line" />
    </div>
  );
}
