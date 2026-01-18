# 升级 Template

## Step 1 准备升级前

* 确保当前是最新的仓库状态，执行 `git pull`。
* 确保编译通过且所有单元测试通过。
* 确保 `./lint.sh` 通过。
* 确保当前分支没有未提交的更改。
* 备份当前代码库，以防万一。
* 确保你已经安装了最新版本的 Voyager 工具。

接下来，做一些预升级准备。首先打开 Jetbrains Rider, 确保所有 C# 类都是独立的文件（即每个类一个文件），没有多个类定义在同一个文件中。如果有，请将它们拆分为单独的文件。

## Step 2 执行升级

运行下面的脚本：

```bash
#!/bin/bash

# ==========================================
# Aiursoft Template Upgrade Script (Final v2)
# ==========================================

# 遇到错误立即停止
set -e

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ================= 配置区 =================
TEMP_BRANCH_NAME="template-upgrade-layer"
TEMPLATE_NAME="web-app-all-in-one" 
# =========================================

# 1. 环境检查
SLN_FILE=$(find . -maxdepth 1 -name "*.sln" | head -n 1)

if [ -z "$SLN_FILE" ]; then
    echo -e "${RED}Error: No .sln file found in current directory.${NC}"
    exit 1
fi

PROJECT_NAME=$(basename "$SLN_FILE" .sln)
CURRENT_BRANCH=$(git branch --show-current)
CURRENT_DIR=$(pwd)

echo -e "${GREEN}Project:${NC} $PROJECT_NAME"
echo -e "${GREEN}Current Branch:${NC} $CURRENT_BRANCH"

# 检查是否有未提交的更改
if [ -n "$(git status --porcelain)" ]; then 
    echo -e "${RED}Error: You have uncommitted changes.${NC}"
    echo "Please commit or stash your changes before running the merge."
    exit 1
fi

echo -e "${BLUE}=== Step 1: Preparing Orphan Branch ===${NC}"

if git show-ref --verify --quiet "refs/heads/$TEMP_BRANCH_NAME"; then
    git branch -D "$TEMP_BRANCH_NAME"
fi

git checkout --orphan "$TEMP_BRANCH_NAME"
git rm -rf . > /dev/null 2>&1
git clean -fdx > /dev/null 2>&1

echo -e "${BLUE}=== Step 2: Generating Fresh Template in Temp Dir ===${NC}"
GEN_DIR=$(mktemp -d)
pushd "$GEN_DIR" > /dev/null

echo "Generating template '$TEMPLATE_NAME'..."
voyager new -t "$TEMPLATE_NAME" -n "$PROJECT_NAME"

popd > /dev/null

echo -e "${BLUE}=== Step 3: Moving Template Files Back ===${NC}"

if [ -d "$GEN_DIR/.git" ]; then
    rm -rf "$GEN_DIR/.git"
fi

cp -r "$GEN_DIR/." "$CURRENT_DIR/"
rm -rf "$GEN_DIR"

echo -e "${BLUE}=== Step 4: Cleaning Template Noise ===${NC}"

# 4.1 删除模版自带的 Migrations
find . -type d -name "Migrations" -exec rm -rf {} +
echo -e "${YELLOW}Removed template migrations.${NC}"

# 4.2 删除 bin/obj
find . -type d -name "bin" -exec rm -rf {} +
find . -type d -name "obj" -exec rm -rf {} +

# 4.3 删除 所有几乎所有项目都已经被重命名或删除的文件
find . -type f -name "HomeController.cs" -exec rm -f {} +
find . -type f -name "DashboardController.cs" -exec rm -f {} +
find . -type f -name "ViewModelArgsInjector.cs" -exec rm -f {} +
find . -type f -name "README.md" -exec rm -f {} +

# [新增] 4.3 彻底删除模版里的所有 .resx 文件
# 这样合并时，模版侧没有任何资源文件，Git 会完全保留你当前的资源文件，
# 且不会引入任何新的资源文件。
find . -type f -name "*.resx" -exec rm -f {} +
find . -type f -name "*.csproj" -exec rm -f {} +
find . -type f -name "*.png" -exec rm -f {} +
find . -type f -name "*.svg" -exec rm -f {} +
find . -type f -name "package-lock.json“ -exec rm -f {} +
echo -e "${YELLOW}Removed all template .resx files (Keeping yours strictly).${NC}"

echo -e "${BLUE}=== Step 5: Committing Template State ===${NC}"
git add .
git commit -m "chore: generated latest template code for $PROJECT_NAME" --quiet

echo -e "${BLUE}=== Step 6: Merging into $CURRENT_BRANCH ===${NC}"
git checkout "$CURRENT_BRANCH"

# 允许不相关的历史合并
set +e
git merge "$TEMP_BRANCH_NAME" --allow-unrelated-histories --no-commit
MERGE_EXIT_CODE=$?
set -e

# 清理临时分支
git branch -D "$TEMP_BRANCH_NAME" > /dev/null

echo -e "------------------------------------------------"
if [ $MERGE_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}Success! Auto-merged without conflicts.${NC}"
    echo "Check the changes and run 'git commit'."
else
    echo -e "${YELLOW}Merge Conflict Detected! (Expected behavior)${NC}"
    echo -e "This is good. It means git preserved your custom logic while trying to bring in updates."
    echo -e "1. Open your IDE."
    echo -e "2. Look for files with ${RED}red conflict markers${NC}."
    echo -e "3. Note: All .resx files conflicts are gone (we ignored template resx)."
    echo -e "4. Resolve conflicts (Startup.cs, .csproj, etc)."
    echo -e "5. Run 'git add .' and 'git commit'."
fi
```

