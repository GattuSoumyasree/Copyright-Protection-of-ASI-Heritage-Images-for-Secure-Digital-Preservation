import subprocess

# Files to run in sequence
scripts = [
    "embed.py",
    "extract.py",
    "evaluate.py",
    "apply_attacks_all.py",
    "extract_from_attacks_all.py",
    "evaluate_attacks_all.py"
]

for script in scripts:
    print(f"\n🔷 Running: {script}\n{'-'*60}")
    try:
        subprocess.run(["python", script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script}: Exit code {e.returncode}")
        break
    print(f"✅ Finished: {script}\n{'='*60}")
