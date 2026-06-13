// SPDX-License-Identifier: AGPL-3.0-or-later

import type { ReactNode } from "react";

import { cn } from "@/lib/cn";

export function FieldGroup({
  label,
  children,
  hint,
}: {
  label: string;
  children: ReactNode;
  hint?: ReactNode;
}) {
  return (
    <label className="plans-wizard-field-group">
      <span className="plans-wizard-field-label">{label}</span>
      {children}
      {hint ? <span className="plans-wizard-field-hint">{hint}</span> : null}
    </label>
  );
}

export function ReviewRow({
  label,
  value,
  muted = false,
}: {
  label: string;
  value: string;
  muted?: boolean;
}) {
  return (
    <div className="plans-wizard-review-row">
      <span className="plans-wizard-review-label">{label}</span>
      <strong className={cn("plans-wizard-review-value", muted && "opacity-70")}>{value}</strong>
    </div>
  );
}

export function ReviewSection({
  title,
  description,
  children,
}: {
  title: string;
  description: string;
  children: ReactNode;
}) {
  return (
    <section className="plans-wizard-review-section">
      <div className="plans-wizard-review-section-head">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
      <div className="plans-wizard-review-section-rows">
        {children}
      </div>
    </section>
  );
}

export function LaunchPreviewMetric({
  label,
  value,
  detail,
}: {
  label: string;
  value: string;
  detail: string;
}) {
  return (
    <div className="plans-launch-preview-metric">
      <span className="plans-launch-preview-metric-label">{label}</span>
      <strong className="plans-launch-preview-metric-value">{value}</strong>
      <span className="plans-launch-preview-metric-detail">{detail}</span>
    </div>
  );
}
