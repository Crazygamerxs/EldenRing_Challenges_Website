#!/usr/bin/env bash
# Debug build script for Render.com - Elden Ring Challenges Website
# This script will help identify the exact file structure issue

set -o errexit  # Exit on error

echo "🚀 Starting DEBUG Render deployment build..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd mybackend
pip install -r requirements.txt

# Move to frontend and debug
echo "⚛️ Debugging React frontend structure..."
cd ../myfrontend

# EXTENSIVE DEBUGGING - Check file structure
echo "📁 === DEBUGGING FILE STRUCTURE ==="
echo "Current directory: $(pwd)"
echo ""

echo "📂 Contents of src/:"
ls -la src/ || echo "src/ directory not found!"
echo ""

echo "📂 Contents of src/components/:"
if [ -d "src/components" ]; then
    ls -la src/components/
else
    echo "❌ src/components/ directory not found!"
fi
echo ""

echo "📂 Looking for Login directory:"
if [ -d "src/components/Login" ]; then
    echo "✅ Login directory found!"
    echo "Contents of src/components/Login/:"
    ls -la src/components/Login/
else
    echo "❌ src/components/Login/ directory not found!"
    echo "Searching for Login files anywhere..."
    find src/ -name "*Login*" -type f 2>/dev/null || echo "No Login files found"
fi
echo ""

echo "📂 Contents of src/ (recursive search for structure):"
find src/ -type f -name "*.js" | head -20
echo ""

echo "🔍 Searching for import statements mentioning Login:"
grep -r "import.*Login" src/ || echo "No Login imports found in search"
echo ""

echo "🔍 Checking App.js content (if exists):"
if [ -f "src/App.js" ]; then
    echo "✅ App.js found, showing imports:"
    head -30 src/App.js | grep -E "(import|Login)" || echo "No Login imports in App.js head"
else
    echo "❌ src/App.js not found!"
fi
echo ""

echo "📂 Complete directory structure (first 30 lines):"
find src/ -type f | head -30
echo ""

# Check package.json
echo "📋 Checking package.json:"
if [ -f "package.json" ]; then
    echo "✅ package.json found"
    echo "Main entry point:"
    cat package.json | grep -E "(main|homepage)" || echo "No main/homepage found"
else
    echo "❌ package.json not found!"
fi

# Install and attempt build with more verbose output
echo "📦 Installing dependencies..."
npm install --only=production

echo "🔨 Attempting build with verbose output..."
echo "Build will fail, but we'll see exactly where..."

# Try to build and capture the error
npm run build 2>&1 | tee build_output.log || {
    echo ""
    echo "🚨 BUILD FAILED - Analyzing error..."
    echo ""
    echo "Last 10 lines of build output:"
    tail -10 build_output.log
    echo ""
    echo "Searching for specific error in build log:"
    grep -A 5 -B 5 "Can't resolve.*Login" build_output.log || echo "Login error not found in expected format"
    echo ""
    
    # Exit with error but after showing debug info
    echo "💥 Build failed as expected - debug info collected above"
    exit 1
}

echo "✅ If we reach here, build succeeded unexpectedly!"