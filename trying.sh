git fetch --all

git reset --hard

for remote_branch in $(git branch -r | grep -v 'HEAD' | awk -F/ '{print $NF}'); do
    local_branch=${remote_branch}
    git checkout -b "${local_branch}" "origin/${remote_branch}"
    git pull --all
done

git checkout main