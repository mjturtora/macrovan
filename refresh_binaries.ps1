# Trigger the build
gh workflow run build-executables.yml --ref dev

# Wait for completion (Select the top run if prompted)
gh run watch

# Download the results
gh run download