import subprocess
import os

def get_output(cmd, cwd=None):
    try:
        return subprocess.check_output(cmd, shell=True, cwd=cwd, stderr=subprocess.DEVNULL).decode().strip()
    except:
        return None

parent_dir = os.getcwd()
submodule_dir = os.path.join(parent_dir, 'ai-agent-rules')

def verify_path(git_path):
    print(f"\nChecking path: {git_path}")
    commits = get_output(f'git log main --format="%H %s" -- {git_path}').split('\n')
    all_valid = True
    for line in commits:
        if not line: continue
        parts = line.split(' ')
        parent_h = parts[0]
        subject = ' '.join(parts[1:])
        sub_h = get_output(f'git rev-parse {parent_h}:{git_path}')
        if not sub_h: continue
        exists = get_output(f'git rev-parse --verify {sub_h}', cwd=submodule_dir)
        if exists:
            print(f"  VALID: {sub_h[:8]} at {parent_h[:8]}")
        else:
            print(f"  !!! MISSING !!!: {sub_h} at {parent_h} ({subject})")
            all_valid = False
    return all_valid

v1 = verify_path('ai-agent-rules')
v2 = verify_path('AI-Agent-Rules')

if v1 and v2:
    print("\nSUCCESS: All historical submodule pointers are valid.")
else:
    print("\nFAILURE: Some historical pointers are still broken.")
