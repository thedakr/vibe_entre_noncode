DELETE FROM `#__plugins` WHERE element = 'acesef';

DROP TABLE IF EXISTS `#__acesef_extensions_backup`;
RENAME TABLE `#__acesef_extensions` TO `#__acesef_extensions_backup`;

DROP TABLE IF EXISTS `#__acesef_routers_backup`;
RENAME TABLE `#__acesef_routers` TO `#__acesef_routers_backup`;

DROP TABLE IF EXISTS `#__acesef_urls_backup`;
RENAME TABLE `#__acesef_urls` TO `#__acesef_urls_backup`;