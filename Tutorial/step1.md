# 开始之前

这里是 Aiursoft Template 的快速入门教程。我们都知道，开始一个新项目可能会很麻烦，所以我们准备了这个教程来帮助你快速上手。

这个教程预计需要 30 分钟。在你完成后，你将拥有一个功能齐全的项目，可以作为你未来项目的基础。我们为了展示，将简单开发一个带数据库、RBAC的 markdown 转 HTML 的简单笔记应用。

# Aiursoft Template Tutorial - Step 1

## Step 1.1 准备开发环境

第一步的目标是创建一个全新的项目。我们推荐你使用 [AnduinOS](https://www.anduinos.com) 来进行实战开发，因为 AnduinOS 非常容易安装 dotnet、bash、npm、git、docker、mysql、nginx 等工具。

如果你不想使用 AnduinOS，你也可以在任何支持 .NET 8.0 的操作系统上进行开发。

在开始之前，请确保你已经安装了 `git`、`.NET 9.0 SDK` 和 `docker`。在 AnduinOS 上，你可以使用以下命令安装这些工具：

```bash
sudo apt install -y git dotnet9 docker.io
```

安装 git 后，你必须配置你的用户名和邮箱：

```bash
git config --global user.name "Your Name"
git config --global user.email "YourEmail@domain.com"
```

你还需要安装 Node.js 和 npm 以管理前端的依赖。你可以使用以下命令安装它们：

```bash
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg --yes
NODE_MAJOR=22
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
sudo apt update
sudo apt install nodejs -y
node -v
```

你还需要一个代码编辑器。我们推荐使用 [Visual Studio Code](https://code.visualstudio.com/) 或 [Jetbrains Rider](https://docs.anduinos.com/Applications/Code-Editors/Jetbrains-Rider/Jetbrains-Rider.html)。你也可以使用以下命令安装 Visual Studio Code：

```bash
cd ~
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
rm -f packages.microsoft.gpg
sudo apt update
sudo apt install code -y
```

安装完成后，你可以通过运行 `code` 命令来启动 Visual Studio Code。

为了新建 Aiursoft Template 的项目，你需要安装 Voyager，它是 Aiursoft Template 的脚手架工具。你可以通过以下命令安装它：

```bash
dotnet tool install --global Aiursoft.Voyager
voyager --version
```

如果上面过程一切顺利，你现在应该已经安装好了所有必要的工具，可以开始创建你的第一个 Aiursoft Template 项目了！

## Step 1.2 创建新项目

首先，创建一个新的文件夹来存放你的项目：

```bash
mkdir MyOrg.MarkToHtml
cd MyOrg.MarkToHtml
```

然后使用 voyager 初始化项目：

```bash
voyager new -t web-app-all-in-one
```

你会注意到下面文件被生成：

```bash
.
├── CODE_OF_CONDUCT.md
├── Dockerfile
├── .editorconfig
├── .git
├── .gitignore
├── .gitlab-ci.yml
├── install.sh
├── LICENSE
├── MyOrg.MarkToHtml.sln
├── ninja.yaml
├── nuget.config
├── README.md
├── src
│   ├── MyOrg.MarkToHtml
│   ├── MyOrg.MarkToHtml.Entities
│   ├── MyOrg.MarkToHtml.InMemory
│   ├── MyOrg.MarkToHtml.MySql
│   └── MyOrg.MarkToHtml.Sqlite
└── tests
    ├── IntegrationTests
    └── MyOrg.MarkToHtml.Tests.csproj

15 directories, 17 files
```

其中未必所有文件都对你有用，下面是每个文件的简要说明，你可以删除不需要的文件：

* CODE_OF_CONDUCT.md: 代码行为准则，这只是一个示例。你可以放心的删除它而不影响项目。
* Dockerfile: 用于在 Docker 容器中运行应用的配置文件。它定义了如何在 Docker 里构建和运行应用的环境。
* .editorconfig: 代码风格配置文件，帮助你和你的团队保持一致的代码风格。你可以根据需要修改或删除它。
* .git: Git 版本控制的元数据文件夹。新创建项目时会自动生成，也会帮你生成一个初始的 commit。
* .gitignore: Git 忽略文件列表，指定哪些文件或文件夹不应被 Git 追踪。请不要删除它。
* .gitlab-ci.yml: GitLab CI/CD 的配置文件。如果你使用 GitLab 进行持续集成和部署，这个文件会定义你的流水线。如果你不使用 GitLab，可以删除它。
* install.sh: 一个简单的快速部署脚本，帮助你在无 Docker 的服务器上快速部署项目。你可以根据需要修改或删除它。
* LICENSE: 许可证文件，说明项目的使用和分发条款。你可以根据需要修改或删除它。
* MyOrg.MarkToHtml.sln: 这是 Visual Studio 的解决方案文件，包含了项目中的所有子项目。请不要删除它。
* ninja.yaml: 这是用于给 nuget ninja 看的配置文件，定义了项目的文件结构。如果你不使用 nuget ninja，可以删除它。
* README.md: 项目的自述文件，包含项目的基本信息和使用说明。你可以根据需要修改它。
* nuget.config: NuGet 包管理器的配置文件，定义了包源和其他设置。如果你不需要自定义包源，可以删除它。
* src/: 这个文件夹包含了项目的源代码。你会看到多个子项目文件夹，每个文件夹对应一个功能模块。你可以根据需要添加或删除子项目。
* tests/: 这个文件夹包含了项目的测试代码。你可以根据需要添加或删除测试项目。

接下来，你可以使用 Visual Studio Code 或 Jetbrains Rider 打开这个 `MyOrg.MarkToHtml.sln` 解决方案文件，开始编写代码了！
