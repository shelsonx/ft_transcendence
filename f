[
    {
        "Name": "ft_transcendence_default",
        "Id": "0db4b0febff276714c3448f1e43e1df26003610ab225856b73ee82b99cc13e46",
        "Created": "2024-04-04T17:59:30.398918332-03:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "172.23.0.0/16",
                    "Gateway": "172.23.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "069d7b3f271e0385beedf62681cc266a6e8dd2b316eee6d7469ea426f83886cd": {
                "Name": "frontend",
                "EndpointID": "3910db905b2496f5e851416317d7baf28c16b2b50d68255883f8890a07413497",
                "MacAddress": "02:42:ac:17:00:04",
                "IPv4Address": "172.23.0.4/16",
                "IPv6Address": ""
            },
            "157a68db97f6fb3d0d8e5fdfefd72541e1ff55f6d98cccfd5ba29b1559acdae1": {
                "Name": "auth-api",
                "EndpointID": "7aca2a5b97ed0ddc1d422b3a8f2ab3ec6e1a5196593ba0ec2f3dbd835df4de30",
                "MacAddress": "02:42:ac:17:00:03",
                "IPv4Address": "172.23.0.3/16",
                "IPv6Address": ""
            },
            "94827d112267bf85d142da8a07731d2a5c01edd5bab847d14e97efdd47d004d4": {
                "Name": "auth-db",
                "EndpointID": "8a1b47cc4fde256ac7ca2188235e9820c1858f8f813d5fffe8df931f0d63bcbc",
                "MacAddress": "02:42:ac:17:00:02",
                "IPv4Address": "172.23.0.2/16",
                "IPv6Address": ""
            }
        },
        "Options": {},
        "Labels": {
            "com.docker.compose.network": "default",
            "com.docker.compose.project": "ft_transcendence",
            "com.docker.compose.version": "2.20.3"
        }
    }
]
