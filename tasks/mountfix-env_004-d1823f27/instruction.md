# Prepare a Git Source Release

The repository `/home/circleci/widget-service` contains the `widget-service` project at version `1.4.2`.
Prepare a source release under `/home/circleci/releases` using the committed Git repository state.

Required end state:

1. In `/home/circleci/widget-service`, create or update `.gitattributes` so that these paths are excluded from Git archives with the `export-ignore` attribute:
   - `tests/`
   - `docs/draft.md`
   - `.env.sample`
   - `.ci/`
   - `build/`

2. Make the `.gitattributes` change part of the repository history before creating the archive.

3. Create a gzip-compressed Git archive at:

   `/home/circleci/releases/widget-service-1.4.2.tar.gz`

   The archive must be produced from the commit that contains the `.gitattributes` rules, must use the top-level prefix `widget-service-1.4.2/`, and must not contain any of the excluded paths.

4. Create `/home/circleci/releases/widget-service-1.4.2.manifest.json`.
   It must be a single minified JSON object followed by one trailing newline, with keys in exactly this order:

   `package`, `version`, `git_commit`, `archive`, `sha256`, `size_bytes`, `entries`

   Field requirements:
   - `package`: `widget-service`
   - `version`: `1.4.2`
   - `git_commit`: the full 40-character commit hash used to create the archive
   - `archive`: `widget-service-1.4.2.tar.gz`
   - `sha256`: lowercase hex SHA-256 digest of the archive file
   - `size_bytes`: archive size in bytes as a JSON number
   - `entries`: a lexicographically sorted array of every regular file path inside the archive

Do not copy the excluded paths into the release archive by hand. The release should reflect Git's archive export rules.
