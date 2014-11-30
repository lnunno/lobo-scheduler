conn = new Mongo();
db = conn.getDB("unm_app_db");
var result = db.courses.aggregate([{
    $unwind: "$sections"
}, {
    $unwind: "$sections.meeting_times"
}, {
    $group: {
        _id: "$sections.meeting_times.start_time_hour",
        count: {
            $sum: 1
        }
    }
}, {
    $sort: {
        "_id": 1
    }
}, {
    $out: "classStartTimes"
}]);

var acc = [
    ['Hour', 'Number of Sections']
];
db['classStartTimes'].find().forEach(function(data) {
    acc.push([data._id, data.count]);
});
printjson(acc);