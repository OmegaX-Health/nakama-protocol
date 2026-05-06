#!/usr/bin/env node
// SPDX-License-Identifier: AGPL-3.0-or-later

import { spawnSync } from 'node:child_process';
import { createWriteStream, existsSync, mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { get as httpsGet } from 'node:https';

const recentJobsPath = '.certora_internal/.certora_recent_jobs.json';
const showReportUrl = process.argv.includes('--show-report-url');

function readLatestJob() {
  if (!existsSync(recentJobsPath)) {
    throw new Error(`${recentJobsPath} not found. Run npm run certora:solana:sanity first.`);
  }

  const recentJobs = JSON.parse(readFileSync(recentJobsPath, 'utf8'));
  const cwd = process.cwd();
  const cwdResolved = resolve(cwd);
  const jobs = recentJobs[cwd] ?? recentJobs[cwdResolved];
  if (!Array.isArray(jobs) || jobs.length === 0) {
    throw new Error(`No recent Certora jobs recorded for ${cwd}.`);
  }

  return jobs[0];
}

function request(url, responseType = 'text', redirects = 0) {
  return new Promise((resolvePromise, rejectPromise) => {
    httpsGet(url, (response) => {
      const { statusCode, headers } = response;
      if ([301, 302, 303, 307, 308].includes(statusCode) && headers.location && redirects < 8) {
        response.resume();
        request(new URL(headers.location, url), responseType, redirects + 1)
          .then(resolvePromise)
          .catch(rejectPromise);
        return;
      }

      const chunks = [];
      response.on('data', (chunk) => chunks.push(chunk));
      response.on('end', () => {
        const body = Buffer.concat(chunks);
        resolvePromise({
          body: responseType === 'buffer' ? body : body.toString('utf8'),
          headers,
          statusCode,
        });
      });
    }).on('error', rejectPromise);
  });
}

function buildStatusUrl(job) {
  const url = new URL(`${job.domain}/jobStatus/${job.user_id}/${job.job_id}`);
  url.searchParams.set('anonymousKey', job.anonymous_key);
  return url;
}

function parseJobStatus(html) {
  const match = html.match(/var job = (\{[\s\S]*?\});/);
  if (!match) {
    throw new Error('Could not parse Certora job status response.');
  }
  return JSON.parse(match[1]);
}

async function downloadReportBundle(job, status) {
  const tmp = mkdtempSync(join(tmpdir(), 'omegax-certora-'));
  const bundle = join(tmp, 'outputs.tar.gz');
  const url = new URL(status.zipOutputUrl || `${job.domain}/v1/domain/jobs/${job.job_id}/f/outputs`);
  if (!url.searchParams.has('anonymousKey')) {
    url.searchParams.set('anonymousKey', job.anonymous_key);
  }

  const response = await request(url, 'buffer');
  if (response.statusCode !== 200) {
    rmSync(tmp, { force: true, recursive: true });
    throw new Error(`Could not download Certora output bundle; status ${response.statusCode}.`);
  }

  await new Promise((resolvePromise, rejectPromise) => {
    const stream = createWriteStream(bundle);
    stream.on('finish', resolvePromise);
    stream.on('error', rejectPromise);
    stream.end(response.body);
  });

  return { bundle, tmp };
}

function extractJson(bundle, path) {
  const result = spawnSync('tar', ['-xOzf', bundle, path], { encoding: 'utf8' });
  if (result.status !== 0) {
    throw new Error(result.stderr.trim() || `Could not extract ${path}.`);
  }
  return JSON.parse(result.stdout);
}

function normalizeRuleResults(output) {
  if (!output || typeof output !== 'object' || Array.isArray(output)) {
    return [];
  }

  if (output.rules && typeof output.rules === 'object') {
    return Object.entries(output.rules);
  }

  return Object.entries(output).filter(([, value]) => typeof value === 'string');
}

async function main() {
  const job = readLatestJob();
  const statusUrl = buildStatusUrl(job);
  const response = await request(statusUrl);
  if (response.statusCode !== 200) {
    throw new Error(`Certora status query returned ${response.statusCode}.`);
  }

  const status = parseJobStatus(response.body);
  console.log(`[certora:solana:status] job ${status.jobId}: ${status.jobStatus}`);
  if (status.postTime) {
    console.log(`[certora:solana:status] submitted: ${status.postTime}`);
  }
  if (status.finishTime) {
    console.log(`[certora:solana:status] finished: ${status.finishTime}`);
  }
  if (job.output_url && showReportUrl) {
    console.log(`[certora:solana:status] report: ${job.output_url}`);
  } else if (job.output_url) {
    const redacted = new URL(job.output_url);
    if (redacted.searchParams.has('anonymousKey')) {
      redacted.searchParams.set('anonymousKey', '<redacted>');
    }
    console.log(`[certora:solana:status] report: ${redacted.toString()}`);
    console.log('[certora:solana:status] pass --show-report-url to print the local private report token.');
  }

  if (status.jobStatus !== 'SUCCEEDED') {
    process.exitCode = status.jobStatus === 'RUNNING' || status.jobStatus === 'QUEUED' ? 0 : 1;
    return;
  }

  const { bundle, tmp } = await downloadReportBundle(job, status);
  try {
    const output = extractJson(bundle, 'TarName/Reports/output.json');
    const results = normalizeRuleResults(output);
    if (results.length === 0) {
      console.log('[certora:solana:status] no rule results found in output bundle.');
      process.exitCode = 1;
      return;
    }

    const failing = [];
    for (const [rule, result] of results) {
      console.log(`[certora:solana:status] ${rule}: ${result}`);
      if (result !== 'VERIFIED') {
        failing.push(rule);
      }
    }

    if (failing.length > 0) {
      process.exitCode = 1;
    }
  } finally {
    rmSync(tmp, { force: true, recursive: true });
  }
}

main().catch((error) => {
  console.error(`[certora:solana:status] ${error.message}`);
  process.exit(1);
});
