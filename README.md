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
├── toolkit.py        # Main command-line program
├── modules/          # Scripts grouped by category and OS
│   ├── network/
│   │   ├── linux/
│   │   ├── macos/
│   │   └── windows/
│   ├── system/
│   └── ...
├── utils/            # Shared helper code
└── README.md
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
```

---

## How to Use

Run the tool:

```bash
python toolkit.py
```

The CLI walks through:
1. Selecting a category  
2. Choosing a task  
3. Entering any required input  

Results are printed to the terminal so they can be copied directly into support tickets.

---

## Example Tasks

- Network information and diagnostics
- DNS cache operations
- System information summary  
- Disk usage reports
- Service status checks
- List installed software

---

## Adding New Tasks

1. Add a script to the appropriate category and OS folder in `modules/`  
2. Make sure it runs on its own  
3. Keep output clean and readable  
4. Add a task to `tasks.json`    

Scripts can be written in:
- Bash  
- PowerShell  

---

## Project Goals

- Practice real-world helpdesk automation  
- Reduce repetitive troubleshooting work  
- Build practical scripting skills  

---

## Security Considerations

- Dry-run mode is available for tasks to preview commands
- Shell=true not used to prevent shell injection

