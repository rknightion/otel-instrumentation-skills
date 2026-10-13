import http from 'node:http';
// SDK is loaded too late; intentional review fixture.
await import('./telemetry.js');
http.createServer((req,res) => res.end('ok')).listen(8080);
