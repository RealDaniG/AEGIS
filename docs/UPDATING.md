# Updating Your AEGIS Project

This document explains how to keep your cloned AEGIS project up to date with the latest changes from the GitHub repository.

## Automatic Update Scripts

We provide two easy-to-use scripts to update your AEGIS installation:

### Windows Batch Script (UPDATE_PROJECT.bat)

A simple batch script for Windows users:

1. Navigate to your AEGIS project directory
2. Double-click on `UPDATE_PROJECT.bat`
3. The script will automatically:
   - Fetch the latest changes from GitHub
   - Pull updates to your local repository
   - Update submodules (if any)
   - Update Python dependencies (if Python is installed)

### PowerShell Script (UPDATE_PROJECT.ps1)

An enhanced PowerShell script with better error handling and visual feedback:

1. Navigate to your AEGIS project directory
2. Right-click in the folder and select "Open in Terminal" or open PowerShell
3. Run the script:
   ```powershell
   .\UPDATE_PROJECT.ps1
   ```
4. For advanced users, you can skip dependency updates:
   ```powershell
   .\UPDATE_PROJECT.ps1 -SkipDependencies
   ```

## Manual Update Process

If you prefer to update manually, you can use the following Git commands:

```bash
# Navigate to your AEGIS project directory
cd path/to/your/AEGIS

# Fetch the latest changes
git fetch origin

# Pull the latest changes
git pull origin master

# Update submodules (if any)
git submodule update --init --recursive

# Update Python dependencies (optional)
pip install -r requirements.txt --upgrade
pip install -r unified_requirements.txt --upgrade
```

## Troubleshooting

### Common Issues

1. **"Permission denied" errors**: Make sure no AEGIS processes are running that might be locking files

2. **Merge conflicts**: If you've made local changes, the script will attempt to stash them. If conflicts occur:
   - Review the conflicting files
   - Manually resolve conflicts or restore your changes
   - Consider backing up important local changes before updating

3. **Git not found**: Install Git from https://git-scm.com/

4. **Python not found**: Install Python from https://python.org/

### If Updates Fail

If the automatic scripts fail:

1. Close any running AEGIS applications
2. Try running the script again
3. If it continues to fail, try the manual process
4. As a last resort, you can backup your important files and re-clone the repository:
   ```bash
   git clone https://github.com/RealDaniG/AEGIS.git
   ```

## Best Practices

1. **Regular Updates**: Update your AEGIS installation regularly to get the latest features and security fixes

2. **Backup Local Changes**: If you've made local modifications, consider backing them up before updating

3. **Check Release Notes**: Review the GitHub releases page for important changes:
   https://github.com/RealDaniG/AEGIS/releases

4. **Report Issues**: If you encounter problems during updates, please report them on our GitHub issues page

## Community Growth and Development

As part of our community-driven development model, each update may include:
- Enhanced conversational training data
- New knowledge contributions from the community
- Improved collaborative development tools
- Expanded computational capabilities through network growth

By keeping your AEGIS installation updated, you're participating in the collective intelligence growth of the system.