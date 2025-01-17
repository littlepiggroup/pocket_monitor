DROP VIEW ccmapp_alert;
CREATE VIEW ccmapp_alert AS
SELECT
1 as id,
company_id AS company_id,
project_id AS project_id,
id AS source_id,
status AS status,
status != 'CLOSED' AS is_open,
alert_type AS alert_type,
create_time AS create_time,
update_time AS update_time
FROM ccmapp_samplealert

UNION

SELECT
1 as id,
company_id AS company_id,
project_id AS project_id,
id AS source_id,
status AS status,
status != 'CLOSED' AS is_open,
alert_type AS alert_type,
create_time AS create_time,
update_time AS update_time
FROM ccmapp_videoalert

UNION

SELECT
1 as id,
company_id AS company_id,
project_id AS project_id,
id AS source_id,
status AS status,
status != 'CLOSED' AS is_open,
alert_type AS alert_type,
create_time AS create_time,
update_time AS update_time
FROM ccmapp_temperaturealert

UNION

SELECT
1 as id,
company_id AS company_id,
project_id AS project_id,
id AS source_id,
status AS status,
status != 'CLOSED' AS is_open,
alert_type AS alert_type,
create_time AS create_time,
update_time AS update_time
FROM ccmapp_humidityalert
;


