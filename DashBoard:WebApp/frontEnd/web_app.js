    // set up ========================
    var express  = require('express');
    var app      = express();                              
    var morgan = require('morgan');
    var http = require('http').createServer(app); 
    var bodyParser = require('body-parser');    
    var methodOverride = require('method-override'); 
    var mqtt    = require('mqtt');


    var client = mqtt.connect({ host: '54.153.76.231', port: 1883 });
    //var client = mqtt.connect({ host: '52.26.17.88', port: 1883 });
    client.subscribe('piData');
    client.subscribe('State');
    client.subscribe('Notif');
    //web server
    app.set('port', process.env.PORT || 8080);
    app.use(express.static(__dirname + '/public'));                 // set the static files location /public/img will be /img for users
    app.use(morgan('dev'));                                         // log every request to the console
    app.use(bodyParser.urlencoded({'extended':'true'}));            // parse application/x-www-form-urlencoded
    app.use(bodyParser.json());                                     // parse application/json
    app.use(bodyParser.json({ type: 'application/vnd.api+json' })); // parse application/vnd.api+json as json
    app.use(methodOverride());
    var msg= {"Dist_Value": 200, "Light_Value": 200};
    var current = {"PiState": true, "ThresVal": 20};
    var counterui = 0;
    var notificationArr = [];
    //var notify = {"NotifyCount": 0, "NotifyVal": []};

    client.on('message', function(topic, message, packet) {
            console.log("message : " + message);
            if(topic == "piData")
            {
                msg = message;
            }
            else if(topic == "State")
            {
                current = message;
            }
            else if(topic == "Notif")
            {
                console.log("Original notification : " + JSON.parse(message).message);
                notificationArr.push(JSON.parse(message).message);
                //console.log("Display notification " + notificationArr);
                counterui++;
            }
        }); 
   
    app.get('/api/data', function(req, res) {
                //console.log("I have arrived");
                res.send(msg); 
    });

    app.get('/api/currentState', function(req, res) {
            res.send(current);
    });

    app.get('/api/notification', function(req, res) {
        //console.log("counter sent : "+ counterui);
        //console.log("Please notificaion backendarray : " + notificationArr);
        res.send({"NotifyCount": counterui, "NotifyVal": notificationArr});
    });

    app.get('/api/notificationSet', function(req, res){
        counterui = 0;
        var notificationArr = [];
        //console.log("counter reset"+ counterui);
        res.header("Access-Control-Allow-Origin", "*");
        res.send("Success");
    });
   app.post('/api/button', function(req, res) {
        console.log("Inside Post...");
        var x = JSON.stringify(req.body.btnState); 
        client.publish('SetUserSensorState',x);        
        //console.log(req.body);
        res.header("Access-Control-Allow-Origin", "*");
        res.send("Success");
    });

   app.post('/api/threshold', function(req, res) {
        console.log("successful");
        var x = JSON.stringify(req.body.thrs); 
        client.publish('SetUserThreshold',x);        
        //console.log(req.body.thrs);
        res.header("Access-Control-Allow-Origin", "*");
        res.send("Success");
    });

/*    app.get('*', function(req, res) {
        res.sendfile('./public/index.html'); // load the single view file (angular will handle the page changes on the front-end)
    });*/
 
    http.listen(app.get('port'), function() {
        console.log('Express server listening on port ' + app.get('port'));
    });