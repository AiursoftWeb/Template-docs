# Aiursoft Template Tutorial - Step 6 - 管理员看板和全新的权限

作为站长，你可能希望有一个专门的管理员看板，用于管理用户和内容。你也可能希望有一些特殊的权限设置，例如调整一篇文档的所有者，或者让某些用户拥有更高的权限。我们将在这一步中实现这些功能。

因此，在这一章节，我们将介绍权限系统的设计思路，并实现一个简单的管理员看板。

## Step 6.1 理解 Aiursoft Template 的权限系统

在继续之前，我们需要理解 Aiursoft Template 的权限系统是基于角色 `Role` 的。每个用户 `User` 可以拥有多个角色，每个角色可以拥有多个权限 `Claim`。

其中，`User` 和 `Role` 之间是多对多的关系，而 `Role` 和 `Claim` 之间也是多对多的关系。

`User` 和 `Role` 是存储在数据库中的。程序第一次启动，会创建一个默认的 `Admin` 角色，和叫 `Administrators` 的权限组。

下面，我们阅读这部分核心代码，找到文件 `./src/MyOrg.MarkToHtml/ProgramExtends.cs`，找到其中的 `SeedAsync` 方法：

```csharp title="ProgramExtensions.cs 无需要修改"
var role = await roleManager.FindByNameAsync("Administrators");
if (role == null)
{
    role = new IdentityRole("Administrators");
    await roleManager.CreateAsync(role);
}

var existingClaims = await roleManager.GetClaimsAsync(role);
var existingClaimValues = existingClaims
    .Where(c => c.Type == AppPermissions.Type)
    .Select(c => c.Value)
    .ToHashSet();

foreach (var permission in AppPermissions.GetAllPermissions())
{
    if (!existingClaimValues.Contains(permission.Key))
    {
        var claim = new Claim(AppPermissions.Type, permission.Key);
        await roleManager.AddClaimAsync(role, claim);
    }
}

if (!await db.Users.AnyAsync(u => u.UserName == "admin"))
{
    var user = new User
    {
        UserName = "admin",
        DisplayName = "Super Administrator",
        Email = "admin@default.com",
    };
    _ = await userManager.CreateAsync(user, "admin123");
    await userManager.AddToRoleAsync(user, "Administrators");
}
```

上面的代码会在程序第一次运行时执行。它会在启动时确保 `Administrators` 角色存在，并且包含所有的权限。它还会确保存在一个用户名为 `admin` 的用户，并将其添加到 `Administrators` 角色中。

!!! info "Administrators 用户组并没有任何特殊性"

    在第一次启动后，`Administrators` 角色并没有任何特殊性。它只是一个普通的角色，唯一的区别是它被赋予了所有的权限。你可以创建其他角色，并赋予它们不同的权限。或删除这个自动创建的角色。

    并不会，也不应当有任何业务逻辑，强制要求一个用户必须属于 `Administrators` 角色才能执行某些操作。权限系统是完全基于权限 `Claim` 来控制的，而不是 `Role`。

和 `User` `Role` 不同，`Claim` 并不直接存储在数据库中，而是存储在代码中。你可以在 `./src/MyOrg.MarkToHtml/AppPermissions.cs` 文件中找到所有的权限定义。

我们也可以修改上述文件，以添加新的权限。

!!! note "新添加的权限 `Claim` 不会自动分配给任何角色 `Role`"

    如果你添加了新的权限，你需要手动将它们分配给某个角色 `Role`，否则没有任何用户会拥有这个权限。

## Step 6.2 设计权限系统

首先，我们需要确定我们需要哪些权限。在这个例子中，我们将设计三个非常高的权限，以允许特定用户执行一些敏感操作：

* 查看所有用户的文档
* 任意编辑一个用户的文档
* 删除任意用户的文档

!!! tip "基础功能还需要设计权限吗？"

    你可能会好奇，基础功能（例如创建、编辑、删除自己的文档）是否也需要设计权限？在我们的例子中，我们允许了所有用户(甚至匿名用户)创建文档，因此这类可以无条件服务的用例不需要权限。

修改文件 `./src/MyOrg.MarkToHtml/AppPermissionNames.cs`，添加新的权限：

```csharp title="AppPermissions.cs 新增权限"
// Document Management
public const string CanReadAllDocuments = nameof(CanReadAllDocuments);
public const string CanDeleteAnyDocument = nameof(CanDeleteAnyDocument);
public const string CanEditAnyDocument = nameof(CanEditAnyDocument);
```

修改后，这个文件应该如下所示：

```csharp title="AppPermissions.cs 完整代码"
namespace MyOrg.MarkToHtml.Authorization;

/// <summary>
/// Defines all permission keys as constants. This is the single source of truth.
/// </summary>
public static class AppPermissionNames
{
    // User Management
    public const string CanReadUsers = nameof(CanReadUsers);
    public const string CanDeleteUsers = nameof(CanDeleteUsers);
    public const string CanAddUsers = nameof(CanAddUsers);
    public const string CanEditUsers = nameof(CanEditUsers);
    public const string CanAssignRoleToUser = nameof(CanAssignRoleToUser);

    // Role Management
    public const string CanReadRoles = nameof(CanReadRoles);
    public const string CanDeleteRoles = nameof(CanDeleteRoles);
    public const string CanAddRoles = nameof(CanAddRoles);
    public const string CanEditRoles = nameof(CanEditRoles);

    // System Management
    public const string CanViewSystemContext = nameof(CanViewSystemContext);
    public const string CanRebootThisApp = nameof(CanRebootThisApp);

    // Document Management
    public const string CanReadAllDocuments = nameof(CanReadAllDocuments);
    public const string CanDeleteAnyDocument = nameof(CanDeleteAnyDocument);
    public const string CanEditAnyDocument = nameof(CanEditAnyDocument);
}
```

接下来，修改文件 `./src/MyOrg.MarkToHtml/AppPermissions.cs`，将新的权限添加到权限列表中：

```csharp title="AppPermissions.cs 新增权限"
new(AppPermissionNames.CanReadAllDocuments,
    localizer["Read All Documents"],
    localizer["Allows viewing all documents in the system, regardless of ownership."]),
new(AppPermissionNames.CanDeleteAnyDocument,
    localizer["Delete Any Document"],
    localizer["Allows deletion of any document, regardless of ownership."]),
new(AppPermissionNames.CanEditAnyDocument,
    localizer["Edit Any Document"],
    localizer["Allows editing of any document, regardless of ownership."]),
```

这里构造的 `PermissionDescriptor` 包含三个参数：

* Key 权限的唯一标识符（字符串）
* Name 权限的名称（本地化字符串）
* Description 权限的描述（本地化字符串）

每次新增一个权限，都应当完整的填写这三个参数以描述它的功能。

## Step 6.3 为 Administrators 角色分配新权限

接下来，我们需要将新添加的权限分配给 `Administrators` 角色。无需修改任何代码，直接启动应用程序。

!!! tip "为什么这次需要手动分配权限？"

    虽然程序会在第一次启动时创建 `Administrators` 角色并分配所有权限，但如果你是在程序已经运行过一次之后添加的新权限，程序不会自动将这些新权限分配给 `Administrators` 角色。

我们需要手工来到 `Roles` 页面，找到 `Administrators` 角色，然后点击 `Edit this Role` 按钮。

在编辑角色页面中，找到新添加的权限，并勾选它们，然后点击 `Save Changes` 按钮保存更改。
