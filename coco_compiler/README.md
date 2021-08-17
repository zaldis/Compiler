# Simple compiler based on Coco/R compilers generator

[Coco link](https://ssw.jku.at/Research/Projects/Coco/#Java)

## Requirements

- JDK
- python 3

## How to use

1. Go to the directory: `./out`
2. Run command: `java JavaParser.class ../program.txt`
3. Copy coded program into the `program.bytecode` file
4. Go to the root directory
5. Run command: `python evaluator.py program.bytecode`
6. Check states on the each step of evaluation