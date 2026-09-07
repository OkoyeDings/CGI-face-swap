"""
One-time setup for Deep-Live-Cam-Cuda (face swap + lip sync).
Run this via setup.bat (double-click) on a fresh machine.

What it does:
  1. Checks for an NVIDIA GPU + driver (warns if missing, does not fail).
  2. Creates a local venv/ folder.
  3. Installs all Python dependencies (face swap + Wav2Lip lip sync) into it.
  4. Verifies the install by importing the key packages.

Model weights (models/, Wav2Lip/checkpoints/) and ffmpeg are expected to
already be present in this folder (they ship inside the zip since they
can't be pip-installed).
"""
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(BASE_DIR, "venv")
VENV_PY = os.path.join(VENV_DIR, "Scripts", "python.exe")
REQUIREMENTS = os.path.join(BASE_DIR, "requirements_full.txt")


def banner(text):
    print()
    print("=" * 60)
    print(text)
    print("=" * 60)


def check_gpu():
    banner("Checking for NVIDIA GPU / driver")
    try:
        result = subprocess.run(["nvidia-smi"], capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "Driver Version" in line or "GeForce" in line or "NVIDIA" in line:
                    print(line.strip())
            print("GPU detected. CUDA acceleration will be used.")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    print("WARNING: No NVIDIA GPU / driver detected (nvidia-smi not found or failed).")
    print("The software will still install, but will run on CPU only (very slow),")
    print("or fail to use --execution-provider cuda.")
    print("If this machine has an NVIDIA GPU, install the driver from:")
    print("  https://www.nvidia.com/Download/index.aspx")
    return False


def create_venv():
    banner("Setting up Python virtual environment")
    if os.path.exists(VENV_PY):
        print(f"venv already exists at {VENV_DIR}, skipping creation.")
        return
    print(f"Creating venv at {VENV_DIR} using {sys.executable}")
    subprocess.run([sys.executable, "-m", "venv", VENV_DIR], check=True)


def install_requirements():
    banner("Installing Python dependencies (this can take a while)")
    subprocess.run([VENV_PY, "-m", "pip", "install", "--upgrade", "pip"], check=True)

    cmd = [
        VENV_PY, "-m", "pip", "install",
        "--timeout", "120", "--retries", "10",
        "-r", REQUIREMENTS,
    ]
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print()
        print("WARNING: Some packages failed to install (likely a network issue")
        print("reaching download.pytorch.org). Retrying with a plain CPU-only")
        print("torch/torchvision as a fallback so the rest of the app still works...")
        subprocess.run([VENV_PY, "-m", "pip", "install", "--timeout", "120", "--retries", "10",
                         "torch", "torchvision"])
        subprocess.run([VENV_PY, "-m", "pip", "install", "--timeout", "120", "--retries", "10",
                         "-r", REQUIREMENTS])


def verify():
    banner("Verifying installation")
    check_script = (
        "import importlib, sys\n"
        "mods = ['torch','cv2','numpy','insightface','onnxruntime','librosa','batch_face','customtkinter']\n"
        "ok = True\n"
        "for m in mods:\n"
        "    try:\n"
        "        importlib.import_module(m)\n"
        "        print(f'  OK  {m}')\n"
        "    except Exception as e:\n"
        "        print(f'  FAIL {m}: {e}')\n"
        "        ok = False\n"
        "import torch\n"
        "print(f'  torch {torch.__version__}, CUDA available: {torch.cuda.is_available()}')\n"
        "sys.exit(0 if ok else 1)\n"
    )
    result = subprocess.run([VENV_PY, "-c", check_script])
    return result.returncode == 0


def main():
    check_gpu()
    create_venv()
    install_requirements()
    ok = verify()

    banner("Setup complete" if ok else "Setup finished with warnings")
    print("To run the app, double-click:  start_portable_nvidia.bat")
    print("  [1] Face Swap")
    print("  [2] Lip Sync")
    if not ok:
        print()
        print("Some packages failed to import - check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
