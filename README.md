# python-otp-services
```shell
nameko shell --broker amqp://guest:guest@localhost
```
```
n.rpc.otp.create("email@domain.local")
n.rpc.otp.delete("email@domain.local")
n.rpc.otp.authen("email@domain.local", "otp")
```
