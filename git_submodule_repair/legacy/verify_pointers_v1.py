import subprocess
import os

def get_output(cmd, cwd=None):
    try:
        return subprocess.check_output(cmd, shell=True, cwd=cwd, stderr=subprocess.DEVNULL).decode().strip()
    except:
        return None

# Get all commits on main that affected ai-agent-rules
commits = get_output('git log main --format="%H %s" -- ai-agent-rules').split('\n')

all_valid = True
parent_dir = os.getcwd()
submodule_dir = os.path.join(parent_dir, 'ai-agent-rules')

for line in commits:
    if not line: continue
    parts = line.split(' ')
    parent_h = parts[0]
    subject = ' '.join(parts[1:])
    
    # Get the submodule hash referenced by this parent commit
    sub_h = get_output(f'git rev-parse {parent_h}:ai-agent-rules')
    
    if not sub_h:
        print(f"ERROR: Could not get subhash for {parent_h}")
        all_valid = False
        continue
        
    # Check if this sub_h exists in the submodule
    exists = get_output(f'git rev-parse --verify {sub_h}', cwd=submodule_dir)
    
    if exists:
        print(f"VALID: {sub_h[:8]} in parent {parent_h[:8]} ({subject})")
    else:
        print(f"!!! MISSING !!!: {sub_h} in parent {parent_h} ({subject})")
        all_valid = False

if all_valid:
    print("\nSUCCESS: All submodule pointers on 'main' are valid.")
else:
    print("\nFAILURE: Some submodule pointers are still broken.")
