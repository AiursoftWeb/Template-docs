# Aiursoft Template Tutorial - Step 12 - 发布应用到真实的服务器

### 

在使用 OIDC 部署以后，第一次登录的用户，如果不在 `Administrators` 这个系统自动创建的角色中，是没有任何权限的。我们需要给用户分配一些权限，才能让用户正常使用系统。

假设目标企业里，我们需要允许所有员工都是这个系统的最高管理员，而员工来自与 OIDC 的 `employees` 这个角色。我们需要把 `employees` 这个角色的所有权限都赋予给 `employees` 这个角色。

这种情况下，可以使用下面的 SQL 语句来完成这个任务：

```sql
-- 步骤 1: 查询名为 'employees' 的角色的 ID，并将其存储在一个变量中
SET @roleId = (SELECT Id FROM AspNetRoles WHERE Name = 'employees');

-- 步骤 2: 为 'employees' 角色插入所有可能的权限
-- 这段代码会从 AspNetRoleClaims 表中复制所有不重复的 ClaimType 和 ClaimValue 组合
-- 并使用 WHERE NOT EXISTS 子句来确保不会重复添加已经存在的权限
INSERT INTO AspNetRoleClaims (RoleId, ClaimType, ClaimValue)
SELECT
    @roleId,
    c.ClaimType,
    c.ClaimValue
FROM
    (SELECT DISTINCT ClaimType, ClaimValue FROM AspNetRoleClaims) AS c
WHERE NOT EXISTS (
    SELECT 1
    FROM AspNetRoleClaims
    WHERE RoleId = @roleId
      AND ClaimType = c.ClaimType
      AND ClaimValue = c.ClaimValue
);
```

执行完上面的 SQL 语句以后，`employees` 这个角色就拥有了所有的权限。这样，所有登录的员工都可以使用这个系统的所有功能。

!!! note "已经登录的用户"

    如果用户已经登录过一次，那么需要用户重新登录一次，才能获得新的权限。