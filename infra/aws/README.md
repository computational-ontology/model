# infra/aws - the E1 record on AWS (decision D24)

Account: the project's AWS account (new AWS experience, *Projects*): management account under the UniTo
institutional email, project `computational-ontology`, member account `806079021361`, home region
`ap-southeast-2` (Sydney). Kaggle remains the GPU compute (D6); AWS holds the **unamendable record**
(Table 1) and, later, the monthly refetch (EventBridge + Lambda) for the temporal axis (axiom 9).

- `e1-record.ps1` - creates the bucket with versioning + Object Lock (COMPLIANCE, 365 days), uploads
  the preamble snapshot (private; Constitute CC BY-NC 3.0), the hash-only manifests and the pilot draw.
  Executed 2026-09-16: bucket `nra-record-ap2`, 209 texts + 2 manifests + pilot, retention until 2027-09-16.
- `objectlock.json` - the default retention rule.

Why Object Lock in COMPLIANCE mode: the snapshot is the record as it stands; no principal - root
included - can delete or overwrite a locked version before retention expires. The only way to
"amend" the corpus is a new object version (a new inscription, thesis 5), which the bucket keeps
alongside the old one. Nothing canonical lives only here: hashes are in `data/` and on Zenodo (D5).

## Constraints of a project account (verified 2026-09-16)

- Sign in with `aws login --profile co --region ap-southeast-2` (AWS CLI >= 2.32). The region must be the
  project's home region; IAM Identity Center (`aws configure sso`) is not used.
- The AWS-managed SCP `RegionFloor` denies every region except the home region, `us-east-1` and
  `us-west-2` (hence Sydney, not Frankfurt as first planned). Activating "advanced features" does not lift it.
- CloudShell is denied by the same policy set; work from the laptop CLI.
- Docs: docs.aws.amazon.com/accounts/latest/reference/scps-and-rcps-for-projects.html,
  docs.aws.amazon.com/cli/latest/userguide/cli-configure-sign-in.html.

Never commit credentials; `aws login` caches short-lived credentials outside the repo.
