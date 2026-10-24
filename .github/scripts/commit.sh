#!/usr/bin/env bash
# commit + push with pull-rebase retry (several writers share main)
set -e
git config user.name "prop-lab-bot"; git config user.email "prop-lab-bot@users.noreply.github.com"
git add -A "$@"
git diff --cached --quiet && { echo "nothing to commit"; exit 0; }
git commit -m "${COMMIT_MSG:-bot: update}"
for i in 1 2 3 4 5; do git pull --rebase -X theirs origin main && git push origin HEAD:main && exit 0; sleep $((i*5)); done
echo "push failed"; exit 1
