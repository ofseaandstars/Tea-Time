# Tea Time

A utility script for those like me who regularly forget they put the kettle on to boil.
**Requires Python 3.13.**

![image](https://i.imgur.com/hHt9Hli.png)

## Installation

Clone the repository, (optionally) set up a Python virtual environment, and run the following commands:

```bash
  python -m pip install -r requirements.txt
  python -m venv .  # Optional
```

If you are using a virtual environment, activate it using one of the following options, based on your operating system:

```bash
  Scripts/Activate.ps1 # Windows PowerShell
  Scripts/Activate.bat # Windows CMD
  bin/Activate.ps1 # pwsh
  source /bin/activate # bash/zsh
```

Then simply run the command - if you do not specify the arguments, you'll be prompted to set them within the application.

```bash
  python ./tea_time.py -k 3m -b 3m
```

## Usage

Tea Time can be run stand-alone, but it does also support a couple of arguments:

### No arguments

If no arguments are specified, Tea Time will prompt you to provide timers for kettle boiling and tea brewing time.

```bash
  python ./tea-time.py
```

### Kettle timer

The `-k` arguments allows you to specify a time string for your kettle boiling timer. Format is <int>[s/m].

```bash
  python ./tea-time.py -k 3m
```

### Brewing timer

The `-b` arguments allows you to specify a time string for your tea brewing timer. Format is <int>[s/m].

```bash
  python ./tea-time.py -b 3m
```

This argument can be left blank to skip the tea-brewing stage - if you don't brew your tea, that is.

### Kettle and Brewing timers

This command will allow you to set separate times for both timers. Useful if your kettle takes a lot longer to boil than your tea takes to brew!

```bash
  python ./tea-time.py -k 5m -b 2m
```

## Interface

1. Once the script is run, you will be prompted with instructions - just follow them and watch the magic happen.
2. After the timers begin, you are free to continue doing whatever it was you were doing - once the kettle is boiled, a 'ding' sound will play.
3. Go pour your water onto your teabag and let it start brewing. Then, continue the script and let the tea brewing timer run.
4. Once the tea is brewed, a 'ring' sound will play to inform you it is ready!
5. ???
6. Profit
