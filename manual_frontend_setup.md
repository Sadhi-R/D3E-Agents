# Manual Frontend Setup Guide

If you're having issues with npm, here's how to set up the frontend manually:

## Option 1: Fix npm first (Recommended)

### Windows
1. Download Node.js from https://nodejs.org/
2. Choose "LTS" version (includes npm)
3. Run installer as Administrator
4. Restart your terminal/command prompt
5. Verify: `node -v` and `npm -v`

### macOS
```bash
# Using Homebrew (recommended)
brew uninstall node
brew install node

# Or download from nodejs.org
```

### Linux
```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify
node -v
npm -v
```

## Option 2: Use pnpm instead

```bash
# Install pnpm
curl -fsSL https://get.pnpm.io/install.sh | sh

# Restart terminal, then:
cd frontend
pnpm install
pnpm dev
```

## Option 3: Use yarn

```bash
# Install yarn globally (once npm is working)
npm install -g yarn

# Or install yarn via other methods:
# Windows: choco install yarn
# macOS: brew install yarn

cd frontend
yarn install
yarn dev
```

## Option 4: Backend-only mode

If you can't get the frontend working immediately, you can still use the backend API:

```bash
# Start just the backend
python start_backend.py

# Access API documentation at:
# http://localhost:8000/docs
```

The backend provides a full REST API that you can use with tools like:
- Postman
- curl commands
- Any HTTP client

## Troubleshooting npm

### Check Node.js installation
```bash
node -v  # Should show v22.17.1
which node  # Should show path to node
```

### Check npm specifically
```bash
# Try to find npm
which npm
where npm  # Windows

# Check if npm is in the right place
ls -la /usr/local/bin/npm  # macOS/Linux
dir "C:\Program Files\nodejs\npm.cmd"  # Windows
```

### Reinstall npm only
```bash
# If node works but npm doesn't
curl -L https://www.npmjs.com/install.sh | sh
```

### Environment variables (Windows)
Make sure these are in your PATH:
- `C:\Program Files\nodejs\`
- `%APPDATA%\npm`

## Quick Test

Once npm is working, test with:
```bash
npm --version
cd frontend
npm install
npm run dev
```

The frontend should start on http://localhost:3000

## Need Help?

If you're still having issues:
1. Share your operating system
2. Share the output of `node -v` and `npm -v`
3. Share any error messages you're seeing

The D3E Agent backend will work fine without the frontend, but the web interface provides a much better user experience!
