# Aiursoft Template Tutorial - Step 7 - 增加全新的配置项目，并支持环境变量

作为站长，有一些应用的配置可能默认配置并不能满足。我们需要允许管理员自己可以调整一些配置项目，来改变应用的默认行为，例如：

* 允许或禁止注册新用户。
* 允许或禁止匿名用户使用应用。
* 允许或禁止用户删除自己的内容。

## Step 7.1 - 理解 ASP.NET Core 的配置系统 (可选)

Aiursoft Template 使用 ASP.NET Core 自带的配置系统。配置系统允许我们从多种来源加载配置数据，例如：

* appsettings.json 文件
* appsettings.{Environment}.json 文件，也就是在开发环境中，appsettings.Development.json 文件，而在生产环境中，appsettings.Production.json 文件。
* 环境变量
* 命令行参数

一般的，我们使用 `appsettings.json` 文件进行本地开发时配置。

!!! tip "方便 Docker 部署的用户直接编辑配置"

    实际在 Docker 中部署时，`appsettings.json` 文件会穿透到 `/data` 目录下，我们可以直接修改这个文件来改变配置。

    因此，我们非常建议 Docker 用户在部署时，将主机上的一个路径挂载到容器的 `/data` 目录下，这样就可以直接编辑主机上的配置文件来改变容器内的配置。

!!! warning "注意：每次修改配置文件后都需要重启应用"

    ASP.NET Core 的配置系统不会自动监视配置文件的变化，因此每次修改配置文件后都需要重启应用，才能让新的配置生效。

!!! question "问题：我可以在配置中包含敏感信息吗？"

    敏感信息例如数据库连接字符串、API 密钥等，建议不要直接写在配置文件中，而是使用环境变量来传递这些信息。这样可以方便 Renew 的时候快速根据声明式的配置而重新生成配置，而不需要担心敏感信息泄露。

例如，现在我们可以尝试禁止应用程序的登录注册功能。

首先使用第一种方法，打开 `./src/MyOrg.MarkToHtml/appsettings.json` 文件，将它的 `AppSettings:Local:AllowRegister` 项设置为 `false`

此时，这个 JSON 可能是下面的样子：

```json title="禁止注册的 appsettings.json"
{
  "ConnectionStrings": {
    "AllowCache": "True",
    "DbType": "Sqlite",
    "DefaultConnection": "DataSource=app.db;Cache=Shared"
  },
  "Storage": {
    "Path": "/tmp/data"
  },
  "AppSettings": {
    "AuthProvider": "Local", // OIDC or Local
    "DefaultRole": "",
    "PersistsSignIn": false,
    "OIDC": {
      // https://auth.aiursoft.cn/application/o/template
      "Authority": "https://auth.aiursoft.cn/application/o/template",
      "ClientId": "",
      "ClientSecret": "",
      "RolePropertyName": "groups",
      "UsernamePropertyName": "preferred_username",
      "UserDisplayNamePropertyName": "name",
      "EmailPropertyName": "email",
      "UserIdentityPropertyName": "sub"
    },
    "Local": {
      "AllowRegister": false,
    }
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}
```

保存文件后，重启应用。我们会注意到，注册按钮已经消失了。

类似的，我们也可以使用环境变量来覆盖配置文件中的配置。

这一次，我们回滚`appsettings.json` 文件中的配置，考虑到环境变量拥有更高的优先级，我们可以直接设置环境变量 `AppSettings__Local__AllowRegister` 为 `false` 来禁止注册功能。

!!! note "环境变量的优先级最高"

    ASP.NET Core 的配置系统中，环境变量的优先级高于配置文件中的配置，因此我们可以使用环境变量来覆盖配置文件中的配置。

    在上面的例子中，即使我们把 `appsettings.json` 文件中的 `AppSettings:Local:AllowRegister` 设置为 `true`，但是只要我们设置了环境变量 `AppSettings__Local__AllowRegister` 为 `false`，注册功能依然会被禁止。

    因此，在生产环境，尤其是 Docker 部署中，我们推荐全部使用环境变量来配置应用，而不是直接修改配置文件。

这一次，使用下面的命令来启动项目：

```bash
cd ./src/MyOrg.MarkToHtml
AppSettings__Local__AllowRegister=false dotnet run
```

!!! tip "注意环境变量的命名规则"

    在环境变量中，使用双下划线 `__` 来表示配置项的层级关系。例如，`AppSettings:Local:AllowRegister` 在环境变量中表示为 `AppSettings__Local__AllowRegister`。

同样会注意到，注册按钮已经消失了。

在实际生产中，我们推荐使用环境变量来配置，这样方便版本控制我们的配置信息。

## 7.2 - 添加一个新的配置项目

上面的例子中，我们演示了一个已经被应用程序支持好的配置项目 `AppSettings:Local:AllowRegister`，但是如果我们需要全新添加一个配置项目呢？

下面，我们将以 `AppSettings:AllowAnonymousUsage` 为例，来演示如何添加一个新的配置项目，并在代码中使用它。

首先，编辑