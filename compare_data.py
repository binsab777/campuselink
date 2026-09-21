import json

with open('fastapi_data_snapshot.json', 'r', encoding='utf-8') as f:
    fastapi = json.load(f)

with open('laravel_data_snapshot.json', 'r', encoding='utf-8') as f:
    laravel = json.load(f)

print("Entity | FastAPI Count | Laravel Count")
print("-" * 40)
for table in laravel.keys():
    fastapi_table = table
    
    # Handle naming differences between DB schemas
    if table == 'student_academic_history': fastapi_table = 'academic_history'
    
    fastapi_count = len(fastapi.get(fastapi_table, []))
    laravel_count = len(laravel.get(table, []))
    print(f"{table:25} | {fastapi_count:13} | {laravel_count:13}")
