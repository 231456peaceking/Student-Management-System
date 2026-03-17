import shutil

shutil.copy(
"../data/students.txt",
"../backup/students_backup.txt"
)

print("Backup complete")