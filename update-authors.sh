#! /bin/sh

set -e

# Keep authors in the order of appearance and use awk to filter out dupes
git log --format='- %aN <%aE>' --reverse | awk '!x[$0]++' > AUTHORS
