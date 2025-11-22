# Helper script to run Gemini CLI with environment variables loaded from .env
# Usage: .\run-gemini.ps1 [gemini-arguments]

# Load .env file if it exists
if (Test-Path .env) {
    Write-Host "Loading environment variables from .env..." -ForegroundColor Cyan
    Get-Content .env | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            # Remove quotes if present
            $value = $value -replace '^["'']|["'']$', ''
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
            Write-Host "  Loaded: $name" -ForegroundColor Gray
        }
    }
} else {
    Write-Host "Warning: .env file not found" -ForegroundColor Yellow
}

# Check if GEMINI_API_KEY is set
if (-not $env:GEMINI_API_KEY) {
    Write-Host "Error: GEMINI_API_KEY not set. Please set it in .env or as an environment variable." -ForegroundColor Red
    exit 1
}

# Run Gemini CLI with all arguments passed through
Write-Host "Running Gemini CLI..." -ForegroundColor Cyan
Write-Host ""

# Pass all arguments to gemini
& gemini $args

