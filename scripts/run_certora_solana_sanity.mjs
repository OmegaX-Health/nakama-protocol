#!/usr/bin/env node
// SPDX-License-Identifier: AGPL-3.0-or-later

import { spawnSync } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const lockfile = 'Cargo.lock';
const config = 'formal_verification/certora/configs/sanity.conf';
const cargoTargetDir = resolve('.certora_internal/cargo-target');

const originalLock = readFileSync(lockfile, 'utf8');
const certoraLock = originalLock.replace(/^version = 4$/m, 'version = 3');

if (certoraLock === originalLock) {
  console.warn('[certora:solana:sanity] Cargo.lock did not contain `version = 4`; no lockfile shim applied.');
} else {
  writeFileSync(lockfile, certoraLock);
}

try {
  const result = spawnSync('certoraSolanaProver', [config, ...process.argv.slice(2)], {
    cwd: process.cwd(),
    env: { ...process.env, CARGO_TARGET_DIR: cargoTargetDir },
    stdio: 'inherit',
  });

  process.exitCode = result.status ?? 1;
} finally {
  writeFileSync(lockfile, originalLock);
}
