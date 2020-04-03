# Run a Flask App

## 1. 创建程序实例

```python
# app.py

from flask import Flask
app = Flask(__name__)
```

 传入Flask类构造方法的第一个参数是模块或包的名称，我们应该使用特殊变量\_\_name\_\_。Python会根据所处的模块来赋予\_\_name\_\_变量相应的值，对于我们的程序来说（app.py），这个值为app。除此之外，这也会帮助Flask在相应的文件夹里找到所需的资源，比如模版核静态文件。

## 2. 注册路由

## 3. 启动开发服务器

Flask内置了一个简单的开发服务器（由依赖包Werkzeug提供），足够在开发和测试阶段使用。

### 3.1 启动

Flask通过依赖包Click内置了一个CLI系统。

当我们安装Flask后，会自动添加一个==flask命令脚本==，我们可以通过**flask命令**执行内置命令，扩展提供的命令或事我们自己定义的命令。其中，`flask run`命令用来启动内置的开发服务器。

```shell
flask run
```

`flask run`命令运行的开发服务器默认会监听http://172.0.0.1:5000/地址（按Ctrl+C退出），并开启多线程支持。

#### 3.1.1 自动发现程序实例

一般来说，在执行`flask run`命令运行程序前，我们需要提供程序实例所在模块的位置。

Flask会自动探测程序实例，**自动探索**存在下面这些规则：

- 从当前目录寻找`app.py`和`wsgi.py`模块，并从中寻找名为app或application的程序实例。
- 从环境变量`FLASK_APP`对应的值寻找名为app或application的程序实例。

#### 3.1.2 管理环境变量

如果安装了`python-dotenv`，那么在使用`flask run`或其它命令时Flask程序会使用它自动从`.flaskenv`文件和`.env`文件中加载环境变量。

> 当安装了`python-dotenv`，Flask在加载环境变量的优先级是：手动设置的环境变量>`.env`中设置的环境变量>`.flaskenv`设置的环境变量

`.flaskenv`用来存储和Flask相关的公开环境变量，比如`FLASK_APP`

`.env`用来存储包含敏感信息的环境变量

`==.env`包含敏感信息，除非是私有项目，否则绝对不能提交到Git仓库中==。

#### 3.1.3 更多启动选项

- 使服务器外部可见

  在`run`命令后添加`--host`选项将主机地址设为0.0.0.0使其对外可见

- 改变默认端口

  在`run`命令后添加`--port`选项来改变它

> 执行`flask run`命令时的`host`和`port`选项也可以通过环境变量`FLASK_RUN_HOST`和`FLASK_RUN_PORT`设置。
>
> Flask内置的命令都可以使用这种模式定义默认选项值，即`FLASK_<COMMAND>_<OPTION>`

#### 3.1.4 设置运行环境

Flask提供了一个`FLASK_ENV`环境变量用来设置环境，默认为`production`。在开发时，我们可以将其设置为`development`，这会开启所有支持开发的特性。

在开发环境下，调试模式（Debug Mode）将被开启，这时执行`flask run`启动程序会自动激活Werkzeug内置的**调试器**（debugger）和**重载器**（reloader）。

## 4. Python Shell

`Python Shell`，即Python交互式解释器

在开发Flask程序时，我们并不会直接使用`python`命令启动`Python Shell`，而是使用`flask shell`命令

```shell
flask shell
```

使用`flask shell`命令打开的`Python Shell`自动包含**程序上下文**，并且已经导入了app实例。

上下文（context）可以理解为环境。在Flask中，上下文有两种，分别为==程序上下文==和==请求上下文==。

## 5. Flask 扩展

## 6. 项目配置

在Flask中，==配置变量==就是一些大写形式的Python变量，也可以称之为配置参数或配置键。

在一个项目中，你会用到许多配置。这些配置变量都通过Flask对象的`app.config`属性作为统一的接口来设置和获取，它指向的`Config类`实际上是字典的子类，所以你可以像操作其他字典一样操作它。

## 7. URL与端点

Flask提供的`url_for()`函数获取URL，当路由中定义的URL规则被修改时，这个函数总会返回正确的URL。

调用`url_for()`函数时，第一个参数为**端点**（endpoint）值。

==在Flask中，端点用来标记一个`视图函数`以及对应的`URL规则`。端点的默认值为视图函数的名称==。

如果URL含有动态部分，那么我们需要在`url_for()`函数里传入相应的参数。

> 使用`url_for()`函数生成的URL是**相对URL**（即内部URL）。，即URL中的path部分。相对URL只能在程序内使用。
>
> 如果想要生成供外部使用的**绝对URL**，可以在使用`url_for()`函数时，将`_external`参数设为True，这会生成完整的URL。

## 8. Flask命令

除了Flask内置的`flask run`等命令，我们也可以自定义命令。

通过创建任意一个函数，并为其添加`app.cli.command()`装饰器，我们就可以注册一个flask命令。

```python
@app.cli.command()
def hello():
	clcik.echo('Hello, Human')
```

函数的名称即为命令名称。你也可以在`app.cli.command()`装饰器中传入参数来设置命令名称。

命令函数的文档字符串会作为命令的帮助信息显示。

## 9. 模版与静态文件

模版即包含程序页面的HTML文件。静态文件则是需要在HTML文件中加载的CSS和JavaScript文件，以及图片，字体文件等资源文件。

默认情况下，模版文件存放在项目根目录中的templates文件夹中，静态文件存放在static文件夹下，这两个文件夹需要和包含程序实例的模版处于同一个目录下。