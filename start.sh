#!/bin/bash

# IndexTTS2 One-Click Startup Script for Linux and macOS
# This script will install dependencies and launch the WebUI

set -e  # Exit on error

# Change to the directory where this script is located
cd "$(dirname "$0")"

echo ""
echo "================================================"
echo "  IndexTTS2 - One-Click Startup (Linux/macOS)"
echo "================================================"
echo ""
echo "[INFO] Working directory: $(pwd)"
echo ""

# Function to print colored output
print_info() {
    echo "[INFO] $1"
}

print_ok() {
    echo "[OK] $1"
}

print_error() {
    echo "[ERROR] $1"
}

print_warning() {
    echo "[WARNING] $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    echo "Please install Python 3.10+ from https://www.python.org/"
    exit 1
fi

print_ok "Python found"
python3 --version

# Check if Git is installed
if ! command -v git &> /dev/null; then
    print_error "Git is not installed"
    echo "Please install Git from https://git-scm.com/"
    exit 1
fi

print_ok "Git found"

# Check if Git LFS is installed
echo ""
print_info "Checking Git LFS setup..."
if ! command -v git-lfs &> /dev/null; then
    print_warning "Git LFS not found. Large files may not download correctly."
    echo "Install Git LFS from https://git-lfs.com/"
else
    print_ok "Git LFS found"
fi

# Pull Git LFS files
echo ""
print_info "Pulling Git LFS files..."
git lfs pull || print_warning "Failed to pull LFS files"

# Install uv if not present
echo ""
print_info "Checking uv package manager..."
if ! command -v uv &> /dev/null; then
    print_info "Installing uv package manager..."
    pip3 install -U uv || {
        print_error "Failed to install uv"
        echo "Try running: pip3 install -U uv"
        exit 1
    }
else
    print_ok "uv found"
fi

# Install dependencies
echo ""
print_info "Installing dependencies (this may take 5-10 minutes)..."
print_info "This downloads PyTorch, transformers, and other libraries..."
uv sync --all-extras || {
    print_error "Failed to install dependencies"
    echo "Try running manually: uv sync --all-extras"
    exit 1
}

# Check if models exist
echo ""
print_info "Checking for model files..."
if [ ! -f "checkpoints/config.yaml" ]; then
    print_warning "Model files not found!"
    echo ""
    print_info "Downloading IndexTTS-2 models (requires internet, ~5GB)..."
    print_info "This may take 10-30 minutes depending on your connection..."
    echo ""
    
    if uv tool install "huggingface-hub[cli,hf_xet]"; then
        if hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints; then
            print_ok "Models downloaded successfully"
        else
            print_warning "Failed to download models from Hugging Face"
            echo "Try downloading manually: https://huggingface.co/IndexTeam/IndexTTS-2"
            echo "Or use ModelScope: https://modelscope.cn/models/IndexTeam/IndexTTS-2"
            echo ""
        fi
    else
        print_warning "Failed to install huggingface-hub CLI"
        echo "Try downloading models manually from:"
        echo "  https://huggingface.co/IndexTeam/IndexTTS-2"
        echo ""
    fi
else
    print_ok "Model files found"
fi

# Check GPU
echo ""
print_info "Checking GPU support..."
if uv run tools/gpu_check.py; then
    print_ok "GPU check completed"
else
    print_warning "GPU check failed. System will use CPU (slower inference)"
fi

# Launch WebUI
echo ""
print_info "Starting IndexTTS2 WebUI..."
print_info "Opening http://127.0.0.1:7860 in your browser..."
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uv run webui.py
