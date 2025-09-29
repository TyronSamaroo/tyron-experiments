# 🏋️ Macro Tracker

A simple CLI tool to track weight, calories, and macros for fitness goals.

## ✨ Features

- **👤 Profile Setup**: Set your goals and daily macro targets
- **⚖️ Weight Tracking**: Log and track weight changes over time
- **🍎 Food Logging**: Log food intake with calories and macros
- **📊 Daily Summary**: View today's progress vs goals
- **📈 Weight History**: Track weight changes over time
- **💾 Persistent Data**: All data saved locally

## 🛠️ Installation

```bash
# Install dependencies with uv
uv install

# Or run directly
uv run main.py
```

## 🚀 Usage

Run the tracker:
```bash
uv run main.py
```

### Menu Options:
1. **Setup profile** - Set your goals and daily targets
2. **Log weight** - Record your current weight
3. **Log food** - Add food with calories and macros
4. **View today's summary** - See progress vs goals
5. **View weight history** - Track weight changes
6. **Exit** - Close the tracker

## 📁 Data Storage

Your data is saved to `~/.macro_tracker.json` including:
- Profile information and goals
- Weight history
- Daily food logs
- Macro tracking

## 🎯 Perfect For

- Simple macro tracking
- Weight loss/gain goals
- Daily nutrition monitoring
- Fitness progress tracking

## 🔧 Customization

The tracker automatically calculates basic macro targets based on your weight and goals, but you can customize:
- Daily calorie targets
- Protein, carb, and fat goals
- Weight tracking frequency

Happy tracking! 🎉
