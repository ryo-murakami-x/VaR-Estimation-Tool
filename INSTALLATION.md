# Installation Guide for VaR Estimation Tool

This guide provides step-by-step instructions for installing the VaR Estimation Tool on Windows, macOS, and Linux.

## Table of Contents

- [System Requirements](#system-requirements)
- [Windows Installation](#windows-installation)
- [macOS Installation](#macos-installation)
- [Linux Installation](#linux-installation)
- [Troubleshooting](#troubleshooting)
- [Verification](#verification)

## System Requirements

### Minimum Requirements
- **OS**: Windows 7+, macOS 10.14+, Linux (Ubuntu 18.04+, CentOS 7+, etc.)
- **Python**: 3.7 or higher
- **RAM**: 1 GB minimum
- **Disk Space**: 500 MB

### Recommended Requirements
- **Python**: 3.9 or higher
- **RAM**: 4 GB or more
- **Disk Space**: 1 GB

## Windows Installation

### Method 1: Using Automated Installer (Recommended)

1. **Download Python** (if not already installed)
   - Visit https://www.python.org/downloads/
   - Download Python 3.9 or higher
   - **Important**: Check "Add Python to PATH" during installation
   - Click "Install Now" or customize as needed

2. **Run the installer script**
   - Open Command Prompt (Win + R, type `cmd`, press Enter)
   - Navigate to the project directory:
     ```batch
     cd path\to\VaR-Estimation-Tool
     ```
   - Run the installer:
     ```batch
     install.bat
     ```
   - Wait for the installation to complete
   - Press any key when prompted

3. **Launch the application**
   - After installation, activate the environment:
     ```batch
     venv\Scripts\activate.bat
     ```
   - Run the GUI:
     ```batch
     python main.py
     ```

### Method 2: Manual Installation

1. **Install Python**
   - Visit https://www.python.org/downloads/
   - Download and install Python 3.9 or higher
   - Ensure "Add Python to PATH" is checked

2. **Open Command Prompt** and navigate to project:
   ```batch
   cd path\to\VaR-Estimation-Tool
   ```

3. **Create virtual environment**:
   ```batch
   python -m venv venv
   ```

4. **Activate virtual environment**:
   ```batch
   venv\Scripts\activate.bat
   ```

5. **Install dependencies**:
   ```batch
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. **Verify installation**:
   ```batch
   python integration_test.py
   ```

7. **Launch GUI**:
   ```batch
   python main.py
   ```

### Method 3: Using pip (After Git Clone)

```batch
# Clone repository
git clone https://github.com/yourusername/VaR-Estimation-Tool.git
cd VaR-Estimation-Tool

# Install in development mode
pip install -e .

# Run the tool
python main.py
```

---

## macOS Installation

### Method 1: Using Automated Installer (Recommended)

1. **Install Python** (if not already installed)
   - **Using Homebrew** (recommended):
     ```bash
     brew install python3
     ```
   - Or visit https://www.python.org/downloads/ and download macOS installer

2. **Run the installer script**
   - Open Terminal (⌘ + Space, type `Terminal`, press Enter)
   - Navigate to the project directory:
     ```bash
     cd path/to/VaR-Estimation-Tool
     ```
   - Make the script executable:
     ```bash
     chmod +x install.sh
     ```
   - Run the installer:
     ```bash
     ./install.sh
     ```
   - Wait for the installation to complete

3. **Launch the application**
   - Activate the virtual environment:
     ```bash
     source venv/bin/activate
     ```
   - Run the GUI:
     ```bash
     python3 main.py
     ```

### Method 2: Manual Installation

1. **Install Python using Homebrew** (recommended):
   ```bash
   brew install python3
   ```

2. **Open Terminal** and navigate to project:
   ```bash
   cd path/to/VaR-Estimation-Tool
   ```

3. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   ```

4. **Activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```

5. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. **Verify installation**:
   ```bash
   python3 integration_test.py
   ```

7. **Launch GUI**:
   ```bash
   python3 main.py
   ```

### Using conda (Alternative)

If you prefer conda:
```bash
conda create -n var-tool python=3.9
conda activate var-tool
pip install -r requirements.txt
python main.py
```

---

## Linux Installation

### Method 1: Using Automated Installer (Recommended)

#### Ubuntu/Debian:
```bash
# Install Python and dependencies
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv -y

# Navigate to project directory
cd path/to/VaR-Estimation-Tool

# Make installer executable
chmod +x install.sh

# Run installer
./install.sh

# Activate environment and run
source venv/bin/activate
python3 main.py
```

#### CentOS/RHEL:
```bash
# Install Python and dependencies
sudo yum install python3 python3-pip -y

# Navigate to project directory
cd path/to/VaR-Estimation-Tool

# Make installer executable
chmod +x install.sh

# Run installer
./install.sh

# Activate environment and run
source venv/bin/activate
python3 main.py
```

#### Fedora:
```bash
# Install Python and dependencies
sudo dnf install python3 python3-pip -y

# Navigate to project directory
cd path/to/VaR-Estimation-Tool

# Make installer executable
chmod +x install.sh

# Run installer
./install.sh

# Activate environment and run
source venv/bin/activate
python3 main.py
```

### Method 2: Manual Installation

#### Ubuntu/Debian:

1. **Install dependencies**:
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip python3-venv -y
   ```

2. **Navigate to project**:
   ```bash
   cd path/to/VaR-Estimation-Tool
   ```

3. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   ```

4. **Activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```

5. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. **Verify installation**:
   ```bash
   python3 integration_test.py
   ```

7. **Launch GUI**:
   ```bash
   python3 main.py
   ```

#### CentOS/RHEL:

1. **Install dependencies**:
   ```bash
   sudo yum install python3 python3-pip -y
   ```

2. **Follow steps 2-7 above** (same as Ubuntu/Debian)

---

## Docker Installation (Optional)

If you prefer containerization:

1. **Create Dockerfile** (if not provided):
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   
   CMD ["python", "main.py"]
   ```

2. **Build and run**:
   ```bash
   docker build -t var-tool .
   docker run -it var-tool
   ```

---

## Troubleshooting

### Python Not Found

**Windows**:
- Add Python to PATH: https://www.python.org/downloads/
- Use `py` instead of `python`: `py main.py`

**macOS/Linux**:
- Use `python3` instead of `python`
- Check installation: `which python3`

### Permission Denied (macOS/Linux)

```bash
chmod +x install.sh
```

### Virtual Environment Issues

**Recreate virtual environment**:
```bash
# macOS/Linux
rm -rf venv
python3 -m venv venv
source venv/bin/activate

# Windows
rmdir /s venv
python -m venv venv
venv\Scripts\activate.bat
```

### Module Not Found Errors

**Ensure virtual environment is activated**:
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate.bat
```

**Reinstall dependencies**:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### GUI Window Won't Display

**macOS/Linux**:
- Ensure X11 or display server is available
- For remote connections, use X11 forwarding:
  ```bash
  ssh -X user@host
  ```

**Windows**:
- Try running as Administrator
- Update Python installation

---

## Data Setup (IMPORTANT)

Before verification and testing, you need to download stock data from Stooq.

### Download Stock Data

1. **Visit Stooq**: https://stooq.com/db/h/
2. **Download CSV files** for TSE stocks (e.g., ticker 1301, 1332, 2001)
3. **Organize files** in your project directory

### Quick Setup

```bash
# Create directory structure
mkdir -p data/daily/jp/tse\ stocks/{1,2}

# Rename downloaded CSV files
# Format: {ticker}.jp.txt
# Example: 1301.csv → 1301.jp.txt

mv ~/Downloads/1301.csv data/daily/jp/tse\ stocks/1/1301.jp.txt
mv ~/Downloads/2001.csv data/daily/jp/tse\ stocks/2/2001.jp.txt
```

### Expected Directory Structure

```
VaR-Estimation-Tool/
├── data/
│   └── daily/
│       └── jp/
│           └── tse stocks/
│               ├── 1/
│               │   ├── 1301.jp.txt
│               │   ├── 1305.jp.txt
│               │   └── ...
│               └── 2/
│                   ├── 2001.jp.txt
│                   ├── 2002.jp.txt
│                   └── ...
├── main.py
├── data_reader.py
└── ...
```

**Note**: For detailed data setup instructions, see [STOOQ_DATA_SETUP.md](STOOQ_DATA_SETUP.md)

---

## Verification

After installation and data setup, verify everything works:

### 1. Test Data Reader
```bash
python3 data_reader.py
# Type: 1301 (or another ticker you downloaded)
# Type: quit
```

### 2. Test VaR Calculator
```bash
python3 var_calculator.py
```

### 3. Run Integration Tests
```bash
python3 integration_test.py
```

Expected output:
```
✓ Data Reader: PASS
✓ VaR Calculator: PASS
✓ Full Integration: PASS
```

### 4. Launch GUI
```bash
python3 main.py
```

GUI should open showing:
- Stock Selection panel
- VaR Parameters
- Results area

---

## Uninstalling

### Remove Virtual Environment

**macOS/Linux**:
```bash
rm -rf venv
```

**Windows**:
```batch
rmdir /s /q venv
```

### Remove Project Files

Simply delete the project directory.

---

## Getting Help

If you encounter issues:

1. **Check Troubleshooting section** above
2. **Review QUICKSTART.md** for common questions
3. **Check README.md** for detailed documentation
4. **Open an issue** on GitHub with:
   - Error message
   - Python version
   - Operating system
   - Steps to reproduce

---

## Next Steps

After successful installation:

1. Read [QUICKSTART.md](QUICKSTART.md) for quick start guide
2. Read [README.md](README.md) for full documentation
3. Load sample stock: ticker `1301`
4. Explore different VaR parameters
5. Try integration tests: `python3 integration_test.py`

---

**Need Help?**
- GitHub Issues: https://github.com/yourusername/VaR-Estimation-Tool/issues
- Discussions: https://github.com/yourusername/VaR-Estimation-Tool/discussions

**Happy analyzing!** 📊
