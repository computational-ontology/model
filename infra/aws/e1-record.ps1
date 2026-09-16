# E1 - Record on AWS: the frozen preamble snapshot in an S3 bucket with versioning + Object Lock (decision D24).
# Run from the repo root on Luis's laptop, one block at a time, with the `co` profile of the computational-ontology
# project (AWS Projects member account 806079021361, role AccountFullAccessRole) - never root.
# Placement: Table 1, unamendable column; theses 5-7 (a new inscription is a new object version, never an overwrite).
# Prerequisites: AWS CLI v2 >= 2.32 (winget install Amazon.AWSCLI), then once per 12-hour session:
#     aws login --profile co --region ap-southeast-2
#   The login region is the project's HOME region (AWS Settings > project > Additional info: Sydney); with any other
#   region the sign-in page answers "Something went wrong". Resources must stay in the home region too: the
#   AWS-managed SCP "RegionFloor" denies every region except the home one, us-east-1 and us-west-2, and
#   CloudShell is denied outright (verified 2026-09-16; D24 amended accordingly).
# Docs consulted: docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-configure.html,
#                 docs.aws.amazon.com/cli/latest/userguide/cli-configure-sign-in.html,
#                 docs.aws.amazon.com/accounts/latest/reference/scps-and-rcps-for-projects.html,
#                 github.com/aws/agent-toolkit-for-aws/blob/main/setup-instructions/setup.md
# Executed 2026-09-16 (blocks 1-4); kept as the reproducible record of how the bucket was made.

$Profile = "co"
$Region  = "ap-southeast-2"                    # Sydney - the project's home region (see header)
$Bucket  = "nra-record-ap2"                    # globally unique; if taken, append a suffix and update this line

# 1 - bucket with Object Lock (can only be enabled at creation); versioning is required by Object Lock
aws s3api create-bucket --bucket $Bucket --region $Region --create-bucket-configuration LocationConstraint=$Region --object-lock-enabled-for-bucket --profile $Profile
aws s3api put-bucket-versioning --bucket $Bucket --region $Region --versioning-configuration Status=Enabled --profile $Profile
aws s3api put-public-access-block --bucket $Bucket --region $Region --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true --profile $Profile

# 2 - default retention: COMPLIANCE, 365 days; no principal, root included, can delete or shorten a locked version before it expires
aws s3api put-object-lock-configuration --bucket $Bucket --region $Region --object-lock-configuration file://infra/aws/objectlock.json --profile $Profile
aws s3api put-bucket-tagging --bucket $Bucket --region $Region --tagging 'TagSet=[{Key=project,Value=computational-ontology},{Key=stratum,Value=E1-record},{Key=licence,Value=CC-BY-NC-3.0-Constitute-private}]' --profile $Profile

# 3 - the record: texts (private, never public) + hash-only manifests + the pilot draw
aws s3 cp data/snapshot_preamble s3://$Bucket/snapshot_preamble/ --recursive --region $Region --profile $Profile
aws s3 cp data/snapshot_manifest_preamble_en.json s3://$Bucket/manifests/ --region $Region --profile $Profile
aws s3 cp data/snapshot_manifest_preamble_es.json s3://$Bucket/manifests/ --region $Region --profile $Profile
aws s3 cp data/splits/pilot_preamble_100.json s3://$Bucket/splits/ --region $Region --profile $Profile

# 4 - verify: 209 texts, every object locked, nothing public
aws s3 ls s3://$Bucket/snapshot_preamble/ --region $Region --profile $Profile | Measure-Object -Line
aws s3api get-object-lock-configuration --bucket $Bucket --region $Region --profile $Profile
aws s3api get-object-retention --bucket $Bucket --key snapshot_preamble/Spain_2011__1__es.txt --region $Region --profile $Profile
aws s3api get-public-access-block --bucket $Bucket --region $Region --profile $Profile
