# IT Support Toolkit

A simple command-line toolkit I am building for common IT support and helpdesk tasks.

This project helps to automate everyday troubleshooting work on **Windows, macOS, and Linux**. It’s designed to be easy to understand, easy to run, and easy to extend.

---

## What This Does

- Runs small scripts to check common system issues  
- Collects basic system information for support tickets  
- Speeds up repetitive troubleshooting tasks  
- Works across Windows, macOS, and Linux  

---

## Typical Uses

- Check network connectivity  
- View disk space and system health  
- Gather OS and hardware information  
- Verify services or running processes  
- Collect logs for escalation  

---

## Project Structure

```
it-support-toolkit/
├── cli.py            # Main command-line program
├── tasks/            # Scripts grouped by OS
│   ├── windows/
│   ├── macos/
│   └── linux/
├── tasks.json        # List of available tasks
├── utils/            # Shared helper code
├── README.md
└── requirements.txt
```

---

## Requirements

- Python 3.9 or newer
- One of the following:
  - Windows 10 / 11
  - macOS
  - Linux (Ubuntu, Fedora, Arch, etc.)

Some tasks may require administrator or sudo access.

---

## Setup

```bash
git clone https://github.com/rojounooo/it-support-toolkit.git
cd it-support-toolkit
pip install -r requirements.txt
```

---

## How to Use

Run the tool:

```bash
python cli.py
```

The CLI walks through:
1. Selecting a category  
2. Choosing a task  
3. Entering any required input  

Results are printed to the terminal so they can be copied directly into support tickets.

---

## Example Tasks

### Windows
- Network information
- Flush DNS cache
- List installed software

### macOS
- System information summary
- Wi-Fi checks

### Linux
- Disk usage report
- Service status checks

---

## Adding New Tasks

1. Add a script to the correct OS folder  
2. Make sure it runs on its own  
3. Register it in `tasks.json`  
4. Keep output clean and readable  

Scripts can be written in:
- Bash  
- PowerShell  

---

## Project Goals

- Practice real-world helpdesk automation  
- Reduce repetitive troubleshooting work  
- Build practical scripting skills  
- Maintain a clean, portfolio-ready project  

---

