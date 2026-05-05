// SPDX-License-Identifier: AGPL-3.0-or-later

type DocumentLinkRowProps = {
  href: string;
  label: string;
  sourceLabel?: string;
};

function formatDocumentSource(value: string, fallback?: string): string {
  if (fallback) return fallback;
  try {
    const url = value.startsWith("/")
      ? new URL(value, "https://protocol.omegax.health")
      : new URL(value);
    return url.hostname;
  } catch {
    return "Metadata";
  }
}

function isOpenableHref(value: string): boolean {
  const normalized = value.trim();
  if (!normalized) return false;
  if (normalized.startsWith("/")) return true;
  try {
    const url = new URL(normalized);
    return url.protocol === "https:" || url.protocol === "http:";
  } catch {
    return false;
  }
}

export function DocumentLinkRow({ href, label, sourceLabel }: DocumentLinkRowProps) {
  const normalizedHref = href.trim();
  const canOpen = isOpenableHref(normalizedHref);

  return (
    <div className="plans-review-document">
      <div className="plans-review-document-copy">
        <span className="plans-review-document-label">{label}</span>
        <span className="plans-review-document-host">{formatDocumentSource(normalizedHref, sourceLabel)}</span>
        <span className="plans-review-document-url" title={normalizedHref}>{normalizedHref}</span>
      </div>
      {canOpen ? (
        <a
          className="secondary-button plans-review-document-action"
          href={normalizedHref}
          target="_blank"
          rel="noreferrer"
          aria-label={`Open ${label}`}
        >
          Open
          <span className="material-symbols-outlined" aria-hidden="true">open_in_new</span>
        </a>
      ) : null}
    </div>
  );
}
