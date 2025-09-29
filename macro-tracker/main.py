#!/usr/bin/env python3
"""
Macro Tracker CLI
A simple tool to track weight, calories, and macros
"""

import json
import os
from datetime import datetime, date
from pathlib import Path
from colorama import Fore, Style, init
from tabulate import tabulate

# Initialize colorama
init(autoreset=True)

class MacroTracker:
    def __init__(self):
        self.data_file = Path.home() / ".macro_tracker.json"
        self.data = self.load_data()
        
    def load_data(self):
        """Load user data from JSON file"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "profile": {
                "name": "",
                "age": 0,
                "height": 0,
                "weight": 0,
                "goal": "maintain",  # lose, maintain, gain
                "daily_calories": 2000,
                "daily_protein": 150,
                "daily_carbs": 200,
                "daily_fat": 65
            },
            "weight_history": [],
            "daily_logs": {}
        }
    
    def save_data(self):
        """Save user data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def display_header(self):
        """Display the main header"""
        print(Fore.CYAN + "=" * 60)
        print(Fore.CYAN + "🏋️  MACRO TRACKER")
        print(Fore.CYAN + "=" * 60)
        print()
    
    def setup_profile(self):
        """Setup user profile"""
        print(Fore.YELLOW + "👤 SETUP YOUR PROFILE")
        print("-" * 30)
        
        name = input("Name: ").strip()
        age = int(input("Age: ") or "25")
        height = float(input("Height (cm): ") or "170")
        weight = float(input("Current weight (kg): ") or "70")
        
        print("\nGoals:")
        print("1. Lose weight")
        print("2. Maintain weight")
        print("3. Gain weight")
        goal_choice = input("Choose goal (1-3): ").strip()
        goals = {"1": "lose", "2": "maintain", "3": "gain"}
        goal = goals.get(goal_choice, "maintain")
        
        # Calculate basic macros (simplified)
        daily_calories = int(weight * 30)  # Rough estimate
        daily_protein = int(weight * 2)    # 2g per kg
        daily_carbs = int(daily_calories * 0.4 / 4)  # 40% of calories
        daily_fat = int(daily_calories * 0.25 / 9)   # 25% of calories
        
        self.data["profile"] = {
            "name": name,
            "age": age,
            "height": height,
            "weight": weight,
            "goal": goal,
            "daily_calories": daily_calories,
            "daily_protein": daily_protein,
            "daily_carbs": daily_carbs,
            "daily_fat": daily_fat
        }
        
        self.save_data()
        print(f"\n{Fore.GREEN}✅ Profile setup complete!")
    
    def log_weight(self):
        """Log current weight"""
        print(Fore.BLUE + "⚖️  LOG WEIGHT")
        print("-" * 30)
        
        weight = float(input("Current weight (kg): "))
        today = date.today().isoformat()
        
        # Update current weight in profile
        self.data["profile"]["weight"] = weight
        
        # Add to weight history
        self.data["weight_history"].append({
            "date": today,
            "weight": weight
        })
        
        self.save_data()
        print(f"\n{Fore.GREEN}✅ Weight logged: {weight} kg")
    
    def log_food(self):
        """Log food intake"""
        print(Fore.GREEN + "🍎 LOG FOOD")
        print("-" * 30)
        
        food_name = input("Food name: ").strip()
        calories = float(input("Calories: ") or "0")
        protein = float(input("Protein (g): ") or "0")
        carbs = float(input("Carbs (g): ") or "0")
        fat = float(input("Fat (g): ") or "0")
        quantity = input("Quantity (e.g., '1 cup', '100g'): ").strip() or "1 serving"
        
        today = date.today().isoformat()
        
        if today not in self.data["daily_logs"]:
            self.data["daily_logs"][today] = {
                "foods": [],
                "total_calories": 0,
                "total_protein": 0,
                "total_carbs": 0,
                "total_fat": 0
            }
        
        food_entry = {
            "name": food_name,
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fat": fat,
            "quantity": quantity,
            "time": datetime.now().strftime("%H:%M")
        }
        
        self.data["daily_logs"][today]["foods"].append(food_entry)
        self.data["daily_logs"][today]["total_calories"] += calories
        self.data["daily_logs"][today]["total_protein"] += protein
        self.data["daily_logs"][today]["total_carbs"] += carbs
        self.data["daily_logs"][today]["total_fat"] += fat
        
        self.save_data()
        print(f"\n{Fore.GREEN}✅ {food_name} logged!")
    
    def view_daily_summary(self):
        """View today's summary"""
        today = date.today().isoformat()
        
        print(Fore.MAGENTA + "📊 TODAY'S SUMMARY")
        print("-" * 30)
        
        if today not in self.data["daily_logs"]:
            print("No food logged today.")
            return
        
        daily = self.data["daily_logs"][today]
        profile = self.data["profile"]
        
        # Display totals vs goals
        print(f"Calories: {daily['total_calories']}/{profile['daily_calories']}")
        print(f"Protein:  {daily['total_protein']:.1f}g/{profile['daily_protein']}g")
        print(f"Carbs:    {daily['total_carbs']:.1f}g/{profile['daily_carbs']}g")
        print(f"Fat:      {daily['total_fat']:.1f}g/{profile['daily_fat']}g")
        
        # Show remaining
        remaining_calories = profile['daily_calories'] - daily['total_calories']
        remaining_protein = profile['daily_protein'] - daily['total_protein']
        remaining_carbs = profile['daily_carbs'] - daily['total_carbs']
        remaining_fat = profile['daily_fat'] - daily['total_fat']
        
        print(f"\n{Fore.YELLOW}Remaining:")
        print(f"Calories: {remaining_calories}")
        print(f"Protein:  {remaining_protein:.1f}g")
        print(f"Carbs:    {remaining_carbs:.1f}g")
        print(f"Fat:      {remaining_fat:.1f}g")
        
        # Show food list
        if daily['foods']:
            print(f"\n{Fore.CYAN}Foods logged today:")
            for food in daily['foods']:
                print(f"• {food['name']} ({food['quantity']}) - {food['calories']} cal at {food['time']}")
    
    def view_weight_history(self):
        """View weight history"""
        print(Fore.BLUE + "📈 WEIGHT HISTORY")
        print("-" * 30)
        
        if not self.data["weight_history"]:
            print("No weight data available.")
            return
        
        # Show last 10 entries
        recent_weights = self.data["weight_history"][-10:]
        
        table_data = []
        for entry in recent_weights:
            table_data.append([
                entry["date"],
                f"{entry['weight']} kg"
            ])
        
        print(tabulate(table_data, headers=["Date", "Weight"], tablefmt="grid"))
    
    def show_menu(self):
        """Display the main menu"""
        while True:
            self.display_header()
            
            # Show profile info if set up
            if self.data["profile"]["name"]:
                profile = self.data["profile"]
                print(f"Welcome, {profile['name']}! Current weight: {profile['weight']} kg")
                print()
            
            print(Fore.WHITE + "🎯 WHAT WOULD YOU LIKE TO DO?")
            print("-" * 30)
            print("1. Setup profile")
            print("2. Log weight")
            print("3. Log food")
            print("4. View today's summary")
            print("5. View weight history")
            print("6. Exit")
            print()
            
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == "1":
                self.setup_profile()
                input("\nPress Enter to continue...")
            elif choice == "2":
                self.log_weight()
                input("\nPress Enter to continue...")
            elif choice == "3":
                self.log_food()
                input("\nPress Enter to continue...")
            elif choice == "4":
                self.view_daily_summary()
                input("\nPress Enter to continue...")
            elif choice == "5":
                self.view_weight_history()
                input("\nPress Enter to continue...")
            elif choice == "6":
                print(f"\n{Fore.GREEN}👋 Keep tracking those macros! See you next time!")
                break
            else:
                print(f"\n{Fore.RED}❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")
            
            # Clear screen for next iteration
            os.system('clear' if os.name == 'posix' else 'cls')

def main():
    """Main function"""
    tracker = MacroTracker()
    tracker.show_menu()

if __name__ == "__main__":
    main()
