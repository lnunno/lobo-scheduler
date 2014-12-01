conn = new Mongo();
db = conn.getDB("unm_app_db");

db.courses.aggregate([{
    $match: {
        semester: "Spring 2015"
    }
}, {
    $group: {
        _id: {
            "subject_name": "$subject_name",
            "level": "$level"
        },
        count: {
            $sum: 1
        }
    },
}, {
    $sort: {
        "_id": 1
    }
}, {
    $out: "subjectByLevel"
}]);

printjson(db['subjectByLevel'].find());
