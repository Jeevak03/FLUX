# 🚀 FLUX - Vercel Deployment Guide

This guide will help you deploy your FLUX multi-agent collaboration system to Vercel.

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your FLUX code should be in a GitHub repository
3. **Groq API Key**: Get your API key from [console.groq.com](https://console.groq.com)

## 🔧 Deployment Steps

### 1. Prepare Your Environment

Make sure you have all the necessary files:
- ✅ `vercel.json` - Vercel configuration
- ✅ `api/index.py` - Serverless API handler
- ✅ `api/requirements.txt` - Python dependencies
- ✅ `.vercelignore` - Files to ignore during deployment

### 2. Connect to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **"New Project"**
3. Import your GitHub repository containing FLUX
4. Select the repository and click **"Import"**

### 3. Configure Project Settings

When importing, Vercel will detect it's a Next.js project. Configure these settings:

**Framework Preset**: `Next.js`
**Root Directory**: `frontend`
**Build Command**: `npm run build`
**Output Directory**: Leave default (`.next`)

### 4. Set Environment Variables

In your Vercel project dashboard:

1. Go to **Settings** → **Environment Variables**
2. Add the following variables:

```
GROQ_API_KEY = your_groq_api_key_here
NODE_ENV = production
```

### 5. Deploy

1. Click **"Deploy"**
2. Wait for the build to complete (usually 2-3 minutes)
3. Once deployed, you'll get a live URL like `https://your-project.vercel.app`

## 🔄 How It Works

### Architecture Overview

```
Frontend (Next.js)     →     Serverless API (Python)     →     Groq AI
     ↓                            ↓                             ↓
• React Components         • FastAPI Handler            • Agent Responses
• WebSocket + REST         • Agent Logic                • AI Processing
• User Interface          • Message Routing             • Natural Language
```

### Key Components

1. **Frontend** (`frontend/`)
   - Next.js application with React components
   - Hybrid WebSocket + REST API communication
   - Automatic fallback for serverless limitations

2. **Serverless API** (`api/`)
   - Python FastAPI handler optimized for Vercel
   - RESTful endpoints for chat functionality
   - Limited WebSocket support (serverless constraints)

3. **Agent System**
   - 7 specialized AI agents (Sara, Marc, Alex, Jess, Dave, Emma, Robt)
   - Direct agent routing and multi-agent collaboration
   - Groq AI integration for responses

## 🌐 Testing Your Deployment

### 1. Basic Functionality
- Visit your Vercel URL
- Try sending messages like "Hi Marc" or "Hello Everyone"
- Verify agents respond correctly

### 2. API Endpoints
Test these endpoints directly:
- `https://your-project.vercel.app/api/health` - Health check
- `https://your-project.vercel.app/api/agents` - List agents
- `https://your-project.vercel.app/api/chat` - Send messages (POST)

### 3. Expected Behavior
- **Single Agent**: "Hi Sara" → Only Sara responds
- **Multi-Agent**: "Hi Everyone" → All agents respond
- **Fallback**: If WebSocket fails, REST API takes over automatically

## 🔧 Troubleshooting

### Common Issues

**1. "GROQ_API_KEY not found"**
- Ensure you've added the environment variable in Vercel settings
- Redeploy after adding environment variables

**2. "Build failed" errors**
- Check the build logs in Vercel dashboard
- Ensure all dependencies are in `package.json` and `requirements.txt`

**3. "API timeout" errors**
- Vercel functions have a 10-second timeout limit
- Large responses may need to be streamed or paginated

**4. WebSocket connection issues**
- WebSockets have limited support in serverless environments
- The system automatically falls back to REST API
- This is normal behavior for Vercel deployments

### Performance Optimization

1. **Cold Starts**: First request may take 2-3 seconds (normal for serverless)
2. **Response Time**: Subsequent requests are typically under 1 second
3. **Caching**: Vercel automatically caches static assets
4. **Global CDN**: Your app is served from edge locations worldwide

## 🔒 Security Considerations

### Environment Variables
- Never commit `.env` files to your repository
- Use Vercel's environment variable system
- Groq API key is securely stored and encrypted

### CORS Configuration
- The API allows all origins by default for development
- Consider restricting origins for production use
- Update CORS settings in `api/index.py` if needed

### Rate Limiting
- Implement rate limiting for production use
- Consider using Vercel's edge functions for better performance
- Monitor Groq API usage to avoid quota limits

## 📊 Monitoring and Analytics

### Vercel Dashboard
- **Functions**: Monitor API performance and errors
- **Analytics**: Track page views and user engagement
- **Logs**: Debug issues with real-time logging

### Usage Metrics
- Track agent response times
- Monitor Groq API usage and costs
- Analyze user interaction patterns

## 🚀 Going to Production

### Domain Setup
1. Add your custom domain in Vercel settings
2. Configure DNS records as instructed
3. Vercel automatically handles SSL certificates

### Performance Tuning
- Enable Vercel Analytics for detailed metrics
- Use Vercel's Image Optimization for better performance
- Consider upgrading to Pro plan for better limits

### Scaling Considerations
- Vercel automatically scales based on traffic
- Monitor function execution time and memory usage
- Consider edge functions for better global performance

## 🔄 Updates and Maintenance

### Continuous Deployment
- Push to your main branch to trigger automatic deployments
- Use preview deployments for testing changes
- Rollback easily through Vercel dashboard

### Monitoring Health
- Set up alerts for function failures
- Monitor response times and error rates
- Keep dependencies updated regularly

## 💡 Advanced Features

### Custom Domains
```bash
# Add custom domain via Vercel CLI
vercel domains add yourdomain.com
```

### Environment-Specific Configs
```bash
# Different settings for production/preview
GROQ_API_KEY_PROD = production_key
GROQ_API_KEY_PREVIEW = preview_key
```

### Edge Functions (Optional)
For better performance, consider migrating critical functions to Vercel Edge Runtime.

---

## 🎉 You're Live!

Once deployed, your FLUX system will be available globally at your Vercel URL. Users can interact with all 7 AI agents through a clean, responsive interface that works on any device.

**Example Production URL**: `https://flux-multi-agent.vercel.app`

**Test Commands**:
- "Hi Marc, review this architecture"
- "Hello Everyone, let's collaborate on this project"
- "Jess, can you create test cases for this feature?"

Your multi-agent AI system is now running in the cloud! 🌟