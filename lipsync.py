import os
import subprocess
import sys
import time
import tkinter as tk
from tkinter import filedialog, messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WAV2LIP_DIR = os.path.join(BASE_DIR, "Wav2Lip")
VENV_PY = os.path.join(BASE_DIR, "venv", "Scripts", "python.exe")
CHECKPOINT = os.path.join(WAV2LIP_DIR, "checkpoints", "wav2lip_gan.pth")
RESULTS_DIR = os.path.join(WAV2LIP_DIR, "results")

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}


def pick_files():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    audio_path = filedialog.askopenfilename(
        title="Step 1 of 2 - Select the AUDIO file",
        filetypes=[("Audio files", "*.mp3 *.wav *.m4a *.aac *.ogg"), ("All files", "*.*")],
    )
    if not audio_path:
        return None, None
    root.update()

    face_path = filedialog.askopenfilename(
        title="Step 2 of 2 - Select the VIDEO or IMAGE of the face",
        filetypes=[
            ("Video/Image files", "*.mp4 *.mov *.avi *.mkv *.png *.jpg *.jpeg *.bmp *.webp"),
            ("All files", "*.*"),
        ],
    )
    root.destroy()
    if not face_path:
        return None, None

    return audio_path, face_path


def run_lipsync(audio_path, face_path):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    is_image = os.path.splitext(face_path)[1].lower() in IMAGE_EXTS
    stamp = time.strftime("%Y%m%d_%H%M%S")
    outfile = os.path.join(RESULTS_DIR, f"lipsync_{stamp}.mp4")

    env = os.environ.copy()
    extra_path = os.pathsep.join([
        os.path.join(BASE_DIR, "ffmpeg"),
        os.path.join(BASE_DIR, "venv", "Lib", "site-packages", "torch", "lib"),
        os.path.join(BASE_DIR, "venv", "Lib", "site-packages", "nvidia", "cudnn", "bin"),
        os.path.join(BASE_DIR, "venv", "Lib", "site-packages", "nvidia", "cublas", "bin"),
    ])
    env["PATH"] = extra_path + os.pathsep + env.get("PATH", "")
    env["CUDA_MODULE_LOADING"] = "LAZY"

    cmd = [
        VENV_PY, "inference.py",
        "--checkpoint_path", CHECKPOINT,
        "--face", face_path,
        "--audio", audio_path,
        "--outfile", outfile,
        "--wav2lip_batch_size", "32",
        "--out_height", "640",
    ]
    if is_image:
        cmd += ["--static", "True"]

    print("Running:", " ".join(f'"{c}"' if " " in c else c for c in cmd))
    print()
    result = subprocess.run(cmd, cwd=WAV2LIP_DIR, env=env)

    if result.returncode == 0 and os.path.exists(outfile):
        print(f"\nDone. Output saved to:\n{outfile}")
        try:
            os.startfile(RESULTS_DIR)
        except Exception:
            pass
        messagebox.showinfo("Lip Sync Complete", f"Saved to:\n{outfile}")
    else:
        print("\nLip sync failed. See the log above for details.")
        messagebox.showerror("Lip Sync Failed", "Something went wrong. Check the console output for details.")


def main():
    audio_path, face_path = pick_files()
    if not audio_path or not face_path:
        print("Cancelled - no files selected.")
        return
    run_lipsync(audio_path, face_path)


if __name__ == "__main__":
    main()