## Step 3 处理合并冲突

预期会有大量冲突需要手动解决，特别是 `Startup.cs`、`.csproj` 文件等。请按照以下步骤操作：

* 打开你的 IDE（推荐 Visual Studio 或 Jetbrains Rider）。
* 查找所有标记为冲突的文件（通常会有红色标记）。
* 逐个文件解决冲突，确保保留你自己的业务逻辑，同时吸收模版的改进。
* 注意：所有 `.resx` 文件的冲突都已经被忽略，因为我们删除了模版中的所有资源文件，确保你的资源文件不会被覆盖。
* 解决完所有冲突后，运行 `git add .` 然后 `git commit` 完成合并。

如果你使用 Antigravity 或 Cursor 等工具，你可以这样做：

* 打开 Antigravity 或 Cursor。
* 导航到冲突文件。
* 使用下面的提示词：

```markdown
这是一个使用 Aiursoft Template 生成的项目。它在很久之前被从模板（Template）生成了，之后我们开发了大量独有的业务逻辑代码。因此，它和模板关系逐渐变得不同。

现在，我们正在尝试将这个项目升级到最新的模板版本，以利用最新的功能和改进。在这个项目单独发展期间，模板也经历了许多变化。大量基础设施功能都是模板带来的，例如文件上传、文件分发、图片压缩、多数据库支持、身份验证、权限系统、设置系统、后台任务等等……显然，我们不能简单地用最新的模板代码覆盖当前项目代码，因为那样会丢失我们所有的业务逻辑代码。

我们试着重新使用模板对这个项目进行了生成，并将生成的代码与当前的代码进行合并。当然，这产生了大量业务逻辑冲突。

因此，我需要你精细的判断这些冲突，如果是明显的模板带来的基础设施级别的改动提升，请优先选择模板的代码，但模板可能并不完全适用于当前项目，比如模板会改变主页、仪表板主页关系等。这个项目很可能当初根本就没有使用全部的模板功能。总之，对于基础设施的变化，优先尊重模板的改动。

但是，有一些基础设施的改动，又是为了服务特有的业务的，比如额外增加的编译步骤、特定的中间件配置、为基础设施例如用户管理增加额外的API……如果你确定这些都是有用的，这些请优先保留当前项目的代码。我们最高优先级是避免项目崩溃。哪怕一些逻辑你完全不理解，也请优先保留两者中能保证项目正常运行的代码。

大量页面、介绍文字、主页、测试代码、独特的权限、数据库实体等，都是当前项目独有的业务逻辑代码，模板的文件现在突然被覆盖过来，可能看起来好像要删除掉很多重要业务逻辑代码。但请你务必判断，这些业务逻辑代码确实是当前项目独有的，而不是模板带来的。如果是当前项目独有的，请优先保留当前项目的代码。

有些类可能会重复，如果内容完全相同，优先以模板的类为准。如果内容不同，请手动合并，确保保留当前项目的业务逻辑代码，同时吸收模板的改进。

最后，确保项目能通过编译，所有单元测试通过，`./lint.sh` 不报错，并且手动测试关键功能，确保一切正常运行。
```

## Step 4 验证升级结果

* 编译项目，确保没有编译错误。

接下来，你大概率需要为新项目重新创建 Migrations。打开终端，导航到`Sqlite`和`MySQL`项目的目录，分别根据目录中的 README 创建新的初始迁移文件。

然后继续：

* 运行所有单元测试，确保没有测试失败。
* 运行 `./lint.sh`，确保代码风格检查通过。
* 手动测试关键功能，确保一切正常运行。
* 最后，提交你的更改到版本控制系统。

到此，你已经成功将项目升级到最新的模版版本！祝你编码愉快！🚀
