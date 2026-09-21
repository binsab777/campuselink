const http = require('http');

const options = {
  hostname: 'localhost',
  port: 8000,
  path: '/api/v1/admin/users/1/role',
  method: 'PATCH',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
};

const req = http.request(options, (res) => {
  console.log(`STATUS: ${res.statusCode}`);
  res.on('data', (d) => {
    process.stdout.write(d);
  });
});

req.on('error', (error) => {
  console.error(error);
});

req.write(JSON.stringify({ role: 'PLACEMENT_OFFICER' }));
req.end();
