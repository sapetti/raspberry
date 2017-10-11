var express = require('express'),
	app = express(),
	server = require('http').createServer(app),
	io = require('socket.io').listen(server),
	PythonShell = require('python-shell');
	//pyshell = new PythonShell('runInArduino.py');

//Server port
server.listen(3456);

//Route request
app.get('/', function(req, res) {
	res.sendfile(__dirname + '/index.html');
});

//Listen server events
io.sockets.on('connection', function(socket) {
	//Listen sendCommand event
	socket.on('sendCommand', function(data) {
		//Show in history
		//console.log('Message receive: ' + data);

		try {		
			console.log('Load options');
			var options = {
			  mode: 'text',
			  scriptPath: '/home/pi/projects/nodeduino/python',
			  args: [data]
			};
				console.log('Options ' + options);
			console.log('pyshell');
			PythonShell.run('runInArduino.py', options, function (err, results) {
			  if (err) throw err;
			  // results is an array consisting of messages collected during execution
			  console.log('results: %j', results);
			});
			console.log('send');
			io.sockets.emit('newCommand', {cmd: data});
		} catch(err) {
			console.log('Error: ' + err);
		}
	});
	
});


