import os, glob, re

for file in glob.glob('app/Models/*.php'):
    with open(file, 'r') as f:
        c = f.read()
    
    if 'StudentProject' in file and '$casts' not in c:
        c = c.replace("protected $guarded = ['id'];", "protected $guarded = ['id'];\n    protected $casts = ['technologies' => 'array'];")
    if 'Job' in file and '$casts' not in c:
        c = c.replace("protected $guarded = ['id'];", "protected $guarded = ['id'];\n    protected $casts = ['eligibility_config' => 'array'];")
    if 'StudentScore' in file and '$casts' not in c:
        c = c.replace("protected $guarded = ['id'];", "protected $guarded = ['id'];\n    protected $casts = ['explanation_data' => 'array'];")
    if 'Student' in file and '$casts' not in c:
        c = c.replace("protected $guarded = ['id'];", "protected $guarded = ['id'];\n    protected $casts = ['profile_metadata' => 'array', 'dob' => 'datetime'];")
        
    with open(file, 'w') as f:
        f.write(c)
