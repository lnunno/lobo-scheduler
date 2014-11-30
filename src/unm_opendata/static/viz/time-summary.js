conn = new Mongo();
db = conn.getDB("unm_app_db");
var acc = {
    'Morning':0,
    'Mid-day':0,
    'Afternoon':0
};
db['classStartTimes'].find().forEach(function(data) {
    var startTime = data._id;
    var count = data.count;
    if(!startTime || startTime < 6){
        
    }
    else if(startTime <= 10){
        acc['Mid-day'] += count;
    }
    else if(startTime <= 13){
        acc['Afternoon'] += count;
    }
    else{
        acc['Morning'] += count;
    }
});
printjson(acc);