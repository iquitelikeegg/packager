# Packager

## Usage instructions

```
# python packager.py <source directory> <dest directory>
```

- Reads packager.json (see packager.json-example)
- Copies all files from the source directory into the dest directory
- Removes the files specified under the "delete" key
- Moves the files specified under the "move" key
- Creates the files and directories under the "create" key 
