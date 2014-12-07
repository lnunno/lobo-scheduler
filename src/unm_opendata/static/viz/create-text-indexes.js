conn = new Mongo();
db = conn.getDB("unm_app_db");
db.courses.createIndex({title:'text',description: 'text'});
db.buildings.createIndex({title:'text',description: 'text', abbr: 'text', keywords: 'text'});