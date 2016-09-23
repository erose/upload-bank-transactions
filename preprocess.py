import uuid, sys
def preprocess_file(filename):
    with open(filename, "r+") as file:
        contents = [line for line in file if len(line.rstrip()) != 0] # Remove blank lines.
        if contents[0].startswith("<UUID>"): # Don't add UUIDs if we already have them.
            print "File already preprocessed."
            return
        contents = ["<UUID>," + contents[0].rstrip() + ",<Tags>\n"] + ["{},{},{}\n".format(uuid.uuid4(), line.rstrip(), "") for line in contents[1:]]  # The first line is a header
        file.seek(0)
        file.write("".join(contents))
    
if __name__ == "__main__":
    preprocess_file(sys.argv[1])
