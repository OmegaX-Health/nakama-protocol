// SPDX-License-Identifier: AGPL-3.0-or-later

import { resolveSafeDocumentHref } from "@/lib/safe-external-url";

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

function canonicalClickableDocumentHref(value: string | null): "/coverage/technical-terms" | "/coverage/risk-disclosures" | null {
  switch (value) {
    case "/coverage/technical-terms":
    case "https://protocol.omegax.health/coverage/technical-terms":
      return "/coverage/technical-terms";
    case "/coverage/risk-disclosures":
    case "https://protocol.omegax.health/coverage/risk-disclosures":
      return "/coverage/risk-disclosures";
    default:
      return null;
  }
}

export function DocumentLinkRow({ href, label, sourceLabel }: DocumentLinkRowProps) {
  const safeHref = resolveSafeDocumentHref(href);
  const displayHref = safeHref ?? "Unavailable";
  const clickableHref = canonicalClickableDocumentHref(safeHref);
  const documentSource = formatDocumentSource(displayHref, sourceLabel);
  const documentCopy = (
    <div className="plans-review-document-copy">
      <span className="plans-review-document-label">{label}</span>
      <span className="plans-review-document-host">{documentSource}</span>
      <span className="plans-review-document-url" title={displayHref}>{displayHref || "Unavailable"}</span>
    </div>
  );

  if (!clickableHref) {
    return (
      <div className="plans-review-document" aria-disabled={safeHref ? undefined : "true"}>
        {documentCopy}
      </div>
    );
  }

  return (
    <a
      className="plans-review-document"
      href={clickableHref}
    >
      {documentCopy}
    </a>
  );
}
