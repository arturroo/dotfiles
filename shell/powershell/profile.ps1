# ==============================================================================
# Copyright (c) 2026 Artur Fejklowicz
# SPDX-License-Identifier: Apache-2.0
# Author: Artur Fejklowicz | Version: 1.0.0 | Updated: 2026-10-14
# PowerShell Profile - Personal Developer Setup
# Compatible with PowerShell 7+ & Windows PowerShell 5.1
# ==============================================================================

# --- Console & Encoding Settings ---
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# --- Oh-My-Posh Prompt Initialization ---
# Active Theme: froczh
if (Get-Command oh-my-posh -ErrorAction SilentlyContinue) {
    oh-my-posh init pwsh --config 'froczh' | Invoke-Expression
}

# Alternate Themes for quick testing:
# oh-my-posh init pwsh --config 'cert' | Invoke-Expression
# oh-my-posh init pwsh --config 'velvet' | Invoke-Expression
# oh-my-posh init pwsh --config 'catppuccin_mocha' | Invoke-Expression
# oh-my-posh init pwsh --config 'powerlevel10k_rainbow' | Invoke-Expression
# oh-my-posh init pwsh --config 'powerlevel10k_lean' | Invoke-Expression

# --- Helpful Aliases & Functions ---
# Directory listing
function ll { Get-ChildItem -Path $args -Force }

# Git shortcuts
function gs { git status }
function gl { git log --oneline -n 15 }
function gp { git push }

# Python & UV helpers
function venv-activate {
    if (Test-Path ".\.venv\Scripts\Activate.ps1") {
        & ".\.venv\Scripts\Activate.ps1"
    } else {
        Write-Warning "No .venv found in current directory."
    }
}
