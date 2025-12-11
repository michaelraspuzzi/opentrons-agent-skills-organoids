# Opentrons Agent Skills for Cardiac Organoid Research

**AI-powered protocol generation for Opentrons Flex liquid handling robots.**

This repo contains Claude Skills for automating cardiac organoid experiments, plus example protocols showing the iterative debugging process with Claude Code.

## What's Here

```
skills/                              # Claude Skills (use in Claude Projects)
├── hypothesis-generation.md         # Generate testable hypotheses
├── opentrons-protocol-gen.md        # Generate Opentrons protocols
└── protocol-validation.md           # Validate before running

protocols/                           # Example protocols
├── test-1-dox-dose-response.py      # First attempt (has bugs)
├── test-2-inflammatory-challenge.py # Second attempt (has bugs)
└── test-3-inflammatory-challenge-FIXED.py  # Fixed by Claude Code ✅

output/                              # Simulator results
└── simulator-output-test3.txt       # Successful simulation run

validate_protocol.py                 # Simple validation script
```

## The Story

### 1. Skills Generate Protocols

The `hypothesis-generation` skill creates experimental designs:
- Dose-response studies
- Time course experiments
- Drug comparisons

The `opentrons-protocol-gen` skill converts designs into Python protocols for Opentrons Flex.

### 2. Protocols Had Bugs

**Test 1 & 2** had critical issues:

| Issue | Problem | Impact |
|-------|---------|--------|
| 8-channel with individual wells | `plate['A1']` with 8-channel dispenses to A1-H1 | Wrong wells treated |
| Duplicate apiLevel | In both metadata and requirements | Protocol won't load |
| Missing trash bin | Flex requires explicit trash | Runtime error |

### 3. Claude Code Fixed Them

Using the Opentrons simulator (`opentrons_simulate`), Claude Code:
1. Identified all errors
2. Changed to single-channel pipette
3. Fixed apiLevel location
4. Added trash bin
5. Validated with simulator

**Test 3** passes simulation and is ready for hardware.

## Quick Start

### Use the Skills

1. Create a Claude Project
2. Add the skills from `skills/` folder to your project
3. Ask Claude to design an experiment and generate a protocol

### Run the Simulator

```bash
# Setup (requires Python 3.10+)
python3.10 -m venv venv-opentrons
source venv-opentrons/bin/activate
pip install opentrons

# Test any protocol
opentrons_simulate protocols/test-3-inflammatory-challenge-FIXED.py
```

### Validate Your Own Protocols

```bash
python validate_protocol.py your_protocol.py
```

## Key Learnings

### Pipette Selection Rule

**The #1 most common error:**

```python
# 8-channel pipettes dispense to ENTIRE COLUMN (A-H)
# If your wells are scattered, use single-channel!

# ❌ WRONG - treats A1, B1, C1, D1, E1, F1, G1, H1
p8_channel.dispense(100, plate['A1'])

# ✅ CORRECT - treats only A1
p1_channel.dispense(100, plate['A1'])
```

### Flex Protocol Requirements

```python
# 1. apiLevel in requirements ONLY
metadata = {'protocolName': '...'}  # No apiLevel here!
requirements = {'robotType': 'Flex', 'apiLevel': '2.16'}

# 2. Load trash bin
trash = protocol.load_trash_bin('A3')

# 3. Use Flex-specific labware
tips = protocol.load_labware('opentrons_flex_96_tiprack_1000ul', 'A1')
```

## Simulator Output (Test 3)

```
PHASE 1: INFLAMMATORY TREATMENT ADDITION
Adding Vehicle control (media) - Rows A-B, Cols 1-6
Picking up tip from A1 of Opentrons Flex 96 Tip Rack 1000 µL on slot A1
Aspirating 100.0 uL from A1 of NEST 12 Well Reservoir 15 mL on slot B1
Dispensing 100.0 uL into A1 of Corning 96 Well Plate 360 µL Flat on slot D1
...
TREATMENT ADDITION COMPLETE
Total wells treated: 72
...
FLUO-4 ADDITION COMPLETE
```

Full output in `output/simulator-output-test3.txt`

## Credits

- Skills generated using [Claude Projects](https://claude.ai)
- Protocols debugged using [Claude Code](https://claude.ai/code)
- Shoutout to the original skill-creation workflow that made these skills possible

## Use Your Own Skills

Feel free to:
1. Fork this repo
2. Modify the skills for your research
3. Generate protocols for your experiments
4. Validate and iterate with Claude Code

## License

MIT - use freely for research and education.
