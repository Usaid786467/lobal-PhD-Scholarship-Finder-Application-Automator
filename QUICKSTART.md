# Quick Start Guide 🚀

Get up and running in 5 minutes!

## Step 1: Setup (2 minutes)

```bash
# Make sure you're in the project directory
cd lobal-PhD-Scholarship-Finder-Application-Automator

# Run one-command setup
./scripts/setup.sh
```

This will:
- ✅ Create Python virtual environment
- ✅ Install all dependencies
- ✅ Initialize database
- ✅ Setup configuration files

## Step 2: Configure (1 minute)

Edit `backend/.env`:

```env
# Get your Gemini API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your-gemini-api-key-here

# Gmail SMTP (optional for now, needed for sending emails)
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## Step 3: Start (1 minute)

```bash
./scripts/start.sh
```

The application will start:
- 🎨 Frontend: http://localhost:3000
- 🔧 Backend: http://localhost:5000

## Step 4: Use (1 minute)

1. **Open browser**: Go to http://localhost:3000
2. **Register**: Create your account
3. **Discover**: Click "Discover Universities" 
4. **Find**: Search for professors
5. **Generate**: Select professors and generate emails
6. **Send**: Review and send your emails!

## Common Issues

### Port already in use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### Database errors
```bash
cd backend
source venv/bin/activate
python cli/main.py db reset
```

### Module not found
```bash
# Reinstall dependencies
./scripts/setup.sh
```

## Testing

```bash
./scripts/test.sh
```

## CLI Usage

```bash
cd backend
source venv/bin/activate

# See all commands
python cli/main.py --help

# Check status
python cli/main.py status

# Scrape universities
python cli/main.py scrape universities --country USA --limit 10
```

## What's Next?

- 📖 Read the full [README.md](README.md) for detailed documentation
- 🎓 Start discovering universities and professors
- ✉️ Generate your first batch of emails
- 📊 Track your application success

## Need Help?

- Check [README.md](README.md) for full documentation
- Open an issue on GitHub
- Review the code comments - everything is documented!

Happy applying! 🎓✨
