# Aiursoft Entity Framework Core 实体建模规范

## 核心哲学：独裁模式 (Dictator Mode)

1.  **DbSet 独裁**：数据的增删改（CUD）必须通过 `DbContext.DbSet<T>` 进行。
2.  **显式加载**：禁止任何形式的隐式行为（如延迟加载），数据必须显式 `Include`。
3.  **编译期契约**：利用 C\# 类型系统（Type System）在编译期暴露潜在错误，而不是推迟到运行期。
4.  **表格可见**: 所有实体类必须清晰地表达其数据列和关系，避免隐式约定。所有实体类必须出现在 `DbContext` 中的 `public DbSet<Repo> Repos => Set<Repo>();`，表名必须是实体类名的复数形式（如 `User` 对应 `Users` 表）。

-----

## 1\. 主键规范 (Primary Keys)

**1.1 类型限制**
所有实体类的主键必须是 `int` 或 `Guid` 类型。

  * **例外**：直接继承自 `Microsoft.AspNetCore.Identity.IdentityUser` 的实体除外（默认使用 `string`，允许保持原样）。

**1.2 强制特性**
所有实体类的主键必须被 `[Key]` Attribute 修饰。

**1.3 不可变性**
所有实体类的主键必须是 `{ get; init; }`（创建后不可变）。

> **示例：**
>
> ```csharp
> [Key]
> public Guid Id { get; init; }
> ```

-----

## 2\. 外键与导航规范 (Foreign Keys & Navigation)

**2.1 成对定义**
所有外键关系必须显式定义两个属性：**外键ID** 和 **导航引用**。

**2.2 外键ID 必填性**

  * **必填关系**：外键ID 必须是 `Guid`，`string` 或 `int`，且属性必须是 `required`。此时，外键是不可空的。
  * **可选关系**：外键ID 必须是 `Guid?`, `string?` 或 `int?`，且属性必须是 `required`。此时，外键是可空的。

**2.3 导航引用可空性**

所有**导航引用属性**必须声明为**可空类型**（如 `User?`）,即使设计上不可能为空。这是考虑到实例化的时候不可能为它有合理的值，因此必须可空。实际上，如果此导航属性不可空，是永远不会返回空的。

  * *理由*：在 `new Entity()` 时我们通常只赋值 ID 而不赋值对象，声明为可空是为了满足 C\# 编译器的初始化检查，避免虚假的警告。

**2.4 导航属性必须 NotNull**
所有**导航引用属性**，如果一定不为空，则必须被 `[NotNull]` 修饰。

**2.5 序列化屏蔽**
所有**导航引用属性**必须被 `[Newtonsoft.Json.JsonIgnore]` 修饰（防止死循环）。

**2.6 禁止 Virtual (禁止延迟加载)**
所有导航属性**严禁**使用 `virtual` 关键字。

  * *后果*：彻底禁用 Lazy Loading Proxy。
  * *操作要求*：查询关联数据时，必须显式调用 `.Include()` 和 `.ThenInclude()`。

> **示例：**
>
> ```csharp
> // 外键 ID (必填)
> public required Guid UserId { get; set; }
>
> // 导航引用 (必须可空，必须 NotNull，禁止 virtual)
> [JsonIgnore]
> [ForeignKey(nameof(UserId))]
> [NotNull] // 不可空的，加 [NotNull]
> public User? User { get; set; } // 不可空的，也要加问号。
> ```

-----

## 3\. 集合与独裁规范 (Collections & Dictatorship)

**3.1 类型限制**
所有反向导航集合必须声明为 `IEnumerable<T>` 类型。

  * *目的*：在编译层面阉割集合的 `.Add()` 和 `.Remove()` 方法。

**3.2 初始化**
所有集合属性必须初始化为 `new List<T>()` 以防止空引用异常。

**3.3 显式关联**
所有集合属性必须被 `[InverseProperty]` 修饰。

**3.4 独裁修改原则**
禁止将 `IEnumerable` 强转为 `List` 来操作数据。

  * **增加子项**：必须创建新对象并 `_dbContext.Add(newItem)`。
  * **删除子项**：必须查询出对象并 `_dbContext.Remove(item)`。

> **示例：**
>
> ```csharp
> [InverseProperty(nameof(ExamPaperSubmission.User))]
> public IEnumerable<ExamPaperSubmission> Submissions { get; init; } = new List<ExamPaperSubmission>();
> ```

-----

## 4\. 数据列规范 (Data Columns)

**4.1 长度约束**
所有 `string` 或 `byte[]` 类型的列必须被 `[MaxLength]` 约束。

**4.2 空值语义**

  * **不可空列**：使用非空类型（如 `string`），严禁使用 `[NotNull]` 修饰可空类型。
  * **可空列**：使用可空类型（如 `string?`），且必须在 XML 注释中说明**为空代表什么业务状态**。

**4.3 不可变属性**
所有业务上不可编辑的属性（如 `CreationTime`），必须是 `{ get; init; }`。

-----

## 5\. 完整标准模板 (V3.0)

```csharp
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Diagnostics.CodeAnalysis; // 尽量少用，除非用于辅助方法
using Newtonsoft.Json;

namespace Aiursoft.Exam.Entities;

public class TemplateEntity
{
    // [规则 1.1, 1.2, 1.3] 主键：Guid/int, Key, init
    [Key]
    public Guid Id { get; init; }

    // [规则 4.1, 4.2] 必填列：required string, MaxLength, 禁止 [NotNull]
    [MaxLength(100)]
    public required string Name { get; set; }

    // [规则 4.2, 4.3] 可空列：string?, 注释说明含义, init (如果是创建时不变量)
    /// <summary>
    /// 描述信息。
    /// 若为空，表示用户在创建时未填写备注。
    /// </summary>
    [MaxLength(1000)]
    public string? Description { get; init; }

    // [规则 4.3] 系统字段
    public DateTime CreationTime { get; init; } = DateTime.UtcNow;

    // ================= 关联关系 =================

    // [规则 2.2] 外键ID：required (即使是 Guid? 也要 required 以强制显式赋值)
    public required Guid ParentId { get; set; }

    // [规则 2.3, 2.4, 2.5, 2.6] 
    // 导航引用：Type?, JsonIgnore, ForeignKey, NotNull
    // 严禁 virtual (禁用延迟加载)
    [JsonIgnore]
    [ForeignKey(nameof(ParentId))]
    [NotNull]
    public ParentEntity? Parent { get; set; }

    // [规则 3.1, 3.2, 3.3] 
    // 集合：IEnumerable (独裁模式), InverseProperty, new List()
    // 严禁 virtual
    [InverseProperty(nameof(ChildEntity.Parent))]
    public IEnumerable<ChildEntity> Children { get; init; } = new List<ChildEntity>();
}
```