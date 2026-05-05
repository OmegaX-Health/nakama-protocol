// SPDX-License-Identifier: AGPL-3.0-or-later

import Link from "next/link";

import type { GenesisProtectDisclosurePageContent } from "@/lib/genesis-protect-disclosures";

export function GenesisProtectDisclosurePage({
  content,
}: {
  content: GenesisProtectDisclosurePageContent;
}) {
  const routeFields = [
    { label: "Route", value: content.path, meta: "Public metadata destination" },
    { label: "Canonical URL", value: content.canonicalUrl, meta: "Stable public disclosure link" },
    { label: "Scope", value: "Shared protection metadata", meta: content.statusLabel },
  ];
  const referenceSection = content.sections.find((section) => section.title === "Reference pack");
  const disclosureSections = content.sections.filter((section) => section.title !== "Reference pack");

  return (
    <div className="plans-shell genesis-disclosure-shell">
      <div className="plans-scroll">
        <header className="plans-hero genesis-disclosure-hero">
          <div className="plans-hero-glow" aria-hidden="true" />
          <div className="plans-hero-head">
            <div className="plans-hero-copy">
              <span className="plans-hero-eyebrow">{content.heroEyebrow}</span>
              <h1 className="plans-hero-title">{content.heroTitle}</h1>
              <p className="plans-hero-subtitle">{content.heroSubtitle}</p>
            </div>
            <div className="plans-hero-actions">
              <span className="plans-secondary-cta plans-action-disabled" aria-disabled="true">
                <span className="material-symbols-outlined" aria-hidden="true">policy</span>
                {content.statusLabel}
              </span>
            </div>
          </div>
        </header>

        <div className="plans-context-bar genesis-disclosure-context-bar">
          <div className="plans-context-selectors genesis-disclosure-context-selectors liquid-glass">
            {routeFields.map((field, index) => (
              <div key={field.label} className="contents">
                <div className="genesis-disclosure-context-field">
                  <span className="plans-hero-select-eyebrow">{field.label}</span>
                  <span className="plans-hero-select-label">{field.value}</span>
                  <span className="plans-hero-select-meta">{field.meta}</span>
                </div>
                {index < routeFields.length - 1 ? (
                  <span className="plans-context-divider genesis-disclosure-context-divider" aria-hidden="true" />
                ) : null}
              </div>
            ))}
          </div>
        </div>

        <section className="plans-stack genesis-disclosure-stack">
          <article className="plans-card heavy-glass genesis-disclosure-primer">
            <div>
              <p className="plans-card-eyebrow">Public reference</p>
              <h2 className="plans-card-title plans-card-title-display">Current canonical disclosure route</h2>
            </div>
            <p className="plans-card-body">{content.description}</p>
          </article>

          <div className="genesis-disclosure-grid">
            {disclosureSections.map((section) => (
              <article key={section.title} className="plans-card heavy-glass genesis-disclosure-card">
                <div className="plans-card-head">
                  <div>
                    <p className="plans-card-eyebrow">{section.eyebrow}</p>
                    <h2 className="plans-card-title plans-card-title-display">
                      {section.title}
                    </h2>
                  </div>
                </div>
                <p className="plans-card-body">{section.copy}</p>
                {section.facts?.length ? (
                  <div className="plans-settings-grid genesis-disclosure-facts">
                    {section.facts.map((fact) => (
                      <div key={`${section.title}-${fact.label}`} className="plans-settings-row genesis-disclosure-fact-row">
                        <div>
                          <span className="plans-settings-label">{fact.label}</span>
                        </div>
                        <span className="plans-settings-address genesis-disclosure-value">{fact.value}</span>
                      </div>
                    ))}
                  </div>
                ) : null}
                {section.bullets?.length ? (
                  <ul className="genesis-disclosure-list">
                    {section.bullets.map((bullet) => (
                      <li key={`${section.title}-${bullet}`}>{bullet}</li>
                    ))}
                  </ul>
                ) : null}
              </article>
            ))}
          </div>

          {referenceSection ? (
            <article className="plans-card heavy-glass genesis-disclosure-reference">
              <div className="plans-card-head">
                <div>
                  <p className="plans-card-eyebrow">{referenceSection.eyebrow}</p>
                  <h2 className="plans-card-title plans-card-title-display">{referenceSection.title}</h2>
                </div>
              </div>
              <p className="plans-card-body">{referenceSection.copy}</p>
              <div className="plans-settings-grid genesis-disclosure-reference-grid">
                {referenceSection.facts?.map((fact) => (
                  <div key={`${referenceSection.title}-${fact.label}`} className="plans-settings-row genesis-disclosure-fact-row">
                    <div>
                      <span className="plans-settings-label">{fact.label}</span>
                    </div>
                    <span className="plans-settings-address genesis-disclosure-value">{fact.value}</span>
                  </div>
                ))}
              </div>
            </article>
          ) : null}

          <article className="plans-card heavy-glass genesis-disclosure-action">
            <div>
              <p className="plans-card-eyebrow">Genesis pack</p>
              <h2 className="plans-card-title">Continue through the public launch pack</h2>
            </div>
            <p className="plans-card-body">
              These disclosure routes exist so the live protection metadata resolves to real public pages. They should stay aligned with the linked Genesis docs pack and protocol metadata, not drift into a separate story.
            </p>
            <div className="protocol-actions">
              <Link href="https://docs.omegax.health/docs/coverage/genesis-protect-acute" className="plans-secondary-cta">
                Open Genesis product page
              </Link>
              <Link href="https://docs.omegax.health/docs/coverage/genesis-protect-faq" className="plans-secondary-cta">
                Open Genesis FAQ
              </Link>
            </div>
          </article>
        </section>
      </div>
    </div>
  );
}
