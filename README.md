# File Convertor

## Support
[ ] Linux
    [x] Nautilus
[ ] Windows - planned on demand

## Usage
A file convertor tool that puts itself into the context menu of your chosen file manager.

### Supported Formats
* PNG
* JPG / JPEG
* JFIF
* WEBP

## Installation

### Quick

> ALWAYS CHECK WHATS IN SCRIPTS YOU EXECUTE BEFORE YOU DO SO, I am not doing anything nefarious but why trust me?
```bash
bash <(curl -sSL https://raw.githubusercontent.com/VerumHades/file_convertor/main/install.sh)
```

### Cloning the repo

```bash
git clone https://github.com/VerumHades/file_convertor.git
cd file_convertor
```

#### For nautilus
```bash
chmod +x install/nautilus.sh
./install/nautilus.sh
```

## Uninstallation

```bash
bash <(curl -sSL https://raw.githubusercontent.com/VerumHades/file_convertor/main/install.sh) uninstall
```

```bash
./install.sh uninstall
```