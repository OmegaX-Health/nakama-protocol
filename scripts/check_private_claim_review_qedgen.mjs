#!/usr/bin/env node
// SPDX-License-Identifier: AGPL-3.0-or-later
//
// Lightweight QEDGen gate for the MagicBlock private claim-review adjunct.
//
// The main protocol has the full generated backend lane in `run_qedgen.mjs`.
// The adjunct spec is intentionally smaller and hand-authored, but it must
// still parse and stay handler/effect aligned so a stale proof model cannot
// pass CI unnoticed.

import { accessSync, constants, existsSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';

const SPEC = 'formal_verification/omegax_private_claim_review.qedspec';
const ANCHOR_PROJECT = 'programs/omegax_private_claim_review';

function isExecutable(path) {
  try {
    accessSync(path, constants.X_OK);
    return true;
  } catch {
    return false;
  }
}

function commandExists(name) {
  const result = spawnSync('sh', ['-lc', `command -v ${name}`], {
    encoding: 'utf8',
  });
  return result.status === 0;
}

function resolveQedgen() {
  const candidates = [
    process.env.QEDGEN,
    join(homedir(), '.codex/skills/qedgen/tools/qedgen'),
    join(homedir(), '.codex/skills/qedgen/bin/qedgen'),
    'qedgen',
  ].filter(Boolean);

  for (const candidate of candidates) {
    if (candidate === 'qedgen') {
      if (commandExists(candidate)) return candidate;
      continue;
    }

    if (existsSync(candidate) && isExecutable(candidate)) return candidate;
  }

  throw new Error(
    'Unable to find qedgen. Set QEDGEN=/path/to/qedgen or install the QEDGen skill.',
  );
}

function parseJsonObjects(text) {
  const docs = [];
  let depth = 0;
  let start = -1;
  let inString = false;
  let escaped = false;

  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];

    if (inString) {
      if (escaped) {
        escaped = false;
      } else if (ch === '\\') {
        escaped = true;
      } else if (ch === '"') {
        inString = false;
      }
      continue;
    }

    if (ch === '"') {
      inString = true;
    } else if (ch === '{' || ch === '[') {
      if (depth === 0) start = i;
      depth += 1;
    } else if (ch === '}' || ch === ']') {
      depth -= 1;
      if (depth === 0 && start >= 0) {
        docs.push(JSON.parse(text.slice(start, i + 1)));
        start = -1;
      }
    }
  }

  return docs;
}

const qedgen = resolveQedgen();
const result = spawnSync(
  qedgen,
  [
    'check',
    '--spec',
    SPEC,
    '--anchor-project',
    ANCHOR_PROJECT,
    '--coverage',
    '--json',
  ],
  {
    cwd: process.cwd(),
    encoding: 'utf8',
    maxBuffer: 50 * 1024 * 1024,
    shell: false,
  },
);

if (result.stderr) process.stderr.write(result.stderr);
if (result.stdout) process.stdout.write(result.stdout);
if (result.error) throw result.error;
if (result.status !== 0) process.exit(result.status ?? 1);

const docs = parseJsonObjects(result.stdout ?? '');
let failed = false;
for (const doc of docs) {
  if (Array.isArray(doc.effect_coverage) && doc.effect_coverage.length > 0) {
    process.stderr.write('[qedgen:private-claim-review] effect coverage drift found.\n');
    failed = true;
  }
  if (Array.isArray(doc.handler_coverage) && doc.handler_coverage.length > 0) {
    process.stderr.write('[qedgen:private-claim-review] handler coverage drift found.\n');
    failed = true;
  }
}

if (docs.length === 0) {
  process.stderr.write('[qedgen:private-claim-review] no QEDGen JSON output found.\n');
  failed = true;
}

process.exit(failed ? 1 : 0);
