import subprocess

def get_output(cmd):
    return subprocess.check_output(cmd, shell=True).decode().strip()

missing_hashes = [
    "b6040f173bcdcc5f75d130271e8d28e39d3a0a19",
    "c2787c95a9d92149633f6f50fec90475913ddc23",
    "c7a3404ca4a97b72bed1dde376fcd6355cb0b72a"
]

parent_commits = get_output('git log --all --pretty=format:"%H %s"').split('\n')

for parent in parent_commits:
    h = parent.split(' ')[0]
    subject = ' '.join(parent.split(' ')[1:])
    try:
        sub_h = get_output(f'git rev-parse {h}:ai-agent-rules')
        if sub_h in missing_hashes:
            print(f"MATCH: Parent {h} ({subject}) -> Submodule {sub_h}")
    except:
        continue
