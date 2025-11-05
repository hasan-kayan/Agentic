# AI Coding Agent - Web UI

A beautiful, modern web interface for the AI Coding Agent with chat and terminal views.

## Features

- 💬 **Chat Interface** - Interact with the AI agent naturally
- 🖥️ **Terminal View** - Real-time execution logs
- 📊 **Live Stats** - Track files created, commands executed, iterations
- 🎨 **Modern Design** - Gradient UI with smooth animations
- ⚡ **Real-time Updates** - See what the AI is doing as it works
- 📱 **Responsive** - Works on desktop, tablet, and mobile

## Screenshots

### Chat + Terminal Split View
The UI features a split-screen design:
- **Left**: Chat interface for natural language interaction
- **Right**: Terminal view showing real-time execution logs

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Backend API running on port 8000

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The UI will be available at `http://localhost:3000`

### Production Build

```bash
npm run build
npm run preview
```

## Usage

1. **Start a conversation**: Type your task in the chat input
   - Example: "Create a React todo app with beautiful UI"
   - Example: "Build a FastAPI backend for a blog"

2. **Watch it work**: The terminal view shows:
   - Files being created
   - Commands being executed
   - Progress updates
   - Success/error messages

3. **Get results**: When complete, you'll see:
   - Summary of what was created
   - Number of files and commands
   - Project location

## Architecture

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx          # Top stats bar
│   │   ├── ChatInterface.jsx   # Left: Chat UI
│   │   └── TerminalView.jsx    # Right: Terminal logs
│   ├── App.jsx                 # Main app component
│   ├── App.css                 # App styles
│   └── main.jsx                # Entry point
├── public/
├── package.json
└── vite.config.js
```

## API Integration

The frontend communicates with the FastAPI backend:

- **Endpoint**: `POST /api/autonomous/execute`
- **Proxy**: Vite proxies `/api/*` to `http://localhost:8000`
- **CORS**: Enabled on backend for development

## Configuration

Edit `vite.config.js` to change backend URL:

```javascript
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // Change this
        changeOrigin: true,
      }
    }
  }
})
```

## Customization

### Colors

Edit `src/index.css` and component CSS files to change the color scheme.

Current theme:
- Primary: Purple/Blue gradient (`#667eea` to `#764ba2`)
- Success: Green (`#4caf50`)
- Error: Red (`#f44336`)
- Info: Blue (`#2196f3`)
- Warning: Orange (`#ff9800`)

### Layout

Edit `src/App.css` to change the split layout:

```css
.main-container {
  grid-template-columns: 1fr 1fr;  /* 50/50 split */
  /* OR */
  grid-template-columns: 2fr 1fr;  /* 66/33 split */
}
```

## Troubleshooting

### Backend Connection Error

**Error**: "Error communicating with the AI agent"

**Solution**: 
1. Make sure backend is running: `cd .. && python -m api.main`
2. Check backend is on port 8000: `curl http://localhost:8000/health`
3. Check browser console for CORS errors

### OpenAI API Quota Error

**Error**: "insufficient_quota"

**Solution**: Add credits to your OpenAI account at https://platform.openai.com/account/billing

### npm Install Errors

**Error**: EPERM or permission errors

**Solution**:
```bash
sudo chown -R $(whoami) ~/.npm
npm cache clean --force
npm install
```

## Technologies Used

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Axios** - HTTP client
- **React Icons** - Icon library
- **CSS3** - Styling with gradients and animations

## License

MIT

## Support

For issues or questions, check the main project README or open an issue.


