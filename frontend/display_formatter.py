def show_students(data):

    print("\n--- Student List ---")

    for line in data.split("\n"):
        if line:
            roll,name,cls,contact = line.split("|")
            print(f"Roll:{roll} Name:{name} Class:{cls} Contact:{contact}")