#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Certora Solana sanity build wrapper.
#
# The workspace defines more than one `cdylib` program, so the default
# `cargo certora-sbf` build is ambiguous and fails with
# "more than one cdylib package found". Scope the build to the coverage
# protocol crate, which is the only crate wired for Certora: its
# `[package.metadata.certora]` carries the nakama_ inlining/summaries used by
# this lane.
#
# Certora invokes this script in place of `cargo certora-sbf`, but with its own
# build-driver flags (e.g. `-l`, `--cargo_features`) that `cargo certora-sbf`
# does not accept. So we ignore the forwarded args and run the explicit,
# scoped build; `--json` makes it emit the build descriptor Certora consumes.
#
# Keep `--tools-version` / `--features` in sync with `cargo_tools_version` /
# `cargo_features` in formal_verification/certora/configs/sanity.conf.
set -euo pipefail

exec cargo certora-sbf --json --tools-version v1.48 --features certora \
  --manifest-path programs/nakama_coverage_protocol/Cargo.toml
