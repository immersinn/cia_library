# Create pres_briefing_links table for cia database
# http://dev.mysql.com/doc/refman/5.7/en/create-table.html

DROP TABLE IF EXISTS pres_briefing_docs;
#@ _CREATE_TABLE_
CREATE TABLE pres_briefing_links
(
	doc_id		VARCHAR(12),
	title		VARCHAR(100) NOT NULL,
	n_pages		TINYINT(100) UNSIGNED NOT NULL,
	PRIMARY KEY (doc_id)
) ENGINE = InnoDB;
#@ _CREATE_TABLE_
