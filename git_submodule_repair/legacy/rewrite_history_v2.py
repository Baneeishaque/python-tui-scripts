import subprocess
import os

def get_output(cmd, cwd=None):
    return subprocess.check_output(cmd, shell=True, cwd=cwd).decode().strip()

# Base commit (everything before this is kept as is)
base = "2d061d0d1112f625f0e15d58af3e0ec3beaefde5"

# Commits to rewrite (in chronological order)
origin_commits = [
    "cdfeb1e0b38183c8e4741aca064650188650fe9e", # Rename
    "d9248571122546fe631def71dfa3427200ad26bd", # Atom Feed
    "971754bd4d63b3714a8af71db487aae5d6e1a0a3", # cSpell
    "fe25868dd5660edf28f2ebb78900af13b34332c5", # Rclone Opt
    "aa442ff1b57ac3b67e4a18e4aa1db7ab4370c4fa", # Refine Git
    "b1ab37e525901af4ca3067d5d75f339d3c5dfa2f", # Industrial Rebase
    "1e459b820a156af66e8cc6e5a2188d9d8c71be0f"  # Refinements
]

# Specifically mapped submodule hashes
# Note: Hash keys must match origin_commits exactly
submodule_map = {
    "cdfeb1e0b38183c8e4741aca064650188650fe9e": "e6d8efa64930b96bb848b7d5dd8e6b29b5449c59",
    "d9248571122546fe631def71dfa3427200ad26bd": "14d71ae4d332521eb4b3bca105250751976aa892",
    "fe25868dd5660edf28f2ebb78900af13b34332c5": "e5602d3b329ab14c8c977a1307d4068605520c95"
}

parent = base
new_head = base

for old_h in origin_commits:
    print(f"Processing {old_h[:8]}...")
    
    # 1. Start with the original tree of this commit
    # We use rev-parse to ensure the tree exists
    tree = get_output(f"git rev-parse {old_h}^{{tree}}")
    
    # 2. Update the tree's submodule entry
    target_subhash = submodule_map.get(old_h)
    
    # If not explicitly mapped, inherit from the new parent's submodule state
    if not target_subhash:
        target_subhash = get_output(f"git rev-parse {parent}:ai-agent-rules")
        
    # Read the original commit's full tree into index, then override the submodule entry
    subprocess.check_call(f"git read-tree {old_h}", shell=True)
    subprocess.check_call(f"git update-index --cacheinfo 160000,{target_subhash},ai-agent-rules", shell=True)
    tree = get_output("git write-tree")

    # 3. Create the new commit with identical metadata
    msg = get_output(f"git log -1 --format=%B {old_h}")
    author_name = get_output(f"git log -1 --format=%an {old_h}")
    author_email = get_output(f"git log -1 --format=%ae {old_h}")
    author_date = get_output(f"git log -1 --format=%ad {old_h}")
    committer_date = get_output(f"git log -1 --format=%cd {old_h}")
    
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = author_name
    env["GIT_AUTHOR_EMAIL"] = author_email
    env["GIT_AUTHOR_DATE"] = author_date
    env["GIT_COMMITTER_DATE"] = committer_date
    env["GIT_COMMITTER_NAME"] = author_name # Preserve committer name too
    env["GIT_COMMITTER_EMAIL"] = author_email
    
    new_h = subprocess.check_output(
        f"git commit-tree {tree} -p {parent}",
        shell=True,
        input=msg.encode(),
        env=env
    ).decode().strip()
    
    print(f"  Rewritten to {new_h[:8]} (submodule: {target_subhash[:8]})")
    parent = new_h
    new_head = new_h

# Reset main to the new head
subprocess.check_call(f"git reset --hard {new_head}", shell=True)
print(f"\nSUCCESS: main reset to {new_head}")
