conn = new Mongo();
db = conn.getDB("unm_app_db");
db.courses.createIndex({title:'text',description: 'text'});