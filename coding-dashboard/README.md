# 🚀 Personal Coding Dashboard CLI

A fun, lightweight command-line tool to track your coding progress, manage projects, and get daily motivation!

## ✨ Features

- **📊 Coding Statistics**: Track total sessions, time spent coding, and streaks
- **⏱️ Session Timer**: Start/stop coding sessions with automatic time tracking
- **📁 Project Management**: Add and track your coding projects
- **💡 Daily Motivation**: Get random coding quotes to stay inspired
- **🎨 Beautiful ASCII Art**: Colorful headers that change every time you run it

## 🛠️ Installation

1. Clone or download this project
2. Install uv (if you don't have it):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

## 🚀 Usage

Run the dashboard:
```bash
# Using uv (recommended - super fast!)
uv run main.py

# Or use the convenient runner script
./run.sh

# Or install as a command
uv sync
coding-dashboard
```

### Menu Options:
1. **Start coding session** - Begin a timer for your coding session
2. **View projects** - See all your tracked projects
3. **Add new project** - Add a new project to track
4. **Exit** - Close the dashboard

## 📁 Data Storage

Your progress is automatically saved to `~/.coding_dashboard.json` in your home directory. This includes:
- Total coding sessions and time
- Current and longest streaks
- Project information
- Session history

## 🎯 Perfect For

- Getting back into coding
- Tracking daily coding habits
- Staying motivated with coding quotes
- Simple project management
- Building a coding streak

## 🔧 Customization

Feel free to modify:
- Add more motivational quotes in the `quotes` list
- Change ASCII art fonts in the `fonts` list
- Add new features like achievements or goals
- Customize colors and styling

## 🎨 Screenshots

The dashboard features:
- Random colorful ASCII art headers
- Clean statistics display
- Motivational quotes
- Simple menu navigation

Happy coding! 🎉
