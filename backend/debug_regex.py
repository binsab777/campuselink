import re
content = open('../backend-laravel/tests/Feature/Admin/UserUpdateParityTest.php').read()
urls = re.findall(r"['\"](/api/v1/[^'\"]+)['\"]", content)
print(urls)
