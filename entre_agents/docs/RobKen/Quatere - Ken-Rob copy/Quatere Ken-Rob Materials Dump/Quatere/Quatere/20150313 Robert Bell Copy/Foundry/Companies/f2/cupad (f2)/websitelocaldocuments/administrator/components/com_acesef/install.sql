# -----------------------
# AceSEF SQL Installation
# -----------------------
DROP TABLE IF EXISTS `#__acesef_urls`;
CREATE TABLE  `#__acesef_urls` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `url_sef` varchar(255) NOT NULL default '',
  `url_real` varchar(255) NOT NULL default '',
  `metatitle` varchar(255) default '',
  `metadesc` varchar(255) default '',
  `metakey` varchar(255) default '',
  `metalang` varchar(30) default '',
  `metarobots` varchar(30) default '',
  `metagoogle` varchar(30) default '',
  `metacanonical` varchar(255) default '',
  `published` tinyint(3) unsigned NOT NULL default '0',
  `used` tinyint(3) unsigned NOT NULL,
  `locked` tinyint(1) unsigned NOT NULL,
  `blocked` tinyint(1) unsigned NOT NULL default '0',
  `notes` text NOT NULL,
  `sef_tmp_url` varchar(255) NOT NULL default '',
  `checked_out` int(11) NOT NULL,
  `date` date NOT NULL default '0000-00-00',
  PRIMARY KEY  (`id`),
  KEY `url_real` (`url_real`),
  KEY `url_sef` (`url_sef`)
) TYPE=MyISAM CHARACTER SET `utf8`;

DROP TABLE IF EXISTS `#__acesef_routers`;
CREATE TABLE  `#__acesef_routers` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `router_type` int(10) unsigned NOT NULL default '0',
  `rewrite_rule` int(10) unsigned NOT NULL default '0',
  `component_prefix` varchar(255) NOT NULL default '',
  `component` varchar(45) NOT NULL default '',
  `skip_title` tinyint(4) NOT NULL,
  `bypass_post_redirect` tinyint(4) NOT NULL,
  PRIMARY KEY  (`id`)
) TYPE=MyISAM CHARACTER SET `utf8`;

DROP TABLE IF EXISTS `#__acesef_extensions`;
CREATE TABLE  `#__acesef_extensions` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(255) NOT NULL default '',
  `description` text NOT NULL,
  `version` varchar(10) NOT NULL,
  `author` varchar(255) NOT NULL default '',
  `author_url` varchar(255) NOT NULL,
  `params` text NOT NULL,
  `extension` varchar(45) NOT NULL,
  `checked_out` int(11) NOT NULL,
  PRIMARY KEY  (`id`)
) TYPE=MyISAM CHARACTER SET `utf8`;

INSERT INTO `#__acesef_extensions` (`id`, `name`, `params`, `author`, `description`, `version`, `author_url`, `extension`) VALUES
(1, 'News Feeds', 'limitnum=5\n', 'JoomAce LLC', 'News Feeds extension for AceSEF.', '1.0.3', 'www.joomace.net', 'com_newsfeeds'),
(2, 'Web Links', 'limitnum=5\n', 'JoomAce LLC', 'Web Links extension for AceSEF.', '1.0.3', 'www.joomace.net', 'com_weblinks'),
(3, 'User', 'limitnum=5\n', 'JoomAce LLC', 'User extension for AceSEF.', '1.0.1', 'www.joomace.net', 'com_user'),
(4, 'Mailto', 'limitnum=5\n', 'JoomAce LLC', 'Mailto extension for AceSEF.', '1.0.1', 'www.joomace.net', 'com_mailto'),
(5, 'Search', 'limitnum=5\n', 'JoomAce LLC', 'Search extension for AceSEF.', '1.0.3', 'www.joomace.net', 'com_search'),
(6, 'Contact', 'limitnum=5\n', 'JoomAce LLC', 'Contact extension for AceSEF.', '1.0.3', 'www.joomace.net', 'com_contact'),
(7, 'Polls', 'limitnum=5\n', 'JoomAce LLC', 'Polls extension for AceSEF.', '1.0.1', 'www.joomace.net', 'com_poll'),
(8, 'Banners', 'limitnum=5\n', 'JoomAce LLC', 'Banners extension for AceSEF.', '1.0.1', 'www.joomace.net', 'com_banners'),
(9, 'Content', 'limitnum=5\n', 'JoomAce LLC', 'Content (Articles) extension for AceSEF.', '1.0.4', 'www.joomace.net', 'com_content'),
(10, 'Wrapper', 'limitnum=5\n', 'JoomAce LLC', 'Wrapper extension for AceSEF.', '1.0.1', 'www.joomace.net', 'com_wrapper');

INSERT INTO `#__acesef_routers` ( `id`, `router_type`, `rewrite_rule`, `component_prefix`, `component`, `skip_title`, `bypass_post_redirect`) VALUES 
(1, '4', '3', '', 'com_content', '1', '0'),
(2, '4', '3', 'search', 'com_search', '0', '0'),
(3, '4', '3', 'poll', 'com_poll', '0', '0'),
(4, '4', '3', 'user', 'com_user', '0', '0'),
(5, '3', '3', 'mail', 'com_mailto', '0', '0'),
(6, '4', '3', 'banner', 'com_banners', '0', '0'),
(7, '4', '3', '', 'com_contact', '1', '0'),
(8, '4', '3', '', 'com_newsfeeds', '0', '0'),
(9, '4', '3', '', 'com_weblinks', '0', '0');

INSERT INTO `#__plugins` ( `name`, `element`, `folder`, `access`, `ordering`, `published`, `iscore`, `client_id`, `checked_out`, `checked_out_time`, `params`) VALUES ('System - AceSEF', 'acesef', 'system', 0, 7, 1, 0, 0, 0, '0000-00-00 00:00:00', '');