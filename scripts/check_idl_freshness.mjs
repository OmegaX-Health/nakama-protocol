#!/usr/bin/env node
// SPDX-License-Identifier: AGPL-3.0-or-later
//
// IDL freshness check.
//
// `npm run protocol:contract:check` verifies that downstream artifacts are
// in sync with `idl/omegax_protocol.json`, but nothing verifies that the
// checked-in IDL itself matches the on-chain program source. If a developer
// edits Rust under `programs/*/` and forgets to run `npm run anchor:idl`, the
// stale IDL ships and silently desyncs every SDK downstream.
//
// This check hashes the program source and compares it to a stored hash in
// `idl/*.source-hash`. The `anchor:idl` npm script writes those files via
// `--write`; CI runs the check (default mode) and fails on drift.
// Running `anchor build` in CI would be authoritative but requires the
// Anchor + Solana CLI toolchains; the hash check catches the most common
// drift case without that overhead.

import { createHash } from 'node:crypto';
import { readFileSync, readdirSync, statSync, writeFileSync } from 'node:fs';
import { join, relative, resolve } from 'node:path';

const REPO_ROOT = resolve(new URL('../', import.meta.url).pathname);
const ROOT_CARGO_TOML = 'Cargo.toml';
const PROGRAMS = [
  {
    name: 'omegax_protocol',
    programDir: 'programs/omegax_protocol',
    idlFile: 'idl/omegax_protocol.json',
    hashFile: 'idl/omegax_protocol.source-hash',
  },
  {
    name: 'omegax_private_claim_review',
    programDir: 'programs/omegax_private_claim_review',
    idlFile: 'idl/omegax_private_claim_review.json',
    hashFile: 'idl/omegax_private_claim_review.source-hash',
  },
];

function gather(dirRel) {
  const out = [];
  const dirAbs = resolve(REPO_ROOT, dirRel);
  for (const name of readdirSync(dirAbs).sort()) {
    if (name === 'target' || name === 'node_modules' || name.startsWith('.')) continue;
    const childAbs = join(dirAbs, name);
    const childRel = relative(REPO_ROOT, childAbs);
    const stat = statSync(childAbs);
    if (stat.isDirectory()) {
      out.push(...gather(childRel));
    } else if (childRel.endsWith('.rs') || childRel.endsWith('Cargo.toml')) {
      out.push(childRel);
    }
  }
  return out;
}

function computeHash(program) {
  const files = [
    ...gather(program.programDir),
    ROOT_CARGO_TOML,
  ].sort();

  const hash = createHash('sha256');
  for (const rel of files) {
    const abs = resolve(REPO_ROOT, rel);
    hash.update(rel);
    hash.update('\0');
    hash.update(readFileSync(abs));
    hash.update('\0');
  }
  return { digest: hash.digest('hex'), files };
}

function formatPayload({ digest, files }) {
  return `${digest}\n${files.map((f) => `  ${f}`).join('\n')}\n`;
}

function readStoredDigest(program) {
  try {
    const contents = readFileSync(resolve(REPO_ROOT, program.hashFile), 'utf8');
    return contents.split('\n', 1)[0]?.trim() ?? '';
  } catch {
    return null;
  }
}

function fileExists(fileRel) {
  try {
    return statSync(resolve(REPO_ROOT, fileRel)).isFile();
  } catch {
    return false;
  }
}

const writeMode = process.argv.includes('--write');
let failed = false;

for (const program of PROGRAMS) {
  const { digest, files } = computeHash(program);

  if (writeMode) {
    writeFileSync(resolve(REPO_ROOT, program.hashFile), formatPayload({ digest, files }));
    process.stdout.write(
      `[idl:freshness] wrote ${program.hashFile} for ${program.name} (${files.length} files, ${digest.slice(0, 12)}...)\n`,
    );
    continue;
  }

  if (!fileExists(program.idlFile)) {
    process.stderr.write(
      `[idl:freshness] missing ${program.idlFile}. Run \`npm run anchor:idl\` to generate it.\n`,
    );
    failed = true;
    continue;
  }

  const stored = readStoredDigest(program);

  if (stored === null) {
    process.stderr.write(
      `[idl:freshness] missing ${program.hashFile}. Run \`npm run anchor:idl\` to generate it.\n`,
    );
    failed = true;
    continue;
  }

  if (stored !== digest) {
    process.stderr.write(
      `[idl:freshness] ${program.name} source has changed but the checked-in IDL is stale.\n`,
    );
    process.stderr.write(`  stored:  ${stored}\n`);
    process.stderr.write(`  current: ${digest}\n`);
    process.stderr.write(
      `Run \`npm run anchor:idl\` and commit ${program.idlFile} plus ${program.hashFile}.\n`,
    );
    failed = true;
    continue;
  }

  process.stdout.write(
    `[idl:freshness] ${program.name} IDL matches program source (${files.length} files, ${digest.slice(0, 12)}...).\n`,
  );
}

process.exit(failed ? 1 : 0);
