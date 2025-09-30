#!/bin/bash
# FLUX Vercel Deployment Helper Script

echo "🚀 Preparing FLUX for Vercel Deployment..."

# Create a clean deployment directory
echo "📁 Creating deployment structure..."
mkdir -p deploy
cd deploy

# Copy essential files
echo "📋 Copying project files..."
cp -r ../api .
cp -r ../frontend .
cp ../vercel.json .
cp ../README.md .
cp ../.vercelignore .

# Update API to be compatible with Vercel
echo "🔧 Optimizing API for serverless..."

# Create a simple index.html for root access  
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>FLUX Multi-Agent System</title>
    <meta http-equiv="refresh" content="0; url=/frontend/">
</head>
<body>
    <h1>Redirecting to FLUX...</h1>
    <p>If you are not redirected automatically, <a href="/frontend/">click here</a>.</p>
</body>
</html>
EOF

echo "✅ Deployment structure ready!"
echo ""
echo "📋 Next steps:"
echo "1. Initialize git in the deploy directory: cd deploy && git init"
echo "2. Add files: git add ."
echo "3. Commit: git commit -m 'Initial deployment'"
echo "4. Push to GitHub and connect to Vercel"
echo ""
echo "🌐 Your project structure:"
tree -L 2 2>/dev/null || find . -maxdepth 2 -type d