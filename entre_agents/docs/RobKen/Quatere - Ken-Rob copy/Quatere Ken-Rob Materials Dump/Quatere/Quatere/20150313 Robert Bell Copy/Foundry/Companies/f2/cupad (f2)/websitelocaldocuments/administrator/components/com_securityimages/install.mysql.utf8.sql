CREATE TABLE IF NOT EXISTS `#__security_images_logs`
(`id` int(9) NOT NULL auto_increment,
`wasAccepted` int(1) NOT NULL DEFAULT '1',
`insertDate` varchar(30) NOT NULL, 
`remoteServer` varchar(15) NULL,
`userAgent` varchar(100) NULL,
`referer` varchar(100) NULL,
`text` varchar(100) NULL,
`itemid` int(5) NULL DEFAULT '0', 
PRIMARY KEY (`id`)) 
TYPE=MyISAM;
