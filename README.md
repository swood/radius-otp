# radius-otp
Small Python backend to add second factor to your FreeRadius installation

This backend is using the MySQL database which could be defined in config.ini like below:
```
[connection]
user: mysql_user
password: mysql_passwd
host: mysql_host
db: mysql_database
```

The structure of the mysql table is expecting below:

```
CREATE TABLE `vpnusers` (
  `vpn_username` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `pin` varchar(32) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `one_time_code` varchar(128) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `skip_2fa` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`vpn_username`),
  UNIQUE KEY `vpn_username` (`vpn_username`)
) ENGINE=InnoDB AUTO_INCREMENT=1856 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci
```

Also, there is a possibility to configure to skip the second factor when the client does not support 2fa, but still able to auth via password.
Field 'one_time_code' should contain reserve codes like below:
12346,123412,123456

Six numbers with "," as a delimiter.

The configuration of FreeRadius could be like:

```
exec multiotp {
        wait = yes
        input_pairs = request
        output_pairs = reply
	program = "/path/to/main-otp.py --user=%{User-Name} --code=%{User-Password}"
        shell_escape = yes
}
```


