var express = require('express');
var Stats = require('fast-stats').Stats;
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
    res.render('index');
  //res.render('index', { title: 'Express' });
  //res.sendFile('index.html');
});

router.get('/petm/json/pie', function(req, res, next){
    /*var json1 = [200, 400, 500, 150];
    var json2 = [300, 160, 434, 234];
    var data = { data1 : json1, data2 : json2 }
    writeJSONHead(data, req, res);*/
    
    var db = req.db;
    var petCollection = db.get('PetM');
    petCollection.find({},{}, function(e, docs){
        
        if(e != null){
            console.log(e);
        }
        
        var column1 = 0; var column2 = 0; var column3 = 0; var column4 = 0;
        for(var i = 0; i < docs.length; i++){
            switch(docs[i].action){
                case 0:
                    column1++;
                    break;
                case 1:
                    column2++;
                    break;
                case 2:
                    column3++;
                    break;
                case 3:
                    column4++;
                    break;
            }
        }  
        
        var columns = {
            Nap : column1,
            Eat : column2,
            Bathroom : column3,
            Play : column4
        }
        
        //console.log(columns);
        writeJSONHead(columns, req, res);
    });
});

router.get('/petm/json/chart', function(req, res, next){    
    var db = req.db;
    var petCollection = db.get('PetM');
    petCollection.find({},{}, function(e, docs){
        
        if(e != null){
            console.log(e);
        }
        
        var data = [];
        for(var i = 0; i < docs.length; i++){
            data.push(docs[i].action);
        }
        
        var columns = {
            Actions : data
        }
        
        //console.log(columns);
        writeJSONHead(columns, req, res);
    });
});

router.get('/petm/json/median', function(req, res, next){
    var db = req.db;
    var petCollection = db.get('PetM');
    petCollection.find({},{}, function(e, docs){
        
        if(e != null){
            console.log(e);
        }
        
        var data = [];
        for(var i = 0; i < docs.length; i++){
            data.push(docs[i].action);
        }
        
        var s1 = new Stats({bucket_precision: 10});
        s1.push(data);
        var medianValue = s1.median();
        //console.log(columns);
        writeJSONHead({ median : medianValue }, req, res);
    });
});

router.get('/petm/json/deviation', function(req, res, next){
    var db = req.db;
    var petCollection = db.get('PetM');
    petCollection.find({},{}, function(e, docs){
        
        if(e != null){
            console.log(e);
        }
        
        var data = [];
        for(var i = 0; i < docs.length; i++){
            data.push(docs[i].action);
        }
        
        var s1 = new Stats({bucket_precision: 10});
        s1.push(data);
        var deviationValue = s1.σ();
        //console.log(columns);
        writeJSONHead({ deviation : deviationValue }, req, res);
    });
});

/* GET Userlist page. */
router.get('/userlist', function(req, res) {
    var db = req.db;
    var collection = db.get('usercollection');
    collection.find({},{},function(e,docs){
        res.render('userlist', {
            "userlist" : docs
        });
    });
    
    //res.render('index', { title: 'Orbe' });
});

router.post('/petm/json/insert', function(req, res){
    var db = req.db;
    var data = req.body.data;
    
    var petCollection = db.get('PetM');
    
    //console.log(req.body);
    
    //First thing is to remove all data from collection
    petCollection.remove({a:1}, {w:1},function(err, removedDocs){
        if(err){
            console.log(err);
            writeJSONHead({ resultId : 255 }, req, res);
        }else{
            //Insert new data
            petCollection.insert(data, {w:1}, function(err2, result){
                if(err2){
                    console.log(err2);
                    writeJSONHead({ resultId : 1023 }, req, res);
                }else{
                    //console.log(result);
                    writeJSONHead({ resultId : 0 }, req, res);
                }
            });
        }
    });
});

router.post('/petm', function(req, res){
    var db = req.db;
    var petCollection = db.get('PetM');
    petCollection.find({},{}, function(e, docs){
        //console.log(req);
        //console.log(docs);
        var body = { data : docs };
        body.resultId = 1;
        writeJSONHead(body, req, res);
    });
});

router.post('/jsonExample', function(req, res){
    //console.log(req);
    writeJSONHead({ resultId: 25 }, req, res);
});

module.exports = router;

writeJSONHead = function(body, req, res){
    res.json(200, body);
    res.end();
}