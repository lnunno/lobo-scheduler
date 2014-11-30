conn = new Mongo();
db = conn.getDB("unm_app_db");

/*
Collect stats for the given semester and output to a new collection.
*/
function semester_subject_stats(semester_name, out_name) {
    // Count the number of Spring 2015 courses by subject.
    db.courses.aggregate([{
        $match: {
            semester: semester_name
        }
    }, {
        $group: {
            _id: "$subject_name",
            count: {
                $sum: 1
            }
        }
    }, {
        $sort: {
            "_id": 1
        }
    }, {
        $out: out_name
    }]);
    var acc = [['Subject', 'Number of Classes']];
    db[out_name].find().forEach(function(data) {
        acc.push([data._id, data.count]);
    });
    printjson(acc);
}

function course_time_range(){

}

semester_subject_stats('Spring 2015', 'springCount');
