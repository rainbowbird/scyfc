# ngrok server setup on Cloud Server

## 1. DNS resolution setup

## 2. Install git and Golang
`$ yum install build-essential golang mercurial git`

## 3. Download ngrok source codes
`$ git clone https://github.com/inconshreveable/ngrok.git`

## 4. Generate self-signed certificate for Base domain
- ngrok需要一个域名作为base域名，ngrok会为客户端分配域名的子域名

- 使用ngrok官方服务时，base域名是ngrok.com，并且使用默认的SSL证书。==现在自建ngrok服务器，需要重新为自己的base域名生成证书==

```shell
# 为base域名tunnel.mydomain.com生成证书
# [ngrok/]目录下执行下列5条语句
$ openssl genrsa -out rootCA.key 2048

$ openssl req -x509 -new -nodes -key rootCA.key -subj "/CN=tunnel.ruananqing.com" -days 5000 -out rootCA.pem
$ openssl genrsa -out device.key 2048

$ openssl req -new -key device.key -subj "/CN=tunnel.ruananqing.com" -out device.csr
$ openssl x509 -req -in device.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out device.crt -days 5000
```

**一定要注意对应的base域名**

执行完上述命令，正常情况下，该目录会多出`device.crt`、`device.csr`、`device.key`、`rootCA.key`、`rootCA.pem`、`rootCA.srl`六个文件，用它们来替换默认的证书文件即可。 
默认的证书文件在`“./assets/client/tls”`和`“./assets/server/tls/”`目录中 

```shell
# 替换默认的证书文件
# [ngrok/]目录下执行下列3条语句，如有需要，按y表示确认覆盖
$ cp rootCA.pem assets/client/tls/ngrokroot.crt
$ cp device.crt assets/server/tls/snakeoil.crt
$ cp device.key assets/server/tls/snakeoil.key
```

## 5. Compile ngrok source files

### 5.1 Compile server side **ngrokd**

```shell
 # 编译ngrokd（服务器端
 # [ngrok/]目录下执行下列语句
 $ make release-server
```

我们可以在`./bin/`目录中找到文件`ngrokd`。可以先运行测试一下，注意，先确保云server下的8888端口没有被占用

```shell
# 运行ngrokd
# [ngrok/]目录下执行下列语句  
$ ./bin/ngrokd -domain="tunnel.ruananqing.com" -httpAddr=":8888"
```

之后退出ngrokd，继续编译ngrok客户端

### 5.2 Compile Linux client ngrok


```shell
# 编译Linux客户端  
# [ngrok/] 目录下执行下列语句  
$ make release-client
```

### 5.3 Compile MacOS client ngrok

类似对windows端操作，命令改成`GOOS=darwin`即可，生成的ngrok文件不带.exe后缀

## 6. Deploy ngrok on server and client

### 6.1 Run server side ngrokd
首先执行云server端ngrokd，这里的8888指的是服务器启用8888端口，就是说内网穿透后的域名为<http://test.tunnel.ruananqing.com:8888>。

如果在80端口未作他用的情况下，也可将8888端口改为80，这样更方便些。而如果我们云server的80端口被占用了，但是我们还想用80端口作为服务端口，那么可以使用==nginx==做一个<http://test.tunnel.ruananqing.com>的反向代理。

```shell
# 执行ngrokd  
# [ngrok/]目录下执行下列语句  
$ ./bin/ngrokd -domain="tunnel.mydomain.com" -httpAddr=":8080"
```

### 6.2 Compose a client side ngrok configuration file  
在ngrok.exe所在目录下建立文件==ngrok.cfg==

```
# 配置文件ngrok.cfg的内容  
#  
server_addr: "tunnel.ruananqing.com:4443"
trust_host_root_certs: false
```

### 6.3 Startup ngrok client for HTTP mapping

 ```shell
# 启动ngrok客户端 
# 注意：如果不加参数-subdomain=test，将会随机自动分配子域名。  
#  
$ ngrok -config=ngrok.cfg -subdomain=test 8888
 ```

## 7. Test  
（此时假设你本地pc的8888端口已经开启了相应的服务），打开浏览器，分别在地址栏中输入（内网）<http://localhost:8888>和(外网)<http://test.tunnel.ruananqing.com:8888>，如果两者显示的内容相同，则证明我们已经成功映射（或者说成功穿透）了。

## 8. Reference  
<https://zhuanlan.zhihu.com/p/49192702>