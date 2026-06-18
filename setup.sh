#!/bin/bash

# =============================================================================
# ATLAS CODING AGENT - ONE-CLICK INSTALLER
# =============================================================================
# Version: 1.0.0
# Description: Installer for Termux (Android) and Ubuntu/Debian (Linux)
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
BOLD='\033[1m'

log() { echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"; }
success() { echo -e "${GREEN}✓${NC} $1"; }
error() { echo -e "${RED}✗${NC} $1"; exit 1; }
warning() { echo -e "${YELLOW}⚠${NC} $1"; }

print_banner() {
    clear
    echo -e "${BLUE}"
    cat << "EOF"
    ___  _________   ___   ____ 
   / _ |/_  __/ /   / _ | / __/ 
  / __ | / / / /__ / __ |_\ \   
 /_/ |_|/_/ /____//_/ |_/___/   
                                
    Atlas Coding Agent v1.0.0
    One-Click Setup System
EOF
    echo -e "${NC}"
}

check_env() {
    log "Detecting environment..."
    if [[ -n "$TERMUX_VERSION" ]] || [[ -d "/data/data/com.termux" ]]; then
        ENV_TYPE="termux"
        PKG_MGR="pkg"
    elif [[ -f /etc/debian_version ]]; then
        ENV_TYPE="ubuntu"
        PKG_MGR="sudo apt-get"
    else
        warning "Unrecognized environment. Assuming generic Linux (Debian-based)."
        ENV_TYPE="linux"
        PKG_MGR="sudo apt-get"
    fi
    success "Environment: $ENV_TYPE"
}

install_dependencies() {
    log "Installing system dependencies..."
    if [[ "$ENV_TYPE" == "termux" ]]; then
        pkg update -y
        pkg install -y python python-pip git binutils
    else
        $PKG_MGR update -y
        $PKG_MGR install -y python3 python3-pip python3-venv git
    fi
    success "System dependencies installed."
}

setup_venv() {
    log "Setting up virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    success "Virtual environment ready."
}

setup_cli() {
    log "Configuring Atlas CLI..."
    # Create a wrapper script in ~/.local/bin or similar
    BIN_DIR="$HOME/.local/bin"
    mkdir -p "$BIN_DIR"
    
    cat > "$BIN_DIR/atlas" << EOF
#!/bin/bash
source $(pwd)/venv/bin/activate
python3 $(pwd)/main.py "\$@"
EOF
    chmod +x "$BIN_DIR/atlas"
    
    # Suggest adding to PATH if not present
    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        warning "Add $BIN_DIR to your PATH to use 'atlas' command globally."
        echo "export PATH=\"\$PATH:$BIN_DIR\"" >> ~/.bashrc
        echo "export PATH=\"\$PATH:$BIN_DIR\"" >> ~/.zshrc
    fi
    success "Atlas CLI configured."
}

main() {
    print_banner
    check_env
    install_dependencies
    setup_venv
    setup_cli
    echo -e "\n${GREEN}${BOLD}Atlas Coding Agent setup complete!${NC}"
    echo -e "Try running: ${BOLD}atlas --help${NC}"
}

main "$@"
