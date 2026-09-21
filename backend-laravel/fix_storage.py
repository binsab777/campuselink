import re

with open('app/Services/FileStorageService.php', 'r') as f:
    c = f.read()

c = c.replace("return Storage::url($path);", "return url('/api/v1/files/' . $path);")

with open('app/Services/FileStorageService.php', 'w') as f:
    f.write(c)
