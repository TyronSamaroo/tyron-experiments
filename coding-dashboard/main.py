#!/usr/bin/env python3
"""
Personal Coding Dashboard CLI
A fun, lightweight tool to track your coding progress and get motivated!
"""

import os
import json
import time
import random
from datetime import datetime, timedelta
from pathlib import Path
import pyfiglet
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class CodingDashboard:
    def __init__(self):
        
        self.data_file = Path.home() / ".coding_dashboard.json"
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
            "total_sessions": 0,
            "total_time": 0,
            "current_streak": 0,
            "longest_streak": 0,
            "last_session": None,
            "projects": [],
            "achievements": []
        }
    
    def save_data(self):
        """Save user data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def format_time(self, total_seconds):
        """Format time in hours:minutes:seconds"""
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    def display_header(self):
        """Display the main dashboard header with ASCII art"""
        fonts = ["slant", "big", "block", "starwars", "doom", "larry3d"]
        colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
        
        font = random.choice(fonts)
        color = random.choice(colors)
        
        ascii_art = pyfiglet.figlet_format("CODING DASHBOARD", font=font)
        print(color + ascii_art)
        print(Fore.WHITE + "=" * 60)
        print()
    
    def display_stats(self):
        """Display coding statistics"""
        print(Fore.CYAN + "📊 YOUR CODING STATS")
        print("-" * 30)
        print(f"Total Sessions: {Fore.GREEN}{self.data['total_sessions']}")
        total_time_formatted = self.format_time(self.data['total_time'] * 60)  # Convert minutes to seconds
        print(f"Total Time: {Fore.GREEN}{total_time_formatted}")
        print(f"Current Streak: {Fore.YELLOW}{self.data['current_streak']} days")
        print(f"Longest Streak: {Fore.MAGENTA}{self.data['longest_streak']} days")
        print()
    
    def display_motivational_quote(self):
        """Display a random motivational coding quote"""
        quotes = [
            "Code is like humor. When you have to explain it, it's bad.",
            "First, solve the problem. Then, write the code.",
            "Experience is the name everyone gives to their mistakes.",
            "In order to be irreplaceable, one must always be different.",
            "Java is to JavaScript what car is to carpet.",
            "Sometimes it pays to stay in bed on Monday, rather than spending the rest of the week debugging Monday's code.",
            "Perfection is achieved not when there is nothing more to add, but rather when there is nothing more to take away.",
            "Code never lies, comments sometimes do.",
            "Simplicity is the ultimate sophistication.",
            "Make it work, make it right, make it fast."
        ]
        
        quote = random.choice(quotes)
        print(Fore.YELLOW + "💡 DAILY MOTIVATION")
        print("-" * 30)
        print(f'"{quote}"')
        print()
    
    def start_coding_session(self):
        """Start a new coding session"""
        print(Fore.GREEN + "🚀 Starting new coding session...")
        print("Press Enter when you're done coding to stop the timer.")
        
        start_time = time.time()
        input()
        end_time = time.time()
        
        session_duration_seconds = int(end_time - start_time)
        session_duration_minutes = session_duration_seconds / 60
        
        if session_duration_seconds > 0:
            self.data['total_sessions'] += 1
            self.data['total_time'] += session_duration_minutes
            self.data['last_session'] = datetime.now().isoformat()
            
            # Update streak
            today = datetime.now().date()
            if self.data['last_session']:
                last_date = datetime.fromisoformat(self.data['last_session']).date()
                if (today - last_date).days == 1:
                    self.data['current_streak'] += 1
                elif (today - last_date).days > 1:
                    self.data['current_streak'] = 1
            else:
                self.data['current_streak'] = 1
            
            self.data['longest_streak'] = max(self.data['longest_streak'], self.data['current_streak'])
            
            self.save_data()
            
            session_formatted = self.format_time(session_duration_seconds)
            total_time_formatted = self.format_time(self.data['total_time'] * 60)
            print(f"\n{Fore.GREEN}✅ Session completed! Duration: {session_formatted}")
            print(f"Total coding time: {total_time_formatted}")
        else:
            print(f"\n{Fore.RED}❌ Session too short to count!")
    
    def add_project(self):
        """Add a new project to track"""
        print(Fore.BLUE + "📁 ADD NEW PROJECT")
        print("-" * 30)
        name = input("Project name: ")
        language = input("Programming language: ")
        description = input("Brief description: ")
        
        project = {
            "name": name,
            "language": language,
            "description": description,
            "created": datetime.now().isoformat(),
            "status": "In Progress"
        }
        
        self.data['projects'].append(project)
        self.save_data()
        print(f"\n{Fore.GREEN}✅ Project '{name}' added!")
    
    def display_projects(self):
        """Display all tracked projects"""
        if not self.data['projects']:
            print(Fore.YELLOW + "📁 No projects tracked yet. Add one with option 3!")
            return
        
        print(Fore.BLUE + "📁 YOUR PROJECTS")
        print("-" * 30)
        for i, project in enumerate(self.data['projects'], 1):
            print(f"{i}. {Fore.GREEN}{project['name']}")
            print(f"   Language: {project['language']}")
            print(f"   Status: {project['status']}")
            print(f"   Description: {project['description']}")
            print()
    
    def show_menu(self):
        """Display the main menu"""
        while True:
            self.display_header()
            self.display_stats()
            self.display_motivational_quote()
            
            print(Fore.WHITE + "🎯 WHAT WOULD YOU LIKE TO DO?")
            print("-" * 30)
            print("1. Start coding session")
            print("2. View projects")
            print("3. Add new project")
            print("4. Exit")
            print()
            
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == "1":
                self.start_coding_session()
            elif choice == "2":
                self.display_projects()
                input("\nPress Enter to continue...")
            elif choice == "3":
                self.add_project()
                input("\nPress Enter to continue...")
            elif choice == "4":
                print(f"\n{Fore.GREEN}👋 Happy coding! See you next time!")
                break
            else:
                print(f"\n{Fore.RED}❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")
            
            # Clear screen for next iteration
            os.system('clear' if os.name == 'posix' else 'cls')

def main():
    """Main function"""
    dashboard = CodingDashboard()
    dashboard.show_menu()

if __name__ == "__main__":
    main()
