# 全局设置

全局设置功能允许您在不重新部署应用程序的情况下动态管理应用程序配置。它支持分层配置系统，有效结合了静态配置（如 `appsettings.json` 或环境变量）与存储在数据库中的动态设置。

## 配置优先级

应用程序按以下优先级顺序解析设置值：

1.  **配置（环境变量 / AppSettings）**：
    如果某个键存在于 `appsettings.json` 中或作为环境变量设置，则此值具有最高优先级。
    *   格式：`GlobalSettings:Key`。
    *   *注意：如果在此处找到设置，它将在数据库界面中变为只读，以避免混淆。*

2.  **数据库**：
    如果在配置中未找到，应用程序将检查数据库中是否存储了该值。此值可通过管理员仪表板进行编辑。

3.  **默认值**：
    如果上述情况均不存在，则使用代码中定义的默认值（`SettingsMap`）。

## 管理设置

管理员可以通过管理控制台中的 **全局设置** 页面来管理这些设置。

### 支持的设置类型

系统支持多种类型的设置，并提供相应的UI验证：

*   **文本**：简单的字符串值。
*   **布尔值**：布尔值（开启/关闭开关）。
*   **数字**：数值类型（整数/浮点数）。
*   **选项**：从预定义选项中进行下拉选择。
*   **文件**：允许上传文件（例如用于替换logo或横幅）。

## 开发者指南

### 定义新设置

要添加新的全局设置，请在 `Aiursoft.Template.Configuration.SettingsMap` 类中添加新的定义：

```csharp
new GlobalSettingDefinition
{
    Key = "NewFeatureEnabled",
    Name = "Enable New Feature",
    Description = "Whether to enable the new experimental feature.",
    Type = SettingType.Bool,
    DefaultValue = "False"
}
```

### 访问设置

在您的服务或控制器中通过注入 `GlobalSettingsService` 来访问设置：

```csharp
public class MyService(GlobalSettingsService settingsService)
{
    public async Task DoWorkAsync()
    {
        // Get raw string value
        var brandName = await settingsService.GetSettingValueAsync("BrandName");

        // Get typed value
        if (await settingsService.GetBoolSettingAsync("NewFeatureEnabled"))
        {
            // Feature logic...
        }
    }
}
```

### 配置覆盖

要覆盖生产环境中的设置（例如使用 Docker 或 Kubernetes），只需设置一个环境变量：

```bash
# Overrides the 'BrandName' setting
GLOBALSETTINGS__BRANDNAME="My Custom Brand"
```
