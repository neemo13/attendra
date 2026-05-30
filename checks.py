import os
import sys

print("=== DIAGNOSTIC REPORT ===")
print("Current Working Directory:", os.getcwd())
print("\nSystem Path (sys.path):")
for path in sys.path[:3]: 
    print(f"  - {path}")

print("\nChecking Files:")
files_to_check = [
    "src/__init__.py",
    "src/database/__init__.py",
    "src/database/auth_queries.py",
    "src/screens/teacher_screen.py"
]

for f in files_to_check:
    exists = os.path.exists(f)
    print(f"  - {f}: {'✅ EXISTS' if exists else '❌ MISSING'}")