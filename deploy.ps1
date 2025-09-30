# FLUX Vercel Deployment Helper Script for Windows
Write-Host "🚀 Preparing FLUX for Vercel Deployment..." -ForegroundColor Green

# Check if we're in the right directory
if (!(Test-Path "frontend") -or !(Test-Path "api")) {
    Write-Host "❌ Error: Please run this script from the FLUX root directory" -ForegroundColor Red
    exit 1
}

# Create a clean deployment directory
Write-Host "📁 Creating deployment structure..." -ForegroundColor Cyan
if (Test-Path "deploy") {
    Remove-Item -Recurse -Force deploy
}
New-Item -ItemType Directory -Name "deploy" | Out-Null
Set-Location deploy

# Copy essential files
Write-Host "📋 Copying project files..." -ForegroundColor Cyan
Copy-Item -Recurse -Path "..\api" -Destination "api"
Copy-Item -Recurse -Path "..\frontend" -Destination "frontend"
Copy-Item -Path "..\vercel.json" -Destination "vercel.json"
Copy-Item -Path "..\README.md" -Destination "README.md"
Copy-Item -Path "..\.vercelignore" -Destination ".vercelignore"

# Create package.json for root level
Write-Host "🔧 Creating root package.json..." -ForegroundColor Cyan
$packageJson = @{
    name = "flux-multi-agent"
    version = "1.0.0"
    description = "FLUX Multi-Agent Collaboration System"
    main = "index.js"
    scripts = @{
        build = "cd frontend && npm run build"
        start = "cd frontend && npm start"
        dev = "cd frontend && npm run dev"
    }
    keywords = @("ai", "agents", "collaboration", "nextjs", "fastapi")
    author = "FLUX Team"
    license = "MIT"
} | ConvertTo-Json -Depth 3

$packageJson | Out-File -FilePath "package.json" -Encoding UTF8

# Create a simple index.html for root access
Write-Host "🌐 Creating root index.html..." -ForegroundColor Cyan
$indexHtml = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FLUX Multi-Agent System</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            text-align: center;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
            background: linear-gradient(45deg, #ff6b6b, #feca57);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .subtitle {
            font-size: 1.2rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }
        .btn {
            background: linear-gradient(45deg, #ff6b6b, #feca57);
            border: none;
            padding: 1rem 2rem;
            border-radius: 50px;
            color: white;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 4px 15px 0 rgba(236, 116, 149, 0.75);
        }
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px 0 rgba(236, 116, 149, 0.9);
        }
        .features {
            margin-top: 2rem;
            text-align: left;
            opacity: 0.8;
        }
        .features li {
            margin: 0.5rem 0;
        }
    </style>
    <script>
        // Auto-redirect after 3 seconds
        setTimeout(() => {
            window.location.href = '/frontend/';
        }, 3000);
    </script>
</head>
<body>
    <div class="container">
        <h1>🚀 FLUX</h1>
        <p class="subtitle">Multi-Agent Collaboration System</p>
        <p>Redirecting to the application...</p>
        <a href="/frontend/" class="btn">Enter FLUX</a>
        
        <div class="features">
            <p><strong>Features:</strong></p>
            <ul>
                <li>🤖 7 Specialized AI Agents</li>
                <li>💬 Real-time Collaboration</li>
                <li>🌐 Multi-Agent Communication</li>
                <li>⚡ Serverless Architecture</li>
            </ul>
        </div>
    </div>
</body>
</html>
"@

$indexHtml | Out-File -FilePath "index.html" -Encoding UTF8

Write-Host "✅ Deployment structure ready!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Yellow
Write-Host "1. Initialize git: git init" -ForegroundColor White
Write-Host "2. Add files: git add ." -ForegroundColor White
Write-Host "3. Commit: git commit -m 'FLUX deployment ready'" -ForegroundColor White
Write-Host "4. Create GitHub repo and push" -ForegroundColor White
Write-Host "5. Connect to Vercel and deploy" -ForegroundColor White
Write-Host ""
Write-Host "🌐 Project structure created in 'deploy' directory" -ForegroundColor Cyan
Write-Host "📁 Files ready for Vercel deployment" -ForegroundColor Green

# Show directory structure
Write-Host "`n📂 Directory Structure:" -ForegroundColor Cyan
Get-ChildItem -Recurse -Depth 2 | Select-Object Mode, Name, FullName | Format-Table -AutoSize

Write-Host "`n🎯 Ready to deploy to Vercel!" -ForegroundColor Green